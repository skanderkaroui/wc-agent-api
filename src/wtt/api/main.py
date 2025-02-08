import os
# Import logging au début
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..database.config import get_db, init_db
from ..models.token import Token
from ..models.user import User
from ..agents.search_agent import SearchExtractionAgent

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

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

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
    db: Session = Depends(get_db)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)