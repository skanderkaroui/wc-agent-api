# Project Structure for World Token Tracker (WTT)

## Change Log

### 2024-02-14

- Added token metrics components and routes  
- Updated API structure for token data  
- Added dashboard and token detail pages  
- Implemented chart components  

## Root Directory Structure

```
wc-agent-api/
├── src/  # Source code directory
│   ├── wtt/  # Main application package
│   │   ├── agents/  # AI agent modules
│   │   ├── api/  # API endpoints
│   │   ├── database/  # Database configuration
│   │   ├── models/  # Data models
│   │   └── tests/  # Test suite
├── .env  # Environment variables
├── .env.example  # Example environment variables
├── .gitignore  # Git ignore file
├── README.md  # Project documentation
├── requirements.txt  # Python dependencies
└── setup.py  # Project setup configuration
```

## Agents Directory (`agents/`)

Contains AI agents responsible for various tasks:

```
agents/
├── search_agent.py  # Search and information extraction agent
├── question_agent.py  # Question generation agent
├── ranking_agent.py  # User ranking and reward agent
└── __init__.py  # Package initialization
```

## API Directory (`api/`)

Houses the FastAPI application and endpoint definitions:

```
api/
├── main.py  # Main FastAPI application
└── __init__.py  # Package initialization
```

## Database Directory (`database/`)

Manages database configuration and initialization:

```
database/
├── config.py  # Database configuration and session management
└── __init__.py  # Package initialization
```

## Models Directory (`models/`)

Defines SQLAlchemy models for database tables:

```
models/
├── user.py  # User model
├── token.py  # Token model
└── __init__.py  # Package initialization
```

## Tests Directory (`tests/`)

Includes test scripts for validating each component's functionality:

```
tests/
├── test_api.py  # Tests for API endpoints
├── test_database.py  # Tests for database operations
├── test_question_agent.py  # Tests for question generation agent
├── test_ranking_agent.py  # Tests for ranking agent
├── test_search_agent.py  # Tests for search agent
├── test_db_connection.py  # Tests for database connection
└── README.md  # Test suite documentation
```

## Key Configuration Files

- `.env`: Environment variables including API keys and database credentials  
- `requirements.txt`: Lists Python dependencies for the project  
- `setup.py`: Configuration for packaging the project  

## Development Patterns

### 1. API Integration
- FastAPI for RESTful API endpoints  
- Asynchronous database operations with SQLAlchemy  

### 2. AI Agents
- Modular design for search, question generation, and ranking  
- Integration with OpenAI and LangChain  

### 3. Testing
- Comprehensive test suite for all components  
- Uses pytest for test execution  

### 4. Database
- PostgreSQL with asyncpg for database operations  
- SQLAlchemy ORM for data modeling  

### 5. Performance
- Optimized data fetching and caching  
- Asynchronous processing for scalability  
