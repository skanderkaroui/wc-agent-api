import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from wtt.agents.ranking_agent import UserRankingAgent
from wtt.models.user import User
from wtt.database.config import db_session

def test_ranking_agent():
    """
    Test the User Ranking and Reward Agent's core functionalities.
    """
    try:
        # Create test users
        session = db_session()
        test_users = [
            User(
                username=f'test_user_{i}',
                email=f'test{i}@example.com',
                hashed_password='hashed_password_placeholder'
            ) for i in range(3)
        ]

        for user in test_users:
            session.add(user)
        session.commit()

        # Initialize Ranking Agent
        ranking_agent = UserRankingAgent()
        print("✅ Ranking Agent Initialized")

        # Test user answer processing
        for i, user in enumerate(test_users):
            # Simulate different answer scenarios
            is_correct = i % 2 == 0  # Alternate correct/incorrect answers
            user_metrics = ranking_agent.process_user_answer(
                user_id=user.id,
                question_id=i,
                answer=is_correct,
                expected_answer=is_correct
            )
            print(f"✅ User {user.username} Metrics Updated")

            # Validate metrics
            assert 'verification_score' in user_metrics, "Verification score missing"
            assert 'total_verifications' in user_metrics, "Total verifications missing"
            assert 'accuracy_rate' in user_metrics, "Accuracy rate missing"
            assert 'total_rewards' in user_metrics, "Total rewards missing"

        # Test leaderboard retrieval
        leaderboard = ranking_agent.get_leaderboard(limit=2)
        print("✅ Leaderboard Retrieved")
        assert len(leaderboard) > 0, "Leaderboard is empty"

        for user in leaderboard:
            print(f"Leaderboard User: {user['username']} - Score: {user['verification_score']}")

        # Test reward distribution (mock)
        ranking_agent.distribute_rewards()
        print("✅ Rewards Distribution Attempted")

        # Test user notification
        for user in test_users:
            ranking_agent.notify_user(user.id, "Test notification message")
        print("✅ User Notifications Sent")

        print("🎉 Ranking Agent Test Completed Successfully!")

    except Exception as e:
        print(f"❌ Ranking Agent Test Failed: {e}")
        raise
    finally:
        # Clean up test data
        session.query(User).filter(User.username.like('test_user_%')).delete()
        session.commit()
        session.close()

if __name__ == "__main__":
    test_ranking_agent()