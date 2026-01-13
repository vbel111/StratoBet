"""
API-Football Connection Test - Final Version
"""

import httpx
import json

API_KEY = "3133433ac52e0dfa04e9c36d9361f4ec"
BASE_URL = "https://v3.football.api-sports.io"

print("=" * 60)
print("API-FOOTBALL CONNECTION TEST")
print("=" * 60)
print()

headers = {"x-apisports-key": API_KEY}

try:
    # Test /status
    print("Testing /status endpoint...")
    response = httpx.get(f"{BASE_URL}/status", headers=headers, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API Connected Successfully!\n")
        print("Response structure:")
        print(json.dumps(data, indent=2))
    else:
        print(f"❌ Error: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
