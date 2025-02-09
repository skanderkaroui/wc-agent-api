import os
import asyncio
import asyncpg
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
from pgvector.sqlalchemy import Vector

# Load environment variables from .env file
load_dotenv()

# Database configuration with defaults
DB_USER = os.getenv("POSTGRES_USER", "wo_api")
DB_PASSWORD = quote_plus(
    os.getenv("POSTGRES_PASSWORD", "pic<)FeD24&@3acb")
)
DB_HOST = os.getenv("POSTGRES_HOST", "34.66.250.90")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "wo-api")

# Construct database URL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy async engine
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=True,
    future=True,
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
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
