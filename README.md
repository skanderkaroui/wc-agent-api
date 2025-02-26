# World Token Tracker (WTT) - AI Agent 🌐🤖

## Overview
World Token Tracker is an AI-powered platform designed to verify token authenticity and quality through automated intelligence and human-powered verification. The AI Agent component is specifically designed to fetch and analyze information about the WorldChain coin, generating insightful questions based on the collected data.

## Key Features
- 🤖 Automated Intelligence Rating (AIR)
- 👥 Human-Powered Analysis (HPA)
- 🏆 User Ranking & Reward System
- 🔍 Automated WorldChain data collection
- 📊 AI-powered analysis of collected information
- ❓ Dynamic question generation based on context

## System Architecture
- **Database**: PostgreSQL with PG_Vector
- **AI Agents**:
  - Search & Information Extraction Agent
  - Question Generation Agent
  - User Ranking & Reward Agent
- **Messaging**: Kafka
- **API**: FastAPI
- **Caching**: Redis
- **LLM**: OpenAI
- **Orchestration**: LangChain

## Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Redis
- Kafka
- pip (Python package installer)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/skanderkaroui/wc-agent-api.git
cd wc-agent-api
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the root directory with the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
```

### 5. Initialize Database
```bash
python -m src.wtt.database.config init_db
```

## Running the Application

### Development Server
```bash
uvicorn src.wtt.api.main:app --reload
```

### AI Agent Usage
1. Ensure your virtual environment is activated
2. Run the main application:
   ```bash
   python main.py
   ```
3. Follow the prompts to input the name of the WorldChain coin
4. Review the generated questions based on the fetched information

### Production Deployment
```bash
gunicorn src.wtt.api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## API Endpoints

### Token Verification
- `GET /tokens/verify/{token_id}`: Initiate token verification
- `POST /tokens/answer`: Submit verification answer

### User Ranking
- `GET /leaderboard`: Retrieve current leaderboard
