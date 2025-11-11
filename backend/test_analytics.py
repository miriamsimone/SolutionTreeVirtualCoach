"""
Test analytics endpoint with sample data.
"""
import requests
import json

# You need to replace this with a real Firebase token from your frontend
# To get a token:
# 1. Open browser console on your frontend
# 2. Run: await firebase.auth().currentUser.getIdToken()
# 3. Copy the token and paste it below

FIREBASE_TOKEN = "YOUR_FIREBASE_TOKEN_HERE"
BASE_URL = "http://localhost:8000"


def test_analytics_endpoint():
    """Test the analytics endpoint with authentication."""
    print("Testing Analytics Endpoint")
    print("=" * 60)

    if FIREBASE_TOKEN == "YOUR_FIREBASE_TOKEN_HERE":
        print("⚠️  Please set FIREBASE_TOKEN in test_analytics.py")
        print("\nTo get a token:")
        print("1. Open your frontend in a browser")
        print("2. Open browser console")
        print("3. Run: await firebase.auth().currentUser.getIdToken()")
        print("4. Copy the token and paste it in test_analytics.py")
        print("\nOr test via curl:")
        print('  curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/analytics')
        return

    headers = {
        "Authorization": f"Bearer {FIREBASE_TOKEN}"
    }

    # Test full analytics
    print("\n1. Testing GET /api/analytics")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics", headers=headers)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success!")
            print(f"\n   Analytics Data:")
            print(f"   - Total conversations: {data.get('total_conversations')}")
            print(f"   - Active users: {data.get('active_users')}")
            print(f"   - Average rating: {data.get('avg_rating')}")
            print(f"   - Sessions this week: {data.get('sessions_this_week')}")
            print(f"   - Total feedback: {data.get('total_feedback_count')}")

            print(f"\n   Agent Usage:")
            for agent, percentage in data.get('agent_usage', {}).items():
                count = data.get('agent_usage_counts', {}).get(agent, 0)
                print(f"   - {agent}: {percentage}% ({count} sessions)")

            print(f"\n   Recent Activity (last {len(data.get('recent_activity', []))} days):")
            for activity in data.get('recent_activity', [])[-3:]:
                print(f"   - {activity['date']}: {activity['sessions']} sessions")

            if data.get('top_rated_sessions'):
                print(f"\n   Top Rated Sessions:")
                for session in data.get('top_rated_sessions', [])[:3]:
                    print(f"   - Session {session['session_id'][:8]}...: {session['avg_rating']} stars ({session['rating_count']} ratings)")
        else:
            print(f"   ✗ Error: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"   ✗ Request failed: {e}")

    # Test summary endpoint
    print("\n2. Testing GET /api/analytics/summary")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/summary", headers=headers)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success!")
            print(f"   Summary: {json.dumps(data, indent=2)}")
        else:
            print(f"   ✗ Error: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Request failed: {e}")

    # Test with custom days parameter
    print("\n3. Testing GET /api/analytics?days=30")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics?days=30", headers=headers)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success!")
            print(f"   Recent activity entries: {len(data.get('recent_activity', []))}")
        else:
            print(f"   ✗ Error: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Request failed: {e}")

    print("\n" + "=" * 60)
    print("Test complete!")


if __name__ == "__main__":
    test_analytics_endpoint()
