import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field

from ..database.config import db_session
from ..models.token import Token

class TavilyQuery(BaseModel):
    query: str = Field(description="web search query")
    topic: str = Field(description="type of search, should be 'general' or 'news'")
    days: int = Field(description="number of days back to run 'news' search")
    domains: Optional[List[str]] = Field(default=None, description="list of domains to include in the research")

class SearchExtractionAgent:
    def __init__(self, openai_api_key: Optional[str] = None, tavily_api_key: Optional[str] = None):
        """
        Initialize the Search Extraction Agent with OpenAI and Tavily configuration.

        :param openai_api_key: Optional API key for OpenAI. If not provided, uses environment variable.
        :param tavily_api_key: Optional API key for Tavily. If not provided, uses environment variable.
        """
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.tavily_api_key = tavily_api_key or os.getenv('TAVILY_API_KEY')
        self.llm = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            model_name='gpt-4o',
            temperature=0.2
        )
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def generate_search_query(self, token_name: str) -> TavilyQuery:
        """
        Generate an optimized search query for a given token.

        :param token_name: Name of the token to search
        :return: TavilyQuery object with search parameters
        """
        query_prompt = PromptTemplate(
            input_variables=['token_name'],
            template="""
            Generate a precise web search query to find comprehensive information about the cryptocurrency token: {token_name}.
            The query should help extract details about its origin, purpose, technology, and current status.
            Consider whether this is a publicly traded token that would be featured in news.

            Suggested Query:
            """
        )

        query_text = self.llm.predict(query_prompt.format(token_name=token_name))

        # Determine if token is likely to be in news
        is_news = "news" if self._is_newsworthy_token(token_name) else "general"

        return TavilyQuery(
            query=query_text.strip(),
            topic=is_news,
            days=7 if is_news == "news" else 30,
            domains=None  # Can be customized based on token type
        )

    def _is_newsworthy_token(self, token_name: str) -> bool:
        """
        Determine if a token is likely to be featured in news.
        """
        newsworthy_prompt = PromptTemplate(
            input_variables=['token_name'],
            template="Is {token_name} a publicly traded or major cryptocurrency token that would be frequently featured in mainstream news? Answer only yes or no."
        )
        response = self.llm.predict(newsworthy_prompt.format(token_name=token_name))
        return response.lower().strip() == "yes"

    async def web_extract(self, query: TavilyQuery, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Extract web information using Tavily search.

        :param query: TavilyQuery object with search parameters
        :param max_results: Maximum number of results to retrieve
        :return: List of extracted web page information
        """
        try:
            # Construct query with date for the most recent results
            query_with_date = f"{query.query} {datetime.now().strftime('%m-%Y')}"

            # Initialize Tavily client
            from tavily import TavilyClient
            tavily_client = TavilyClient(api_key=self.tavily_api_key)

            # Perform search
            response = await tavily_client.search(
                query=query_with_date,
                topic=query.topic,
                days=query.days,
                max_results=max_results,
                include_domains=query.domains if query.domains else None
            )

            # Process and format results
            extracted_data = []
            for result in response['results']:
                extracted_data.append({
                    'url': result.get('url', ''),
                    'title': result.get('title', ''),
                    'content': result.get('content', ''),
                    'score': result.get('relevance_score', 0.0)
                })

            return extracted_data

        except Exception as e:
            self.logger.error(f"Web extraction error: {e}")
            return []

    async def process_token_data(self, token: Token) -> Dict[str, Any]:
        """
        Process and enrich token data through web extraction and AI analysis.

        :param token: Token model instance
        :return: Enriched token information
        """
        search_query = self.generate_search_query(token.name)
        web_results = await self.web_extract(search_query)

        # Analyze and extract key information
        enrichment_prompt = PromptTemplate(
            input_variables=['token_name', 'web_results'],
            template="""
            Analyze the following web search results for the token {token_name}:
            {web_results}

            Extract and summarize key information about:
            1. Token's primary purpose
            2. Technology or blockchain it's built on
            3. Current market status
            4. Potential verification flags

            Provide a concise, structured summary.
            """
        )

        enrichment_result = self.llm.predict(
            enrichment_prompt.format(
                token_name=token.name,
                web_results=str(web_results)
            )
        )

        return {
            'name': token.name,
            'enriched_data': enrichment_result,
            'web_results': web_results
        }

    def update_token_metadata(self, token_data: Dict[str, Any]):
        """
        Update token metadata in the database based on web extraction.

        :param token_data: Enriched token information
        """
        session = db_session()
        try:
            token = session.query(Token).filter_by(name=token_data['name']).first()
            if token:
                # Update token metadata based on enriched data
                # Implement specific update logic here
                session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Token metadata update error: {e}")
        finally:
            session.close()