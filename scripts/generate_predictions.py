"""
Generate Predictions Script
Fetches upcoming fixtures, generates predictions, and saves to database
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.fixture_service import fixture_service
from app.services.odds_service import odds_service
from app.services.prediction_service import prediction_service
from app.services.ml_service import ml_service


def generate_predictions_for_upcoming_fixtures():
    """
    Main pipeline:
    1. Fetch upcoming fixtures
    2. For each fixture:
       - Generate prediction
       - Fetch odds (if available)
       - Save prediction with odds
    """
    print("=" * 60)
    print("GENERATING PREDICTIONS FOR UPCOMING FIXTURES")
    print("=" * 60)
    print()
    
    # Check if model is loaded
    if not ml_service.is_loaded():
        print("Loading ML model...")
        success = ml_service.load_model()
        if not success:
            print("❌ Failed to load model!")
            return
    
    # Fetch upcoming fixtures
    print("1. Fetching upcoming fixtures...")
    fixtures = fixture_service.fetch_all_leagues_fixtures(days_ahead=7)
    print(f"   Found {len(fixtures)} upcoming matches\n")
    
    if not fixtures:
        print("No upcoming fixtures found!")
        return
    
    # Generate predictions
    print("2. Generating predictions...")
    db = next(get_db())
    
    predictions_generated = 0
    predictions_with_odds = 0
    
    for i, fixture in enumerate(fixtures, 1):
        try:
            print(f"\n   [{i}/{len(fixtures)}] {fixture['home_team']} vs {fixture['away_team']}")
            
            # Generate prediction
            prediction = prediction_service.generate_prediction(
                db=db,
                home_team=fixture['home_team'],
                away_team=fixture['away_team'],
                league=fixture['league'],
                match_date=datetime.fromisoformat(fixture['date'].replace('Z', '+00:00')),
                fixture_id=fixture['fixture_id']
            )
            
            print(f"      Prediction: Over 2.5 ({prediction.over_25_probability:.1%})")
            print(f"      Confidence: {prediction.confidence_level} ({prediction.confidence_score:.1%})")
            
            # Try to fetch odds
            sport_key_map = {
                'Premier League': 'soccer_epl',
                'La Liga': 'soccer_spain_la_liga',
                'Serie A': 'soccer_italy_serie_a',
                'Bundesliga': 'soccer_germany_bundesliga',
                'Ligue 1': 'soccer_france_ligue_one',
                'Champions League': 'soccer_uefa_champs_league'
            }
            
            sport_key = sport_key_map.get(fixture['league'])
            if sport_key:
                odds = odds_service.get_match_odds(
                    fixture['home_team'],
                    fixture['away_team'],
                    sport_key
                )
                
                if odds:
                    prediction.bookmaker_over_25_odds = odds.get('over_25_odds')
                    prediction.bookmaker_under_25_odds = odds.get('under_25_odds')
                    prediction.odds_updated_at = datetime.now()
                    predictions_with_odds += 1
                    print(f"      Odds: Over {odds['over_25_odds']:.2f} / Under {odds['under_25_odds']:.2f}")
            
            predictions_generated += 1
            
            # TODO: Save prediction to database
            # For now, just print
            
        except Exception as e:
            print(f"      ❌ Error: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Fixtures processed: {len(fixtures)}")
    print(f"Predictions generated: {predictions_generated}")
    print(f"Predictions with odds: {predictions_with_odds}")
    print(f"Success rate: {predictions_generated/len(fixtures)*100:.1f}%")
    print("=" * 60 + "\n")
    
    db.close()


if __name__ == '__main__':
    generate_predictions_for_upcoming_fixtures()
