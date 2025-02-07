import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from wtt.database.config import engine, get_db, init_db
from wtt.models.token import Token
from wtt.models.user import User
from sqlalchemy.orm import sessionmaker

def test_database_connection():
    """
    Test database connection and basic operations.
    """
    try:
        # Test connection
        connection = engine.connect()
        print("✅ Database Connection Successful")
        connection.close()

        # Initialize database
        init_db()
        print("✅ Database Tables Initialized")

        # Create a test session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Test Token model
        test_token = Token(
            address='0x1234567890123456789012345678901234567890',
            symbol='TEST',
            name='Test Token',
            decimals=18,
            is_native=False
        )
        session.add(test_token)
        session.commit()
        print("✅ Token Creation Successful")

        # Test User model
        test_user = User(
            username='test_user',
            email='test@example.com',
            hashed_password='hashed_password_placeholder'
        )
        session.add(test_user)
        session.commit()
        print("✅ User Creation Successful")

        # Verify insertions
        stored_token = session.query(Token).filter_by(symbol='TEST').first()
        stored_user = session.query(User).filter_by(username='test_user').first()

        assert stored_token is not None, "Token not stored correctly"
        assert stored_user is not None, "User not stored correctly"

        print("🎉 Database Test Completed Successfully!")

    except Exception as e:
        print(f"❌ Database Test Failed: {e}")
        raise

if __name__ == "__main__":
    test_database_connection()