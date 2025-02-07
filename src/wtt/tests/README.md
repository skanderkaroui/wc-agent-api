# World Token Tracker - Test Suite

## Overview
This directory contains individual test scripts for each major component of the World Token Tracker system. These tests are designed to verify the functionality of individual modules and ensure system reliability.

## Test Scripts

### 1. `test_database.py`
- Tests database connection
- Verifies table creation
- Checks basic CRUD operations for Token and User models

### 2. `test_search_agent.py`
- Validates Search Extraction Agent
- Tests query generation
- Checks token data processing
- Verifies metadata update mechanism

### 3. `test_question_agent.py`
- Tests Question Generation Agent
- Validates question generation process
- Checks question distribution mechanism
- Verifies question processing workflow

### 4. `test_ranking_agent.py`
- Tests User Ranking and Reward Agent
- Validates user answer processing
- Checks leaderboard retrieval
- Verifies reward distribution and notification mechanisms

### 5. `test_api.py`
- Tests API endpoints
- Validates health check
- Checks token verification process
- Verifies answer submission and leaderboard retrieval

## Running Tests

### Individual Test
```bash
python -m src.wtt.tests.test_database
python -m src.wtt.tests.test_search_agent
# ... and so on
```

### Using pytest
```bash
pytest src/wtt/tests/
```

## Best Practices
- Each test script is self-contained
- Tests clean up their own test data
- Provides clear console output for debugging
- Uses minimal external dependencies

## Notes
- Ensure `.env` is properly configured before running tests
- Some tests use mock data and placeholder implementations