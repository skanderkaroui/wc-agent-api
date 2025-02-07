import os
import asyncio
import asyncpg
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

# Load environment variables from .env file
load_dotenv()

# Construct DATABASE_URL using environment variables
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

# Create SQLAlchemy async engine
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

# Create a thread-local session factory
db_session = scoped_session(SessionLocal)

# Base class for declarative models
Base = declarative_base()

async def init_db():
    """
    Initialize the database by creating all tables defined in models.
    """
    from ..models.token import Token
    from ..models.user import User

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables initialized successfully.")

async def get_db():
    """
    Dependency that creates a new database session for each request.
    """
    db = db_session()
    try:
        yield db
    finally:
        await db.close()

def drop_db():
    """
    Drop all database tables. Use with caution!
    """
    Base.metadata.drop_all(bind=engine)
    print("All database tables dropped.")