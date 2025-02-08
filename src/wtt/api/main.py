import os
# Import logging au début
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncpg
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from tavily import TavilyClient

from ..database.config import get_db, init_db
from ..models.token import Token
from ..models.user import User
from ..agents.search_agent import SearchExtractionAgent
from ..agents.ranking_agent import UserRankingAgent

# Load environment variables
load_dotenv()

# Initialize Tavily client
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Configure logging AVANT toute utilisation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("wtt_api")  # Donner un nom spécifique au logger

# Initialize FastAPI application
app = FastAPI(
    title=os.getenv('APP_TITLE', "World Token Tracker (WTT)"),
    description="AI-powered token verification platform",
    version="0.1.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenResearchRequest(BaseModel):
    token_name: str = Field(..., description="Name of the token to research")
    search_depth: str = Field(default="advanced", description="Depth of search: 'basic' or 'advanced'")

@app.on_event("startup")
async def startup_event():
    """Test database connection on startup"""
    try:
        # Test database connection
        conn = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )

        # Simple connection test
        await conn.execute('SELECT 1')
        logger.info("Successfully connected to the database!")

    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise
    finally:
        # Ensure the connection is closed
        await conn.close()

@app.get("/tokens/verify/{token_id}")
async def verify_token(token_id: int, db: AsyncSession = Depends(get_db)):
    """Verify token endpoint"""
    try:
        logger.info(f"Processing verification request for token_id: {token_id}")

        # Récupérer uniquement le nom du token
        query = select(Token.name).where(Token.id == token_id)
        result = await db.execute(query)
        token_name = result.scalar_one_or_none()

        if not token_name:
            logger.warning(f"Token with id {token_id} not found")
            raise HTTPException(status_code=404, detail="Token not found")

        logger.info(f"Found token name: {token_name}")

        # Initialiser le search agent et obtenir les informations
        search_agent = SearchExtractionAgent()
        token_information = await search_agent.process_token_data(token_name)

        logger.info(f"Successfully processed token {token_id}")
        return {
            "token_name": token_name,
            "information": token_information
        }

    except Exception as e:
        logger.error(f"Error processing token {token_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/tokens/answer")
async def submit_token_verification(
    token_id: int,
    question_id: int,
    user_id: int,
    answer: bool,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a user's verification answer for a token.
    """
    ranking_agent = UserRankingAgent()

    # In a real implementation, you'd retrieve the expected answer from the database
    expected_answer = True  # Placeholder

    try:
        user_metrics = ranking_agent.process_user_answer(
            user_id,
            question_id,
            answer,
            expected_answer
        )

        return {
            "status": "success",
            "user_metrics": user_metrics
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/leaderboard")
async def get_leaderboard():
    """
    Retrieve the current user leaderboard.
    """
    ranking_agent = UserRankingAgent()
    leaderboard = ranking_agent.get_leaderboard()

    return {
        "leaderboard": leaderboard
    }

# Monitoring and Health Check
@app.get("/health")
async def health_check():
    """
    Simple health check endpoint.
    """
    return {
        "status": "healthy",
        "version": "0.1.0"
    }

@app.post("/research/token")
async def research_token(request: TokenResearchRequest):
    """
    Research information about a specific token using Tavily search.
    Returns comprehensive information from multiple sources.
    """
    try:
        logger.info(f"Starting research for token: {request.token_name}")

        # Generate search queries for different aspects
        queries = [
            f"{request.token_name} blockchain platform technical details",
            f"{request.token_name} official website documentation",
            f"{request.token_name} market analysis {datetime.now().strftime('%Y-%m')}"
        ]

        # Execute searches concurrently
        results = []
        for query in queries:
            try:
                search_result = await tavily_client.search(
                    query=query,
                    search_depth=request.search_depth,
                    max_results=5,
                    include_answer=True,
                    include_raw_content=True,
                    include_images=False
                )
                results.append({
                    "query": query,
                    "answer": search_result.get("answer", ""),
                    "sources": [
                        {
                            "title": r.get("title", ""),
                            "url": r.get("url", ""),
                            "content": r.get("content", ""),
                            "score": r.get("relevance_score", 0)
                        }
                        for r in search_result.get("results", [])
                    ]
                })
            except Exception as e:
                logger.error(f"Error in search query '{query}': {str(e)}")
                continue

        # Structure the response
        research_summary = {
            "token_name": request.token_name,
            "timestamp": datetime.now().isoformat(),
            "research_results": results,
            "sources_count": sum(len(r["sources"]) for r in results)
        }

        logger.info(f"Completed research for {request.token_name} with {research_summary['sources_count']} sources")
        return research_summary

    except Exception as e:
        error_msg = f"Error researching token {request.token_name}: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)