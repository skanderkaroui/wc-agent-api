import os
import asyncio
import asyncpg
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def test_database_connection():
    try:
        # Connect to the database using environment variables
        conn = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )

        print("\n✅ Successfully connected to the database!")

        # Close the connection
        await conn.close()

    except Exception as e:
        print(f"❌ Failed to connect to the database: {e}")

# Run the test
if __name__ == "__main__":
    asyncio.run(test_database_connection())