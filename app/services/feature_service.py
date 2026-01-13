"""
Feature Engineering Service
Calculates features for upcoming matches, reusing logic from ML pipeline
"""

import pandas as pd
from sqlalchemy.orm import Session
from typing import Dict
from datetime import datetime, timedelta


class FeatureService:
    """Service for calculating features for predictions"""
    
    def calculate_team_form(self, db: Session, team_name: str, as_of_date: datetime, 
                           venue: str = 'all', games: int = 5) -> Dict[str, float]:
        """
        Calculate team recent form.
        
        Args:
            db: Database session
            team_name: Team to calculate form for
            as_of_date: Calculate form as of this date
            venue: 'home', 'away', or 'all'
            games: Number of recent games
        
        Returns:
            Dictionary with form metrics
        """
        # Query recent matches from database
        from app.models.match import HistoricalMatch
        
        if venue == 'home':
            matches = db.query(HistoricalMatch).filter(
                HistoricalMatch.home_team == team_name,
                HistoricalMatch.date < as_of_date.date()
            ).order_by(HistoricalMatch.date.desc()).limit(games).all()
            
            goals_scored = [m.home_goals for m in matches]
            goals_conceded = [m.away_goals for m in matches]
            
        elif venue == 'away':
            matches = db.query(HistoricalMatch).filter(
                HistoricalMatch.away_team == team_name,
                HistoricalMatch.date < as_of_date.date()
            ).order_by(HistoricalMatch.date.desc()).limit(games).all()
            
            goals_scored = [m.away_goals for m in matches]
            goals_conceded = [m.home_goals for m in matches]
            
        else:  # all
            home_matches = db.query(HistoricalMatch).filter(
                HistoricalMatch.home_team == team_name,
                HistoricalMatch.date < as_of_date.date()
            ).order_by(HistoricalMatch.date.desc()).limit(games).all()
            
            away_matches = db.query(HistoricalMatch).filter(
                HistoricalMatch.away_team == team_name,
                HistoricalMatch.date < as_of_date.date()
            ).order_by(HistoricalMatch.date.desc()).limit(games).all()
            
            all_matches = sorted(
                home_matches + away_matches,
                key=lambda x: x.date,
                reverse=True
            )[:games]
            
            goals_scored = []
            goals_conceded = []
            
            for m in all_matches:
                if m.home_team == team_name:
                    goals_scored.append(m.home_goals)
                    goals_conceded.append(m.away_goals)
                else:
                    goals_scored.append(m.away_goals)
                    goals_conceded.append(m.home_goals)
        
        if len(goals_scored) == 0:
            return {
                'avg_scored': 0.0,
                'avg_conceded': 0.0,
                'games_played': 0
            }
        
        import numpy as np
        return {
            'avg_scored': float(np.mean(goals_scored)),
            'avg_conceded': float(np.mean(goals_conceded)),
            'games_played': len(goals_scored)
        }
    
    def calculate_h2h(self, db: Session, home_team: str, away_team: str,
                      as_of_date: datetime, games: int = 5) -> Dict[str, float]:
        """Calculate head-to-head statistics"""
        from app.models.match import HistoricalMatch
        
        matches = db.query(HistoricalMatch).filter(
            ((HistoricalMatch.home_team == home_team) & (HistoricalMatch.away_team == away_team)) |
            ((HistoricalMatch.home_team == away_team) & (HistoricalMatch.away_team == home_team)),
            HistoricalMatch.date < as_of_date.date()
        ).order_by(HistoricalMatch.date.desc()).limit(games).all()
        
        if len(matches) == 0:
            return {
                'h2h_avg_goals': 0.0,
                'h2h_games': 0
            }
        
        import numpy as np
        total_goals = [m.total_goals for m in matches]
        
        return {
            'h2h_avg_goals': float(np.mean(total_goals)),
            'h2h_games': len(matches)
        }
    
    def calculate_league_context(self, db: Session, league: str,
                                 as_of_date: datetime) -> Dict[str, float]:
        """Calculate league-wide statistics"""
        from app.models.match import HistoricalMatch
        
        # Get last 100 matches in league
        matches = db.query(HistoricalMatch).filter(
            HistoricalMatch.league == league,
            HistoricalMatch.date < as_of_date.date()
        ).order_by(HistoricalMatch.date.desc()).limit(100).all()
        
        if len(matches) == 0:
            return {'league_avg_goals': 2.5}
        
        import numpy as np
        return {
            'league_avg_goals': float(np.mean([m.total_goals for m in matches]))
        }
    
    def engineer_features_for_match(
        self,
        db: Session,
        home_team: str,
        away_team: str,
        league: str,
        match_date: datetime,
        over_25_odds: float = None,
        under_25_odds: float = None
    ) -> Dict[str, float]:
        """
        Generate all features for a match.
        Returns feature dictionary ready for model prediction.
        """
        # Home team features
        home_form = self.calculate_team_form(db, home_team, match_date, venue='all')
        home_home_form = self.calculate_team_form(db, home_team, match_date, venue='home')
        
        # Away team features
        away_form = self.calculate_team_form(db, away_team, match_date, venue='all')
        away_away_form = self.calculate_team_form(db, away_team, match_date, venue='away')
        
        # H2H
        h2h = self.calculate_h2h(db, home_team, away_team, match_date)
        
        # League context
        league_ctx = self.calculate_league_context(db, league, match_date)
        
        # Build feature dict
        features = {
            'home_avg_scored': home_form['avg_scored'],
            'home_avg_conceded': home_form['avg_conceded'],
            'home_games_played': home_form['games_played'],
            'home_home_avg_scored': home_home_form['avg_scored'],
            'home_home_avg_conceded': home_home_form['avg_conceded'],
            
            'away_avg_scored': away_form['avg_scored'],
            'away_avg_conceded': away_form['avg_conceded'],
            'away_games_played': away_form['games_played'],
            'away_away_avg_scored': away_away_form['avg_scored'],
            'away_away_avg_conceded': away_away_form['avg_conceded'],
            
            'h2h_avg_goals': h2h['h2h_avg_goals'],
            'h2h_games': h2h['h2h_games'],
            
            'league_avg_goals': league_ctx['league_avg_goals'],
            
            # Derived features
            'total_avg_scored': home_form['avg_scored'] + away_form['avg_scored'],
            'goal_diff_home': home_form['avg_scored'] - home_form['avg_conceded'],
            'goal_diff_away': away_form['avg_scored'] - away_form['avg_conceded'],
            
            # Bookmaker odds (NEW - for accuracy boost)
            'over_25_odds': over_25_odds if over_25_odds is not None else 2.0,
            'under_25_odds': under_25_odds if under_25_odds is not None else 2.0,
        }
        
        return features


# Global feature service instance
feature_service = FeatureService()
