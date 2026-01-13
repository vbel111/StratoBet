"""
Prediction API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.services.prediction_service import prediction_service
from app.services.ml_service import ml_service
from app.schemas.prediction import PredictionResponse
from pydantic import BaseModel

router = APIRouter()


class PredictionRequest(BaseModel):
    """Request body for generating a prediction"""
    home_team: str
    away_team: str
    league: str
    match_date: datetime
    fixture_id: str = None


@router.post("/predict", response_model=PredictionResponse)
async def generate_prediction(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a prediction for a match.
    
    - **home_team**: Name of home team
    - **away_team**: Name of away team
    - **league**: League name (e.g., "Premier League")
    - **match_date**: Match date and time
    - **fixture_id**: Optional ID for the fixture
    """
    # Check if model is loaded
    if not ml_service.is_loaded():
        raise HTTPException(
            status_code=503,
            detail="ML model not loaded. Please start the server."
        )
    
    try:
        prediction = prediction_service.generate_prediction(
            db=db,
            home_team=request.home_team,
            away_team=request.away_team,
            league=request.league,
            match_date=request.match_date,
            fixture_id=request.fixture_id
        )
        
        return prediction
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating prediction: {str(e)}"
        )


@router.get("/test")
async def test_prediction(db: Session = Depends(get_db)):
    """
    Quick test endpoint with sample data
    """
    # Check if model is loaded
    if not ml_service.is_loaded():
        return {
            "error": "ML model not loaded",
            "message": "Model training may still be in progress"
        }
    
    # Generate test prediction
    try:
        prediction = prediction_service.generate_prediction(
            db=db,
            home_team="Arsenal",
            away_team="Chelsea",
            league="Premier League",
            match_date=datetime(2026, 1, 10, 15, 0, 0),
            fixture_id="test_match_001"
        )
        
        return prediction
        
    except Exception as e:
        return {
            "error": str(e),
            "message": "Error generating test prediction"
        }
