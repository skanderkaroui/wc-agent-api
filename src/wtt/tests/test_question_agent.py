import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from wtt.agents.question_agent import QuestionGenerationAgent
from wtt.models.token import Token
from wtt.database.config import db_session

def test_question_agent():
    """
    Test the Question Generation Agent's core functionalities.
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

        # Initialize Question Agent
        question_agent = QuestionGenerationAgent()
        print("✅ Question Agent Initialized")

        # Prepare a mock context
        mock_context = {
            'name': test_token.name,
            'description': 'A test token for verification system',
            'website': 'https://testtoken.com'
        }

        # Test question generation
        questions = question_agent.generate_verification_questions(test_token, mock_context)
        print("✅ Questions Generated")

        # Validate questions
        assert len(questions) > 0, "No questions generated"
        for question in questions:
            assert 'token_id' in question, "Token ID missing in question"
            assert 'question_text' in question, "Question text missing"
            assert 'type' in question, "Question type missing"
            assert 'difficulty' in question, "Question difficulty missing"
            print(f"✅ Question: {question['question_text']}")

        # Test question distribution (mock)
        question_agent.distribute_questions(questions)
        print("✅ Questions Distribution Attempted")

        # Full process test
        processed_questions = question_agent.process_token_questions(test_token, mock_context)
        print("✅ Full Question Process Completed")
        assert len(processed_questions) > 0, "No questions processed"

        print("🎉 Question Agent Test Completed Successfully!")

    except Exception as e:
        print(f"❌ Question Agent Test Failed: {e}")
        raise
    finally:
        # Clean up test data
        session.query(Token).filter_by(symbol='TEST').delete()
        session.commit()
        session.close()

if __name__ == "__main__":
    test_question_agent()