"""
Fixtures API Endpoints
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.services.fixture_service import fixture_service
from pydantic import BaseModel

router = APIRouter()


class FixtureResponse(BaseModel):
    """Fixture response schema"""
    fixture_id: str
    date: datetime
    league: str
    home_team: str
    away_team: str
    venue: Optional[str] = None
    status: str


@router.get("/upcoming", response_model=List[FixtureResponse])
async def get_upcoming_fixtures(
    league: Optional[str] = Query(None, description="Filter by league name"),
    days_ahead: int = Query(7, description="Days ahead to fetch (1-14)")
):
    """
    Get upcoming fixtures for all supported leagues.
    
    - **league**: Optional - filter by specific league (e.g., "Premier League")
    - **days_ahead**: Number of days ahead to fetch (default: 7)
    """
    days_ahead = min(max(days_ahead, 1), 14)  # Limit between 1-14 days
    
    fixtures = fixture_service.fetch_all_leagues_fixtures(days_ahead=days_ahead)
    
    # Filter by league if specified
    if league:
        fixtures = [f for f in fixtures if league.lower() in f['league'].lower()]
    
    # Convert to response models
    return [FixtureResponse(**fixture) for fixture in fixtures]


@router.get("/leagues")
async def get_supported_leagues():
    """Get list of supported leagues"""
    return {
        "leagues": [
            {"id": 39, "name": "Premier League", "country": "England"},
            {"id": 140, "name": "La Liga", "country": "Spain"},
            {"id": 135, "name": "Serie A", "country": "Italy"},
            {"id": 78, "name": "Bundesliga", "country": "Germany"},
            {"id": 61, "name": "Ligue 1", "country": "France"},
            {"id": 2, "name": "Champions League", "country": "Europe"}
        ]
    }
