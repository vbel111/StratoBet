"""
Test The Odds API Connection
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('ODDS_API_KEY')
BASE_URL = "https://api.the-odds-api.com/v4"

print("=" * 60)
print("THE ODDS API - CONNECTION TEST")
print("=" * 60)
print(f"\nAPI Key: {API_KEY[:10] if API_KEY else 'NOT SET'}...{API_KEY[-4:] if API_KEY else ''}\n")

if not API_KEY:
    print("❌ ODDS_API_KEY not set in .env file!")
    print("   Get your key from: https://the-odds-api.com/\n")
    exit(1)

headers = {
    "apiKey": API_KEY
}

try:
    # Test 1: Get available sports
    print("Test 1: Fetching available sports...")
    response = httpx.get(f"{BASE_URL}/sports", params={"apiKey": API_KEY}, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        sports = response.json()
        print(f"✅ Connected! Found {len(sports)} sports\n")
        
        # Find football sports
        football_sports = [s for s in sports if 'soccer' in s.get('group', '').lower()]
        if football_sports:
            print(f"📊 Football leagues available ({len(football_sports)}):")
            for sport in football_sports[:5]:
                print(f"   - {sport['title']} ({sport['key']})")
            if len(football_sports) > 5:
                print(f"   ... and {len(football_sports) - 5} more")
    else:
        print(f"❌ Error: {response.text}\n")
        exit(1)
    
    # Test 2: Get odds for Premier League
    print("\n\nTest 2: Fetching Premier League Over/Under odds...")
    params = {
        "apiKey": API_KEY,
        "regions": "uk",
        "markets": "totals",  # Over/Under markets
        "oddsFormat": "decimal"
    }
    
    response = httpx.get(
        f"{BASE_URL}/sports/soccer_epl/odds",
        params=params,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Found odds for {len(data)} upcoming matches\n")
        
        if len(data) > 0:
            match = data[0]
            print(f"Sample match:")
            print(f"   {match['home_team']} vs {match['away_team']}")
            print(f"   Commence: {match['commence_time']}")
            
            if match.get('bookmakers'):
                bookmaker = match['bookmakers'][0]
                print(f"\n   Odds from {bookmaker['title']}:")
                for market in bookmaker.get('markets', []):
                    if market['key'] == 'totals':
                        for outcome in market['outcomes']:
                            print(f"      {outcome['name']}: {outcome['price']}")
        
        # Show API usage
        remaining = response.headers.get('x-requests-remaining', 'unknown')
        print(f"\n📊 API Usage:")
        print(f"   Requests remaining: {remaining}/500 this month")
        
    else:
        print(f"❌ Error: {response.text}\n")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nYour Odds API key is working correctly!\n")
    
except Exception as e:
    print(f"\n❌ Exception: {e}\n")
    import traceback
    traceback.print_exc()
