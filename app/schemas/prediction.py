"""
Pydantic schemas for API requests and responses
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class PredictionResponse(BaseModel):
    """Prediction response schema"""
    
    fixture_id: str
    date: datetime
    league: str
    home_team: str
    away_team: str
    
    # Prediction
    over_25_probability: float = Field(..., ge=0, le=1, description="Probability of Over 2.5 goals")
    under_25_probability: float = Field(..., ge=0, le=1, description="Probability of Under 2.5 goals")
    
    # Confidence
    confidence_score: float = Field(..., ge=0, le=1, description="Model confidence (0-1)")
    confidence_level: str = Field(..., description="Low, Medium, High, Very High")
    
    # Context
    key_factors: List[str] = Field(default_factory=list, description="Key factors influencing prediction")
    
    # Odds (optional)
    bookmaker_over_25_odds: Optional[float] = None
    bookmaker_under_25_odds: Optional[float] = None
    odds_updated_at: Optional[datetime] = None
    
    # Metadata
    model_version: str
    generated_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "fixture_id": "match_12345",
                "date": "2026-01-10T15:00:00Z",
                "league": "Premier League",
                "home_team": "Arsenal",
                "away_team": "Chelsea",
                "over_25_probability": 0.6421,
                "under_25_probability": 0.3579,
                "confidence_score": 0.7142,
                "confidence_level": "High",
                "key_factors": [
                    "Arsenal averaging 2.4 goals/game at home (last 5)",
                    "Chelsea conceding 1.8 goals/game away (last 5)",
                    "Last 3 H2H averaged 3.3 total goals"
                ],
                "bookmaker_over_25_odds": 1.72,
                "bookmaker_under_25_odds": 2.10,
                "model_version": "v1.0.0",
                "generated_at": "2026-01-08T12:00:00Z"
            }
        }


class PredictionListResponse(BaseModel):
    """List of predictions response"""
    
    predictions: List[PredictionResponse]
    total: int
    page: int = 1
    page_size: int = 20


class FixtureBase(BaseModel):
    """Fixture base schema"""
    
    fixture_id: str
    date: datetime
    league: str
    home_team: str
    away_team: str


class FixtureResponse(FixtureBase):
    """Fixture response with optional prediction"""
    
    prediction: Optional[PredictionResponse] = None
    
    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str
    timestamp: datetime
    version: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-01-08T12:00:00Z",
                "version": "1.0.0"
            }
        }


class ModelHealthResponse(BaseModel):
    """ML Model health response"""
    
    model_loaded: bool
    model_version: str
    model_path: str
    features_count: int
    last_prediction_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_loaded": True,
                "model_version": "v1.0.0",
                "model_path": "../ml-pipeline/models/random_forest_v1.0.0.pkl",
                "features_count": 16,
                "last_prediction_at": "2026-01-08T11:45:00Z"
            }
        }
