import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from wtt.agents.search_agent import SearchExtractionAgent
from wtt.models.token import Token
from wtt.database.config import db_session

def test_search_agent():
    """
    Test the Search Extraction Agent's core functionalities.
    """
    try:
        # Create a test token
        session = db_session()
        test_token = Token(
            address='0x1234567890123456789012345678901234567890',
            symbol='TEST',
            name='Test Token',
            decimals=18,
            is_native=False
        )
        session.add(test_token)
        session.commit()

        # Initialize Search Agent
        search_agent = SearchExtractionAgent()
        print("✅ Search Agent Initialized")

        # Test search query generation
        search_query = search_agent.generate_search_query(test_token.name)
        print(f"✅ Generated Search Query: {search_query}")
        assert search_query, "Search query generation failed"

        # Test token data processing
        token_context = search_agent.process_token_data(test_token)
        print("✅ Token Data Processing Completed")

        # Verify context contains expected keys
        assert 'name' in token_context, "Token name missing in context"
        assert 'enriched_data' in token_context, "Enriched data missing"
        assert 'web_results' in token_context, "Web results missing"

        # Test token metadata update (placeholder)
        search_agent.update_token_metadata(token_context)
        print("✅ Token Metadata Update Attempted")

        print("🎉 Search Agent Test Completed Successfully!")

    except Exception as e:
        print(f"❌ Search Agent Test Failed: {e}")
        raise
    finally:
        # Clean up test data
        session.query(Token).filter_by(symbol='TEST').delete()
        session.commit()
        session.close()

if __name__ == "__main__":
    test_search_agent()