"""
Simple test of improved model with demo prediction
"""

import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from app.services.ml_service import ml_service
from app.services.prediction_service import prediction_service
from app.core.database import get_db
from datetime import datetime, timedelta

print("=" * 70)
print("🎯 TESTING IMPROVED MODEL WITH ODDS")
print("=" * 70)
print()

# Test 1: Load model
print("1. Loading Model...")
if not ml_service.is_loaded():
    success = ml_service.load_model()
    if not success:
        print("   ❌ Failed!")
        exit(1)

print(f"   ✅ Model loaded: v{ml_service.model_version}")
print()

# Test 2: Generate a prediction
print("2. Generating Test Prediction...")
print("   Match: Arsenal vs Chelsea")
print("   Odds: Over 2.5 = 1.85, Under 2.5 = 2.05")
print()

db = next(get_db())

try:
    prediction = prediction_service.generate_prediction(
        db=db,
        home_team="Arsenal",
        away_team="Chelsea",
        league="Premier League",
        match_date=datetime.now() + timedelta(days=2),
        fixture_id="test_1",
        over_25_odds=1.85,
        under_25_odds=2.05
    )
    
    print("📊 RESULTS:")
    print(f"   Over 2.5:  {prediction.over_25_probability:.1%}")
    print(f"   Under 2.5: {prediction.under_25_probability:.1%}")
    print(f"   Confidence: {prediction.confidence_level} ({prediction.confidence_score:.1%})")
    
    if prediction.key_factors:
        print(f"\n📌 KEY FACTORS:")
        for factor in prediction.key_factors:
            print(f"   • {factor}")
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! Model working with odds!")
    print("=" * 70)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    db.close()
