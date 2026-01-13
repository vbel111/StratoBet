"""
Prediction Service
Coordinates feature calculation and model prediction
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from app.services.ml_service import ml_service
from app.services.feature_service import feature_service
from app.schemas.prediction import PredictionResponse


class PredictionService:
    """Service for generating predictions"""
    
    def generate_prediction(
        self,
        db: Session,
        home_team: str,
        away_team: str,
        league: str,
        match_date: datetime,
        fixture_id: str = None,
        over_25_odds: float = None,
        under_25_odds: float = None
    ) -> PredictionResponse:
        """
        Generate a prediction for a match.
        
        Args:
            db: Database session
            home_team: Home team name
            away_team: Away team name
            league: League name
            match_date: Match date
            fixture_id: Optional fixture ID
        
        Returns:
            PredictionResponse with full prediction details
        """
        # Generate fixture ID if not provided
        if fixture_id is None:
            fixture_id = f"match_{home_team}_{away_team}_{match_date.strftime('%Y%m%d')}"
        
        # Step 1: Engineer features
        features = feature_service.engineer_features_for_match(
            db, home_team, away_team, league, match_date,
            over_25_odds=over_25_odds,
            under_25_odds=under_25_odds
        )
        
        # Step 2: Get prediction from ML model
        over_prob, under_prob, confidence = ml_service.predict(features)
        
        # Step 3: Get confidence level
        confidence_level = ml_service.get_confidence_level(confidence)
        
        # Step 4: Generate key factors
        key_factors = self._generate_key_factors(features, home_team, away_team)
        
        # Step 5: Build response
        prediction = PredictionResponse(
            fixture_id=fixture_id,
            date=match_date,
            league=league,
            home_team=home_team,
            away_team=away_team,
            over_25_probability=over_prob,
            under_25_probability=under_prob,
            confidence_score=confidence,
            confidence_level=confidence_level,
            key_factors=key_factors,
            model_version=ml_service.model_version,
            generated_at=datetime.utcnow()
        )
        
        return prediction
    
    def _generate_key_factors(self, features: dict, home_team: str, 
                             away_team: str) -> List[str]:
        """Generate human-readable key factors"""
        factors = []
        
        # Home team scoring
        if features['home_home_avg_scored'] >= 2.0:
            factors.append(
                f"{home_team} averaging {features['home_home_avg_scored']:.1f} goals/game at home (last 5)"
            )
        
        # Away team conceding
        if features['away_away_avg_conceded'] >= 1.5:
            factors.append(
                f"{away_team} conceding {features['away_away_avg_conceded']:.1f} goals/game away (last 5)"
            )
        
        # H2H
        if features['h2h_games'] >= 3 and features['h2h_avg_goals'] >= 2.5:
            factors.append(
                f"Last {int(features['h2h_games'])} H2H matches averaged {features['h2h_avg_goals']:.1f} total goals"
            )
        
        # League context
        if features['league_avg_goals'] >= 2.7:
            factors.append(
                f"League averaging {features['league_avg_goals']:.1f} goals/game (high-scoring)"
            )
        
        # Combined attack
        if features['total_avg_scored'] >= 3.0:
            factors.append(
                f"Combined attack averaging {features['total_avg_scored']:.1f} goals/game"
            )
        
        return factors[:5]  # Return top 5 factors


# Global prediction service instance
prediction_service = PredictionService()
