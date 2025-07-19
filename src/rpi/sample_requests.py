import requests
import time

# Base URL for the motor control API
BASE_URL = "http://10.33.35.1:5000"


def test_forward():
    """Test moving forward"""
    print("Testing forward movement...")
    try:
        response = requests.post(f"{BASE_URL}/forward")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)


def test_backward():
    """Test moving backward"""
    print("Testing backward movement...")
    try:
        response = requests.post(f"{BASE_URL}/backward")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)


def test_left():
    """Test turning left"""
    print("Testing left turn...")
    try:
        response = requests.post(f"{BASE_URL}/left")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)


def test_right():
    """Test turning right"""
    print("Testing right turn...")
    try:
        response = requests.post(f"{BASE_URL}/right")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)


def test_stop():
    """Test stopping motors"""
    print("Testing stop...")
    try:
        response = requests.post(f"{BASE_URL}/stop")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)


def test_all_movements():
    """Test all movement commands in sequence"""
    print("Testing all movement commands...")
    print("=" * 50)

    # Test forward
    test_forward()
    time.sleep(2)  # Wait between movements

    # Test backward
    test_backward()
    time.sleep(2)

    # Test left turn
    test_left()
    time.sleep(2)

    # Test right turn
    test_right()
    time.sleep(2)

    # Test stop
    test_stop()

    print("All tests completed!")


def test_individual_endpoints():
    """Test each endpoint individually"""
    print("Individual endpoint tests:")
    print("=" * 50)

    test_forward()
    test_backward()
    test_left()
    test_right()
    test_stop()


if __name__ == "__main__":
    print("Motor Control API Test Script")
    print(f"Target URL: {BASE_URL}")
    print("=" * 50)

    # Test individual endpoints
    test_individual_endpoints()

    print("\n" + "=" * 50)
    print("Testing movement sequence...")
    test_all_movements()
