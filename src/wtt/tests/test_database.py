import asyncio
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

async def test_connection():
    try:
        # Connect to database using environment variables
        conn = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )

        print("\n✅ Successfully connected to database!")

        # Create users table if it doesn't exist
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                worldcoin_sub VARCHAR(100) UNIQUE,

                -- Gamification and ranking metrics
                verification_score FLOAT DEFAULT 0.0,
                total_verifications INTEGER DEFAULT 0,
                accuracy_rate FLOAT DEFAULT 0.0,
                total_rewards FLOAT DEFAULT 0.0,

                -- Timestamps
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP WITH TIME ZONE
            )
        """)
        print("✅ Users table created/verified")

        # List all tables
        tables = await conn.fetch("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)

        print("\nTables in database:")
        for table in tables:
            print(f"- {table['table_name']}")

        # Show users table structure
        columns = await conn.fetch("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position;
        """)

        print("\nUsers table structure:")
        for col in columns:
            print(f"  - {col['column_name']}: {col['data_type']} "
                  f"(nullable: {col['is_nullable']}, default: {col['column_default']})")

        # Test inserting a sample user with ranking metrics
        await conn.execute("""
            INSERT INTO users (
                username, email, hashed_password, worldcoin_sub,
                verification_score, total_verifications, accuracy_rate, total_rewards
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (username) DO NOTHING
        """, 'test_user', 'test@example.com', 'hashed_password_placeholder', 'test123',
             10.5, 5, 85.5, 100.0)
        print("\n✅ Sample user created with ranking metrics")

        # Verify user insertion and ranking metrics
        user = await conn.fetchrow('SELECT * FROM users WHERE username = $1', 'test_user')
        if user:
            print(f"\n✅ Retrieved test user:")
            print(f"  - Username: {user['username']}")
            print(f"  - Email: {user['email']}")
            print(f"  - Verification Score: {user['verification_score']}")
            print(f"  - Total Verifications: {user['total_verifications']}")
            print(f"  - Accuracy Rate: {user['accuracy_rate']}%")
            print(f"  - Total Rewards: {user['total_rewards']} WTT")

        await conn.close()
        print("\n🎉 Database test completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_connection())