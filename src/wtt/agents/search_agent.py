import os
import logging
from typing import Dict, List, Optional, Any

from jina import Client, Document, DocumentArray
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from ..database.config import db_session
from ..models.token import Token

class SearchExtractionAgent:
    def __init__(self, openai_api_key: Optional[str] = None, jina_host: str = "grpc://localhost:51001"):
        """
        Initialize the Search Extraction Agent with OpenAI and Jina configuration.

        :param openai_api_key: Optional API key for OpenAI. If not provided, uses environment variable.
        :param jina_host: Jina server host address
        """
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.llm = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            model_name='gpt-4o',
            temperature=0.2
        )
        self.jina_client = Client(host=jina_host)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def generate_search_query(self, token_name: str) -> str:
        """
        Generate an optimized search query for a given token.

        :param token_name: Name of the token to search
        :return: Refined search query
        """
        query_prompt = PromptTemplate(
            input_variables=['token_name'],
            template="""
            Generate a precise web search query to find comprehensive information about the cryptocurrency token: {token_name}.
            The query should help extract details about its origin, purpose, technology, and current status.

            Suggested Query:
            """
        )

        query = self.llm.predict(query_prompt.format(token_name=token_name))
        return query.strip()

    async def web_extract(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Extract web information using Jina search.

        :param query: Search query
        :param max_results: Maximum number of results to retrieve
        :return: List of extracted web page information
        """
        try:
            # Create a Document with the search query
            doc = Document(text=query)

            # Use Jina's client to search
            results = await self.jina_client.post('/search', inputs=DocumentArray([doc]), parameters={'limit': max_results})

            # Process results
            extracted_data = []
            for match in results[0].matches:
                extracted_data.append({
                    'url': match.tags.get('url', ''),
                    'title': match.tags.get('title', ''),
                    'content': match.text,
                    'score': float(match.scores['cosine'].value)
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