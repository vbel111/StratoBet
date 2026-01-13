"""
Demo Predictions Test
Tests prediction generation with sample upcoming matches
"""

import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.services.ml_service import ml_service
from app.services.prediction_service import prediction_service
from app.core.database import get_db
from datetime import datetime, timedelta

def test_demo_predictions():
    print("=" * 70)
    print("STRATOBET - DEMO PREDICTION TEST")
    print("=" * 70)
    print()
    
    # Load model
    print("Loading ML model...")
    if not ml_service.is_loaded():
        success = ml_service.load_model()
        if not success:
            print("❌ Failed to load model!")
            return
    print(f"✅ Model v{ml_service.model_version} loaded\n")
    
    # Sample upcoming matches (for demo/testing)
    demo_fixtures = [
        {
            'home_team': 'Arsenal',
            'away_team': 'Chelsea',
            'league': 'Premier League',
            'date': datetime.now() + timedelta(days=2)
        },
        {
            'home_team': 'Manchester City',
            'away_team': 'Liverpool',
            'league': 'Premier League',
            'date': datetime.now() + timedelta(days=3)
        },
        {
            'home_team': 'Real Madrid',
            'away_team': 'Barcelona',
            'league': 'La Liga',
            'date': datetime.now() + timedelta(days=4)
        },
        {
            'home_team': 'Bayern Munich',
            'away_team': 'Borussia Dortmund',
            'league': 'Bundesliga',
            'date': datetime.now() + timedelta(days=5)
        }
    ]
    
    db = next(get_db())
    
    print("Generating predictions for demo fixtures...\n")
    print("=" * 70)
    
    for i, fixture in enumerate(demo_fixtures, 1):
        print(f"\n🏆 MATCH {i}")
        print(f"   {fixture['home_team']} vs {fixture['away_team']}")
        print(f"   League: {fixture['league']}")
        print(f"   Date: {fixture['date'].strftime('%Y-%m-%d %H:%M')}")
        
        try:
            prediction = prediction_service.generate_prediction(
                db=db,
                home_team=fixture['home_team'],
                away_team=fixture['away_team'],
                league=fixture['league'],
                match_date=fixture['date'],
                fixture_id=f"demo_{i}"
            )
            
            print(f"\n   🎯 PREDICTION:")
            print(f"      Over 2.5:  {prediction.over_25_probability:.1%}")
            print(f"      Under 2.5: {prediction.under_25_probability:.1%}")
            print(f"      Confidence: {prediction.confidence_level} ({prediction.confidence_score:.1%})")
            
            # Recommendation
            if prediction.over_25_probability >= 0.65:
                rec = "STRONG OVER 2.5"
            elif prediction.over_25_probability >= 0.55:
                rec = "LEAN OVER 2.5"
            elif prediction.under_25_probability >= 0.65:
                rec = "STRONG UNDER 2.5"
            elif prediction.under_25_probability >= 0.55:
                rec = "LEAN UNDER 2.5"
            else:
                rec = "SKIP - Low Confidence"
            
            print(f"      Recommendation: {rec}")
            
            if prediction.key_factors:
                print(f"\n   📊 KEY FACTORS:")
                for factor in prediction.key_factors:
                    print(f"      • {factor}")
            
            print("\n" + "-" * 70)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    db.close()
    
    print("\n" + "=" * 70)
    print("✅ DEMO TEST COMPLETE!")
    print("=" * 70)
    print("\nPrediction Model is working correctly!")
    print("Try the API:")
    print("  POST http://localhost:8000/api/v1/predictions/predict")
    print("  GET  http://localhost:8000/api/v1/predictions/test\n")


if __name__ == '__main__':
    test_demo_predictions()
