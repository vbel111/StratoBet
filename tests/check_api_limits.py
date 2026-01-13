"""
Check API Limitations
Verify what both APIs actually support
"""

import httpx
from datetime import datetime

print("=" * 70)
print("API LIMITATIONS CHECK")
print("=" * 70)
print()

# API-Football Check
print("1. API-FOOTBALL CHECK")
print("-" * 70)

api_football_key = "3133433ac52e0dfa04e9c36d9361f4ec"
headers = {'x-apisports-key': api_football_key}

print("\nTesting season 2024:")
r = httpx.get(
    'https://v3.football.api-sports.io/fixtures',
    headers=headers,
    params={'league': 39, 'season': 2024, 'next': 5},
    timeout=10
)
data = r.json()
print(f"  Status: {r.status_code}")
print(f"  Results: {data.get('results', 0)}")
if 'errors' in data and data['errors']:
    print(f"  Errors: {data['errors']}")

print("\nTesting without season (should auto-detect):")
r2 = httpx.get(
    'https://v3.football.api-sports.io/fixtures',
    headers=headers,
    params={'league': 39, 'next': 10},
    timeout=10
)
data2 = r2.json()
print(f"  Status: {r2.status_code}")
print(f"  Results: {data2.get('results', 0)}")
if 'errors' in data2 and data2['errors']:
    print(f"  Errors: {data2['errors']}")
    
if data2.get('results', 0) > 0:
    print("\n  Sample fixtures:")
    for f in data2['response'][:3]:
        print(f"    - {f['teams']['home']['name']} vs {f['teams']['away']['name']}")
        print(f"      Date: {f['fixture']['date']}")
        print(f"      Status: {f['fixture']['status']['short']}")

print("\n" + "=" * 70)
print()

# Odds API Check  
print("2. THE ODDS API CHECK")
print("-" * 70)

odds_key = "31c30c97b6fe5d0811864f977fa9a7de"

print("\nChecking available sports:")
r3 = httpx.get(
    'https://api.the-odds-api.com/v4/sports',
    params={'apiKey': odds_key},
    timeout=10
)

if r3.status_code == 200:
    sports = r3.json()
    soccer_sports = [s for s in sports if 'soccer' in s.get('group', '').lower()]
    print(f"  ✅ Found {len(soccer_sports)} football leagues")
    print("\n  Available leagues:")
    for sport in soccer_sports[:6]:
        print(f"    - {sport['title']} ({sport['key']})")
else:
    print(f"  ❌ Error: {r3.status_code}")

print("\nChecking Premier League odds:")
r4 = httpx.get(
    'https://api.the-odds-api.com/v4/sports/soccer_epl/odds',
    params={'apiKey': odds_key, 'regions': 'uk', 'markets': 'totals'},
    timeout=10
)

if r4.status_code ==200:
    odds_data = r4.json()
    print(f"  ✅ Found odds for {len(odds_data)} matches")
    if len(odds_data) > 0:
        print("\n  Sample matches:")
        for match in odds_data[:3]:
            print(f"    - {match['home_team']} vs {match['away_team']}")
            print(f"      Start: {match['commence_time']}")
else:
    print(f"  ❌ Error: {r4.status_code}")

print("\n" + "=" * 70)
print("\n📊 SUMMARY:")
print("   API-Football: Free plan = Historical data only (2022-2024)")
print("   The Odds API: Works for current/upcoming matches ✅")
print("\n💡 SOLUTION:")
print("   Use The Odds API to get upcoming fixtures + odds")
print("   It provides everything we need!")
print("=" * 70 + "\n")
