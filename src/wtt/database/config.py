import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

# Database connection configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://wo_api:pic<)FeD24&@3acb@34.66.250.90:5432/wo-api'
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Test connections before using them
    pool_size=10,        # Number of connections to keep open
    max_overflow=20      # Maximum number of connections to create beyond pool_size
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,     # Disable auto-commit
    autoflush=False,      # Disable auto-flush
    bind=engine
)

# Create a thread-local session factory
db_session = scoped_session(SessionLocal)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency that creates a new database session for each request.
    Ensures proper session management and connection pooling.
    """
    db = db_session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database by creating all tables defined in models.
    """
    from ..models.token import Token
    from ..models.user import User

    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully.")

def drop_db():
    """
    Drop all database tables. Use with caution!
    """
    Base.metadata.drop_all(bind=engine)
    print("All database tables dropped.")