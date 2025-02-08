import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from tavily import TavilyClient
from pydantic import BaseModel, Field

class SearchExtractionAgent:
    def __init__(self, tavily_api_key: Optional[str] = None):
        """
        Initialize the Search Extraction Agent with Tavily configuration.
        """
        self.tavily_api_key = tavily_api_key or os.getenv('TAVILY_API_KEY')
        self.client = TavilyClient(api_key=self.tavily_api_key)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def generate_search_query(self, token_name: str) -> str:
        """
        Generate an optimized search query for a given token.
        """
        return f"{token_name} cryptocurrency token blockchain details technical analysis"

    async def web_extract(self, query: str) -> List[Dict[str, Any]]:
        """
        Extract web information using Tavily search.
        """
        try:
            search_result = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=5,
                include_answer=True,
                include_raw_content=True,
                include_images=False
            )
            
            return {
                'answer': search_result.get('answer', ''),
                'results': search_result.get('results', [])
            }
            
        except Exception as e:
            self.logger.error(f"Web extraction error: {e}")
            return {'answer': '', 'results': []}

    def format_token_information(self, search_results: Dict) -> str:
        """
        Format search results into a comprehensive paragraph.
        """
        main_answer = search_results['answer']
        
        # Compile additional information from results
        additional_info = []
        for result in search_results['results']:
            if 'content' in result:
                additional_info.append(result['content'])

        # Combine all information into a structured paragraph
        formatted_text = f"""
{main_answer}

Additional Details:
{' '.join(additional_info[:3])}  # Limiting to first 3 results to keep it concise

Sources:
"""
        # Add sources
        for result in search_results['results']:
            if 'url' in result:
                formatted_text += f"- {result['url']}\n"

        return formatted_text

    async def process_token_data(self, token_name: str) -> str:
        """
        Process token data and return formatted information.
        """
        try:
            # Generate and execute search
            search_query = self.generate_search_query(token_name)
            search_results = await self.web_extract(search_query)
            
            # Format results into a comprehensive paragraph
            formatted_info = self.format_token_information(search_results)
            
            return formatted_info
            
        except Exception as e:
            self.logger.error(f"Error processing token data: {e}")
            return f"Error retrieving information for {token_name}: {str(e)}"