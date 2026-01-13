"""
Debug Fixture Fetching
Check what's being returned from API-Football
"""

import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

import httpx
from datetime import datetime, timedelta
from app.core.config import settings

API_KEY = settings.API_FOOTBALL_KEY
BASE_URL = "https://v3.football.api-sports.io"
headers = {'x-apisports-key': API_KEY}

print("=" * 70)
print("DEBUGGING FIXTURE FETCHING")
print("=" * 70)
print()

# Test 1: Check current season
print("1. Checking current season for Premier League...")
response = httpx.get(
    f"{BASE_URL}/leagues",
    headers=headers,
    params={'id': 39, 'current': True},
    timeout=10
)

if response.status_code == 200:
    data = response.json()
    if data['response']:
        league_data = data['response'][0]
        seasons = league_data['seasons']
        current_season = [s for s in seasons if s.get('current')]
        if current_season:
            print(f"   Current season: {current_season[0]['year']}")
            season_year = current_season[0]['year']
        else:
            print(f"   No current season found. Latest: {seasons[-1]['year']}")
            season_year = seasons[-1]['year']
    else:
        print("   No league data returned")
        season_year = 2024
else:
    print(f"   Error: {response.status_code}")
    season_year = 2024

print()

# Test 2: Fetch fixtures with correct season
print("2. Fetching Premier League fixtures...")
today = datetime.now()
end_date = today + timedelta(days=14)

print(f"   Date range: {today.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
print(f"   Season: {season_year}")
print()

params = {
    'league': 39,  # Premier League
    'season': season_year,
    'from': today.strftime('%Y-%m-%d'),
    'to': end_date.strftime('%Y-%m-%d'),
    'timezone': 'UTC'
}

response = httpx.get(
    f"{BASE_URL}/fixtures",
    headers=headers,
    params=params,
    timeout=10
)

print(f"   Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    fixtures = data.get('response', [])
    
    print(f"   ✅ Found {len(fixtures)} fixtures!")
    print()
    
    if fixtures:
        print("   First 5 matches:")
        for i, fixture in enumerate(fixtures[:5], 1):
            home = fixture['teams']['home']['name']
            away = fixture['teams']['away']['name']
            date = fixture['fixture']['date']
            status = fixture['fixture']['status']['short']
            
            print(f"   {i}. {home} vs {away}")
            print(f"      Date: {date}")
            print(f"      Status: {status}")
            print()
    else:
        print("   ⚠️  No fixtures in this date range")
        print()
        print("   Trying without date filter (next 10 upcoming)...")
        
        # Try getting next fixtures without date filter
        response2 = httpx.get(
            f"{BASE_URL}/fixtures",
            headers=headers,
            params={'league': 39, 'season': season_year, 'next': 10},
            timeout=10
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            fixtures2 = data2.get('response', [])
            
            if fixtures2:
                print(f"   ✅ Found {len(fixtures2)} upcoming fixtures:")
                for i, fixture in enumerate(fixtures2[:5], 1):
                    home = fixture['teams']['home']['name']
                    away = fixture['teams']['away']['name']
                    date = fixture['fixture']['date']
                    
                    print(f"   {i}. {home} vs {away} - {date}")
else:
    print(f"   ❌ Error: {response.text[:200]}")

print("\n" + "=" * 70)
