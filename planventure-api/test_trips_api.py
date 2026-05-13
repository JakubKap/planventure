#!/usr/bin/env python3
"""
Test script for Trip API endpoints.

This script demonstrates how to test the trip creation endpoint
using the example JSON files.
"""

import json
import requests
from pathlib import Path

# Configuration
API_BASE_URL = "http://127.0.0.1:5000"
EXAMPLE_FILES = [
    "example_trip_create.json",
    "example_trip_minimal.json",
    "example_trip_coordinates.json"
]

def test_trip_creation(jwt_token: str):
    """Test trip creation with example JSON files."""

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    print("🧪 Testing Trip Creation Endpoints")
    print("=" * 50)

    for example_file in EXAMPLE_FILES:
        file_path = Path(__file__).parent / example_file

        if not file_path.exists():
            print(f"❌ Example file not found: {example_file}")
            continue

        print(f"\n📄 Testing with {example_file}:")

        try:
            # Load example data
            with open(file_path, 'r') as f:
                trip_data = json.load(f)

            print(f"   Destination: {trip_data['destination']}")
            print(f"   Dates: {trip_data['start_date']} → {trip_data['end_date']}")

            # Make API request
            response = requests.post(
                f"{API_BASE_URL}/trips",
                json=trip_data,
                headers=headers
            )

            if response.status_code == 201:
                result = response.json()
                print("   ✅ Success! Trip created with ID:", result['trip']['id'])
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                try:
                    error = response.json()
                    print(f"   Error: {error.get('error', 'Unknown error')}")
                except:
                    print(f"   Response: {response.text}")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

    print("\n" + "=" * 50)
    print("🏁 Trip creation tests completed!")


def get_user_trips(jwt_token: str):
    """Get all trips for the authenticated user."""

    headers = {"Authorization": f"Bearer {jwt_token}"}

    try:
        response = requests.get(f"{API_BASE_URL}/trips", headers=headers)

        if response.status_code == 200:
            result = response.json()
            trips = result.get('trips', [])
            print(f"\n📋 Current trips: {len(trips)}")
            for trip in trips:
                print(f"   • {trip['destination']} ({trip['start_date'][:10]} → {trip['end_date'][:10]})")
        else:
            print(f"❌ Failed to get trips: {response.status_code}")

    except Exception as e:
        print(f"❌ Error getting trips: {str(e)}")


if __name__ == "__main__":
    # You'll need to replace this with your actual JWT token
    # Get it from /auth/login endpoint after registering
    JWT_TOKEN = "YOUR_JWT_TOKEN_HERE"

    if JWT_TOKEN == "YOUR_JWT_TOKEN_HERE":
        print("❌ Please replace JWT_TOKEN with your actual JWT token!")
        print("   1. Register: POST /auth/register")
        print("   2. Login: POST /auth/login")
        print("   3. Copy the access_token from login response")
        exit(1)

    # Test trip creation
    test_trip_creation(JWT_TOKEN)

    # Show current trips
    get_user_trips(JWT_TOKEN)