import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from ..database.config import get_db, init_db
from ..models.token import Token
from ..models.user import User
from ..agents.search_agent import SearchExtractionAgent
from ..agents.question_agent import QuestionGenerationAgent
from ..agents.ranking_agent import UserRankingAgent

# Initialize FastAPI application
app = FastAPI(
    title="World Token Tracker (WTT)",
    description="AI-powered token verification platform",
    version="0.1.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize database tables on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Token Verification Endpoints
@app.get("/tokens/verify/{token_id}")
async def verify_token(token_id: int, db: Session = Depends(get_db)):
    """
    Initiate token verification process for a specific token.
    """
    token = db.query(Token).filter(Token.id == token_id).first()

    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    # Initialize agents
    search_agent = SearchExtractionAgent()
    question_agent = QuestionGenerationAgent()

    # Process token data
    token_context = search_agent.process_token_data(token)

    # Generate verification questions
    questions = question_agent.process_token_questions(token, token_context)

    return {
        "token": {
            "id": token.id,
            "name": token.name,
            "symbol": token.symbol
        },
        "verification_questions": questions
    }

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