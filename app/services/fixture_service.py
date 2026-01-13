"""
Fixture Fetching Service
Fetches upcoming fixtures from The Odds API (since API-Football free plan doesn't support 2025)
"""

import httpx
from datetime import datetime
from typing import List, Dict
from app.core.config import settings


class FixtureFetchingService:
    """Service for fetching upcoming fixtures from The Odds API"""
    
    def __init__(self):
        self.base_url = settings.ODDS_API_BASE_URL
        self.api_key = settings.ODDS_API_KEY
    
    def fetch_upcoming_fixtures(self, sport_key: str = 'soccer_epl') -> List[Dict]:
        """
        Fetch upcoming fixtures for a league from The Odds API.
        
        Args:
            sport_key: Sport key (soccer_epl, soccer_spain_la_liga, etc.)
        
        Returns:
            List of fixture dictionaries
        """
        params = {
            'apiKey': self.api_key,
            'regions': 'uk',
            'markets': 'totals',  # We need this anyway for odds
            'oddsFormat': 'decimal'
        }
        
        try:
            response = httpx.get(
                f"{self.base_url}/sports/{sport_key}/odds",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            fixtures_data = response.json()
            
            # Parse and clean fixtures
            cleaned_fixtures = []
            for fixture in fixtures_data:
                cleaned = {
                    'fixture_id': fixture['id'],
                    'date': fixture['commence_time'],
                    'league': self._get_league_name(sport_key),
                    'league_id': sport_key,
                    'home_team': fixture['home_team'],
                    'away_team': fixture['away_team'],
                    'venue': None,
                    'status': 'NS'  # Not Started
                }
                cleaned_fixtures.append(cleaned)
            
            return cleaned_fixtures
            
        except Exception as e:
            print(f"Error fetching fixtures for {sport_key}: {e}")
            return []
    
    def fetch_all_leagues_fixtures(self, days_ahead: int = 7) -> List[Dict]:
        """Fetch fixtures for all supported leagues"""
        
        # Sport keys from The Odds API
        sport_keys = {
            'soccer_epl': 'Premier League',
            'soccer_spain_la_liga': 'La Liga',
            'soccer_italy_serie_a': 'Serie A',
            'soccer_germany_bundesliga': 'Bundesliga',
            'soccer_france_ligue_one': 'Ligue 1',
            'soccer_uefa_champs_league': 'Champions League'
        }
        
        all_fixtures = []
        
        for sport_key, league_name in sport_keys.items():
            print(f"Fetching {league_name} fixtures...")
            fixtures = self.fetch_upcoming_fixtures(sport_key)
            all_fixtures.extend(fixtures)
            print(f"  Found {len(fixtures)} upcoming matches")
        
        return all_fixtures
    
    def _get_league_name(self, sport_key: str) -> str:
        """Convert sport key to league name"""
        mapping = {
            'soccer_epl': 'Premier League',
            'soccer_spain_la_liga': 'La Liga',
            'soccer_italy_serie_a': 'Serie A',
            'soccer_germany_bundesliga': 'Bundesliga',
            'soccer_france_ligue_one': 'Ligue 1',
            'soccer_uefa_champs_league': 'Champions League'
        }
        return mapping.get(sport_key, sport_key)


# Global instance
fixture_service = FixtureFetchingService()
