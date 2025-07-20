#!/usr/bin/env python3
"""
Test script for the Autonomous RC Car MCP Server
Tests all movement functions and photo analysis capabilities
"""

import requests
import time
import json

# Test configuration
BASE_URL = "http://10.33.35.1:5000"  # Flask server
MCP_SERVER_URL = "http://localhost:8000"  # MCP server (if running as HTTP)


def test_flask_connection():
    """Test connection to Flask server"""
    print("Testing Flask server connection...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"Flask server status: {response.status_code}")
        return True
    except Exception as e:
        print(f"Flask server connection failed: {e}")
        return False


def test_movement_endpoints():
    """Test all movement endpoints"""
    print("\nTesting movement endpoints...")

    movements = [
        ("forward", "Moving forward"),
        ("backward", "Moving backward"),
        ("left", "Turning left"),
        ("right", "Turning right"),
        ("stop", "Stopping"),
    ]

    for endpoint, description in movements:
        print(f"\n{description}...")
        try:
            response = requests.post(f"{BASE_URL}/{endpoint}", timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")


def test_photo_endpoint():
    """Test photo capture and analysis"""
    print("\nTesting photo capture and analysis...")
    try:
        payload = {
            "goal": "Find a red ball on the ground",
            "laptop_ip": "10.33.49.88",
            "laptop_port": 8000,
        }

        response = requests.post(f"{BASE_URL}/photo", json=payload, timeout=15)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

    except Exception as e:
        print(f"Error: {e}")


def test_movement_sequence():
    """Test a sequence of movements"""
    print("\nTesting movement sequence...")

    sequence = [
        ("forward", 0.3),
        ("stop", 0),
        ("left", 0.3),
        ("stop", 0),
        ("right", 0.3),
        ("stop", 0),
        ("backward", 0.3),
        ("stop", 0),
    ]

    for movement, duration in sequence:
        print(f"\nExecuting: {movement} for {duration}s")
        try:
            response = requests.post(f"{BASE_URL}/{movement}", timeout=10)
            print(f"Status: {response.status_code}")
            if duration > 0:
                time.sleep(duration)
        except Exception as e:
            print(f"Error: {e}")


def test_autonomous_navigation_simulation():
    """Simulate autonomous navigation behavior"""
    print("\nSimulating autonomous navigation...")

    # Simulate the behavior the MCP server would have
    goal = "Find a keychain object on the ground"

    print(f"Goal: {goal}")
    print("Starting autonomous navigation simulation...")

    # Step 1: Take initial photo
    print("\nStep 1: Taking initial photo...")
    try:
        payload = {"goal": goal, "laptop_ip": "10.33.49.88", "laptop_port": 8000}
        response = requests.post(f"{BASE_URL}/photo", json=payload, timeout=15)
        print(f"Photo analysis: {response.json()}")
    except Exception as e:
        print(f"Photo error: {e}")

    # Step 2: Simulate movement based on analysis
    print("\nStep 2: Simulating movement...")
    movements = [
        ("forward", 0.3),
        ("left", 0.2),
        ("forward", 0.3),
        ("right", 0.2),
        ("forward", 0.3),
    ]

    for movement, duration in movements:
        print(f"Moving: {movement} for {duration}s")
        try:
            response = requests.post(f"{BASE_URL}/{movement}", timeout=10)
            time.sleep(duration)
        except Exception as e:
            print(f"Movement error: {e}")

    # Step 3: Take final photo
    print("\nStep 3: Taking final photo...")
    try:
        response = requests.post(f"{BASE_URL}/photo", json=payload, timeout=15)
        print(f"Final analysis: {response.json()}")
    except Exception as e:
        print(f"Final photo error: {e}")


def test_duration_control():
    """Test different duration values"""
    print("\nTesting duration control...")

    durations = [0.1, 0.2, 0.3, 0.5, 0.8]

    for duration in durations:
        print(f"\nTesting forward movement with {duration}s duration...")
        try:
            # Simulate multiple requests for duration control
            num_requests = max(1, int(duration / 0.3))
            print(f"Making {num_requests} requests to simulate {duration}s")

            for i in range(num_requests):
                response = requests.post(f"{BASE_URL}/forward", timeout=10)
                print(f"Request {i+1}: {response.status_code}")
                if i < num_requests - 1:
                    time.sleep(0.3)

        except Exception as e:
            print(f"Error: {e}")


def main():
    """Run all tests"""
    print("Autonomous RC Car MCP Server Test Suite")
    print("=" * 50)

    # Test 1: Flask connection
    if not test_flask_connection():
        print("Flask server not available. Exiting.")
        return

    # Test 2: Individual endpoints
    test_movement_endpoints()

    # Test 3: Photo endpoint
    test_photo_endpoint()

    # Test 4: Movement sequence
    test_movement_sequence()

    # Test 5: Duration control
    test_duration_control()

    # Test 6: Autonomous navigation simulation
    test_autonomous_navigation_simulation()

    print("\n" + "=" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    main()
