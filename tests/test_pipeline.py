"""
Test Real-Time Prediction Pipeline
Generates predictions for upcoming fixtures with odds
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

print("Starting prediction pipeline test...\n")

# Now import after path is set
from app.services.fixture_service import fixture_service
from app.services.odds_service import odds_service
from app.services.ml_service import ml_service
from app.services.prediction_service import prediction_service
from app.core.database import get_db
from datetime import datetime

def test_pipeline():
    print("=" * 70)
    print("STRATOBET - REAL-TIME PREDICTION PIPELINE TEST")
    print("=" * 70)
    print()
    
    # Step 1: Load ML Model
    print("1. Loading ML Model...")
    if not ml_service.is_loaded():
        success = ml_service.load_model()
        if not success:
            print("   ❌ Failed to load model!")
            return
    print(f"   ✅ Model v{ml_service.model_version} loaded\n")
    
    # Step 2: Fetch Fixtures
    print("2. Fetching Upcoming Fixtures...")
    fixtures = fixture_service.fetch_all_leagues_fixtures(days_ahead=3)
    print(f"   ✅ Found {len(fixtures)} upcoming matches\n")
    
    if not fixtures:
        print("   No upcoming fixtures found. This might be off-season.")
        return
    
    # Step 3: Generate Predictions (first 3 matches only for testing)
    print("3. Generating Predictions with Odds...\n")
    
    db = next(get_db())
    
    for i, fixture in enumerate(fixtures[:3], 1):
        print(f"   Match {i}: {fixture['home_team']} vs {fixture['away_team']}")
        print(f"   League: {fixture['league']}")
        print(f"   Date: {fixture['date']}")
        
        try:
            # Generate prediction
            prediction = prediction_service.generate_prediction(
                db=db,
                home_team=fixture['home_team'],
                away_team=fixture['away_team'],
                league=fixture['league'],
                match_date=datetime.fromisoformat(fixture['date'].replace('Z', '+00:00')),
                fixture_id=fixture['fixture_id']
            )
            
            print(f"\n   🎯 PREDICTION:")
            print(f"      Over 2.5:  {prediction.over_25_probability:.1%}")
            print(f"      Under 2.5: {prediction.under_25_probability:.1%}")
            print(f"      Confidence: {prediction.confidence_level} ({prediction.confidence_score:.1%})")
            
            if prediction.key_factors:
                print(f"\n   📊 KEY FACTORS:")
                for factor in prediction.key_factors[:3]:
                    print(f"      • {factor}")
            
            # Try to fetch odds
            sport_key_map = {
                'Premier League': 'soccer_epl',
                'La Liga': 'soccer_spain_la_liga',
                'Serie A': 'soccer_italy_serie_a',
                'Bundesliga': 'soccer_germany_bundesliga',
                'Ligue 1': 'soccer_france_ligue_one',
            }
            
            sport_key = sport_key_map.get(fixture['league'])
            if sport_key:
                print(f"\n   💰 FETCHING ODDS...")
                odds = odds_service.get_match_odds(
                    fixture['home_team'],
                    fixture['away_team'],
                    sport_key
                )
                
                if odds:
                    print(f"      Over 2.5:  {odds['over_25_odds']:.2f}")
                    print(f"      Under 2.5: {odds['under_25_odds']:.2f}")
                    print(f"      Bookmaker: {odds['bookmaker']}")
                else:
                    print(f"      ⚠️  No odds available yet")
            
            print("\n" + "-" * 70 + "\n")
            
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            import traceback
            traceback.print_exc()
            print()
    
    db.close()
    
    print("=" * 70)
    print("✅ PIPELINE TEST COMPLETE!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Check http://localhost:8000/api/v1/fixtures/upcoming")
    print("  2. Test prediction endpoint")
    print("  3. Set up automated scheduler\n")


if __name__ == '__main__':
    test_pipeline()
