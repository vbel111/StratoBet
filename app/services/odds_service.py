"""
Odds Fetching Service
Fetches Over/Under 2.5 odds from The Odds API
"""

import httpx
from typing import Dict, Optional, List
from app.core.config import settings


class OddsFetchingService:
    """Service for fetching odds from The Odds API"""
    
    def __init__(self):
        self.base_url = settings.ODDS_API_BASE_URL
        self.api_key = settings.ODDS_API_KEY
    
    def fetch_league_odds(self, sport_key: str = 'soccer_epl') -> List[Dict]:
        """
        Fetch Over/Under odds for a league.
        
        Args:
            sport_key: Sport key from Odds API (soccer_epl, soccer_spain_la_liga, etc.)
        
        Returns:
            List of matches with odds
        """
        params = {
            'apiKey': self.api_key,
            'regions': 'uk',
            'markets': 'totals',  # Over/Under markets
            'oddsFormat': 'decimal'
        }
        
        try:
            response = httpx.get(
                f"{self.base_url}/sports/{sport_key}/odds",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error fetching odds for {sport_key}: {e}")
            return []
    
    def get_match_odds(self, home_team: str, away_team: str, sport_key: str = 'soccer_epl') -> Optional[Dict]:
        """
        Get Over/Under 2.5 odds for a specific match.
        
        Args:
            home_team: Home team name
            away_team: Away team name
            sport_key: Sport key
        
        Returns:
            Dictionary with over_25_odds and under_25_odds, or None
        """
        fixtures = self.fetch_league_odds(sport_key)
        
        # Find matching fixture
        for fixture in fixtures:
            if (self._match_team(fixture['home_team'], home_team) and 
                self._match_team(fixture['away_team'], away_team)):
                
                # Extract Over/Under 2.5 odds
                if fixture.get('bookmakers'):
                    bookmaker = fixture['bookmakers'][0]  # Use first bookmaker
                    
                    for market in bookmaker.get('markets', []):
                        if market['key'] == 'totals':
                            odds = {}
                            for outcome in market['outcomes']:
                                if 'Over' in outcome['name']:
                                    odds['over_25_odds'] = outcome['price']
                                    odds['over_25_point'] = outcome.get('point', 2.5)
                                elif 'Under' in outcome['name']:
                                    odds['under_25_odds'] = outcome['price']
                                    odds['under_25_point'] = outcome.get('point', 2.5)
                            
                            if odds:
                                odds['bookmaker'] = bookmaker['title']
                                odds['last_update'] = bookmaker.get('last_update')
                                return odds
        
        return None
    
    def _match_team(self, api_name: str, our_name: str) -> bool:
        """Fuzzy match team names (case-insensitive, remove spaces)"""
        api_clean = api_name.lower().replace(' ', '').replace('-', '')
        our_clean = our_name.lower().replace(' ', '').replace('-', '')
        return api_clean in our_clean or our_clean in api_clean
    
    def fetch_all_leagues_odds(self) -> Dict[str, List]:
        """Fetch odds for all supported leagues"""
        
        sport_keys = {
            'soccer_epl': 'Premier League',
            'soccer_spain_la_liga': 'La Liga',
            'soccer_italy_serie_a': 'Serie A',
            'soccer_germany_bundesliga': 'Bundesliga',
            'soccer_france_ligue_one': 'Ligue 1',
            'soccer_uefa_champs_league': 'Champions League'
        }
        
        all_odds = {}
        
        for sport_key, league_name in sport_keys.items():
            print(f"Fetching {league_name} odds...")
            try:
                odds = self.fetch_league_odds(sport_key)
                all_odds[league_name] = odds
                print(f"  Found odds for {len(odds)} matches")
            except Exception as e:
                print(f"  Error: {e}")
                all_odds[league_name] = []
        
        return all_odds


# Global instance
odds_service = OddsFetchingService()
