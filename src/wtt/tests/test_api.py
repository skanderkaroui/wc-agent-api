import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
from httpx import AsyncClient
from wtt.api.main import app
from wtt.database.config import db_session
from wtt.models.token import Token
from wtt.models.user import User

async def setup_test_data():
    """Set up test data and return session and test objects"""
    session = db_session()

    # Create test data
    test_token = Token(
        address='0x1234567890123456789012345678901234567890',
        symbol='TEST',
        name='Test Token',
        decimals=18,
        is_native=False
    )
    session.add(test_token)

    test_user = User(
        username='test_api_user',
        email='api_test@example.com',
        hashed_password='hashed_password_placeholder'
    )
    session.add(test_user)

    session.commit()
    return session, test_token, test_user

async def cleanup_test_data(session):
    """Clean up test data"""
    session.query(Token).filter_by(symbol='TEST').delete()
    session.query(User).filter_by(username='test_api_user').delete()
    session.commit()
    session.close()

async def test_api_endpoints():
    """
    Test all API endpoints functionality.
    """
    try:
        # Set up test data
        session, test_token, test_user = await setup_test_data()
        print("✅ Test Data Setup Complete")

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Test health check endpoint
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "healthy", "version": "0.1.0"}
            print("✅ Health Check Endpoint Working")

            # Test token verification endpoint
            response = await client.get(f"/tokens/verify/{test_token.id}")
            assert response.status_code == 200
            verification_data = response.json()
            assert "token" in verification_data
            assert "verification_questions" in verification_data
            print("✅ Token Verification Endpoint Working")

            # Test token answer submission endpoint
            response = await client.post("/tokens/answer", json={
                "token_id": test_token.id,
                "question_id": 1,
                "user_id": test_user.id,
                "answer": True
            })
            assert response.status_code == 200
            answer_response = response.json()
            assert "status" in answer_response
            assert "user_metrics" in answer_response
            print("✅ Token Answer Submission Endpoint Working")

            # Test leaderboard endpoint
            response = await client.get("/leaderboard")
            assert response.status_code == 200
            leaderboard_data = response.json()
            assert "leaderboard" in leaderboard_data
            print("✅ Leaderboard Endpoint Working")

        print("🎉 API Endpoint Tests Completed Successfully!")

    except Exception as e:
        print(f"❌ API Endpoint Test Failed: {e}")
        raise
    finally:
        # Clean up test data
        await cleanup_test_data(session)

def main():
    """Run all API tests"""
    asyncio.run(test_api_endpoints())

if __name__ == "__main__":
    main()