#!/usr/bin/env python3
"""
Example autonomous navigation workflow using the MCP server
This demonstrates how an LLM would control the RC car to find a target object
"""

import requests
import time
import json

# Configuration
BASE_URL = "http://10.33.35.1:5000"


def simulate_mcp_call(tool_name: str, **kwargs):
    """
    Simulate an MCP tool call
    In a real MCP environment, this would be handled by the MCP protocol
    """
    print(f"🤖 MCP Tool Call: {tool_name}({kwargs})")

    if tool_name == "move_forward":
        return simulate_move_forward(kwargs.get("duration", 0.3))
    elif tool_name == "move_backward":
        return simulate_move_backward(kwargs.get("duration", 0.3))
    elif tool_name == "turn_left":
        return simulate_turn_left(kwargs.get("duration", 0.3))
    elif tool_name == "turn_right":
        return simulate_turn_right(kwargs.get("duration", 0.3))
    elif tool_name == "stop_car":
        return simulate_stop_car()
    elif tool_name == "take_photo_and_analyze":
        return simulate_take_photo_and_analyze(kwargs.get("goal_description", ""))
    elif tool_name == "get_car_status":
        return simulate_get_car_status()
    else:
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}


def simulate_move_forward(duration: float = 0.3):
    """Simulate move_forward MCP tool"""
    try:
        # Make multiple requests to simulate duration
        num_requests = max(1, int(duration / 0.3))
        results = []

        for i in range(num_requests):
            response = requests.post(f"{BASE_URL}/forward", timeout=10)
            results.append(response.json())
            if i < num_requests - 1:
                time.sleep(0.3)

        return {
            "status": "success",
            "message": f"Moved forward for {duration} seconds",
            "duration_used": duration,
            "requests_made": num_requests,
            "results": results,
        }
    except Exception as e:
        return {"status": "error", "message": f"Move forward failed: {str(e)}"}


def simulate_move_backward(duration: float = 0.3):
    """Simulate move_backward MCP tool"""
    try:
        num_requests = max(1, int(duration / 0.3))
        results = []

        for i in range(num_requests):
            response = requests.post(f"{BASE_URL}/backward", timeout=10)
            results.append(response.json())
            if i < num_requests - 1:
                time.sleep(0.3)

        return {
            "status": "success",
            "message": f"Moved backward for {duration} seconds",
            "duration_used": duration,
            "requests_made": num_requests,
            "results": results,
        }
    except Exception as e:
        return {"status": "error", "message": f"Move backward failed: {str(e)}"}


def simulate_turn_left(duration: float = 0.3):
    """Simulate turn_left MCP tool"""
    try:
        num_requests = max(1, int(duration / 0.3))
        results = []

        for i in range(num_requests):
            response = requests.post(f"{BASE_URL}/left", timeout=10)
            results.append(response.json())
            if i < num_requests - 1:
                time.sleep(0.3)

        return {
            "status": "success",
            "message": f"Turned left for {duration} seconds",
            "duration_used": duration,
            "requests_made": num_requests,
            "results": results,
        }
    except Exception as e:
        return {"status": "error", "message": f"Turn left failed: {str(e)}"}


def simulate_turn_right(duration: float = 0.3):
    """Simulate turn_right MCP tool"""
    try:
        num_requests = max(1, int(duration / 0.3))
        results = []

        for i in range(num_requests):
            response = requests.post(f"{BASE_URL}/right", timeout=10)
            results.append(response.json())
            if i < num_requests - 1:
                time.sleep(0.3)

        return {
            "status": "success",
            "message": f"Turned right for {duration} seconds",
            "duration_used": duration,
            "requests_made": num_requests,
            "results": results,
        }
    except Exception as e:
        return {"status": "error", "message": f"Turn right failed: {str(e)}"}


def simulate_stop_car():
    """Simulate stop_car MCP tool"""
    try:
        response = requests.post(f"{BASE_URL}/stop", timeout=10)
        return {
            "status": "success",
            "message": "Car stopped",
            "result": response.json(),
        }
    except Exception as e:
        return {"status": "error", "message": f"Stop car failed: {str(e)}"}


def simulate_take_photo_and_analyze(goal_description: str):
    """Simulate take_photo_and_analyze MCP tool"""
    try:
        payload = {
            "goal": goal_description,
            "laptop_ip": "10.33.49.88",
            "laptop_port": 8000,
        }

        response = requests.post(f"{BASE_URL}/photo", json=payload, timeout=15)
        result = response.json()

        return {
            "status": "success",
            "message": "Photo taken and analyzed",
            "goal": goal_description,
            "analysis_result": result.get("action", "No analysis available"),
            "full_response": result,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Photo analysis failed: {str(e)}",
            "goal": goal_description,
        }


def simulate_get_car_status():
    """Simulate get_car_status MCP tool"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        server_status = "connected" if response.status_code == 200 else "unknown"
    except:
        server_status = "disconnected"

    return {
        "status": "success",
        "car_system": "autonomous-rc-car",
        "flask_server_status": server_status,
        "flask_server_url": BASE_URL,
        "available_tools": [
            "move_forward",
            "move_backward",
            "turn_left",
            "turn_right",
            "stop_car",
            "take_photo_and_analyze",
            "get_car_status",
        ],
        "movement_parameters": {
            "default_duration": 0.3,
            "min_duration": 0.1,
            "max_duration": 1.0,
        },
    }


def autonomous_navigation_example():
    """
    Example of how an LLM would use the MCP server for autonomous navigation
    This simulates the complete workflow of finding a target object
    """
    print("🚗 Autonomous RC Car Navigation Example")
    print("=" * 50)

    # Goal for the autonomous navigation
    goal = "Find a red keychain object on the ground"
    print(f"🎯 Objective: {goal}")
    print()

    # Step 1: Check system status
    print("📋 Step 1: Checking system status...")
    status_result = simulate_mcp_call("get_car_status")
    print(f"Status: {status_result['status']}")
    print(f"Flask server: {status_result.get('flask_server_status', 'unknown')}")
    print()

    # Step 2: Initial assessment
    print("📸 Step 2: Taking initial photo for assessment...")
    photo_result = simulate_mcp_call("take_photo_and_analyze", goal_description=goal)
    print(f"Photo analysis: {photo_result.get('analysis_result', 'No analysis')}")
    print()

    # Step 3: Autonomous navigation loop
    print("🧭 Step 3: Starting autonomous navigation...")
    max_iterations = 20  # Safety limit
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        print(f"\n🔄 Navigation iteration {iteration}")

        # Get current photo analysis
        photo_result = simulate_mcp_call(
            "take_photo_and_analyze", goal_description=goal
        )
        analysis = photo_result.get("analysis_result", "")
        print(f"📸 Photo analysis: {analysis}")

        # Check if goal is achieved
        if "GOAL_ACHIEVED" in analysis:
            print("🎉 SUCCESS: Goal achieved!")
            break

        # Execute movement based on analysis
        if "MOVE_LEFT" in analysis:
            print("⬅️  Moving left (fine adjustment)...")
            result = simulate_mcp_call("turn_left", duration=0.2)
        elif "MOVE_RIGHT" in analysis:
            print("➡️  Moving right (fine adjustment)...")
            result = simulate_mcp_call("turn_right", duration=0.2)
        elif "MOVE_FORWARD" in analysis:
            print("⬆️  Moving forward...")
            result = simulate_mcp_call("move_forward", duration=0.3)
        elif "MOVE_BACKWARD" in analysis:
            print("⬇️  Moving backward...")
            result = simulate_mcp_call("move_backward", duration=0.3)
        elif "TURN_LEFT" in analysis:
            print("🔄 Turning left (searching)...")
            result = simulate_mcp_call("turn_left", duration=0.4)
        elif "TURN_RIGHT" in analysis:
            print("🔄 Turning right (searching)...")
            result = simulate_mcp_call("turn_right", duration=0.4)
        elif "NOT_FOUND" in analysis:
            print("🔍 Target not found, searching systematically...")
            result = simulate_mcp_call("turn_left", duration=0.5)
        else:
            print("❓ Unknown analysis result, stopping...")
            simulate_mcp_call("stop_car")
            break

        print(f"Movement result: {result.get('status', 'unknown')}")

        # Brief pause between movements
        time.sleep(0.5)

    # Final status
    print(f"\n🏁 Navigation completed after {iteration} iterations")
    final_photo = simulate_mcp_call("take_photo_and_analyze", goal_description=goal)
    print(f"Final analysis: {final_photo.get('analysis_result', 'No final analysis')}")


def simple_movement_example():
    """Simple example of basic movements"""
    print("\n🚗 Simple Movement Example")
    print("=" * 30)

    # Forward movement
    print("Moving forward...")
    result = simulate_mcp_call("move_forward", duration=0.3)
    print(f"Result: {result['status']}")

    # Turn left
    print("Turning left...")
    result = simulate_mcp_call("turn_left", duration=0.2)
    print(f"Result: {result['status']}")

    # Turn right
    print("Turning right...")
    result = simulate_mcp_call("turn_right", duration=0.2)
    print(f"Result: {result['status']}")

    # Stop
    print("Stopping...")
    result = simulate_mcp_call("stop_car")
    print(f"Result: {result['status']}")


if __name__ == "__main__":
    print("🤖 Autonomous RC Car MCP Server Example")
    print("This demonstrates how an LLM would use the MCP tools")
    print("=" * 60)

    # Run simple movement example
    simple_movement_example()

    # Run autonomous navigation example
    autonomous_navigation_example()

    print("\n✅ Example completed!")
    print("In a real MCP environment, the LLM would make these tool calls")
    print("through the MCP protocol, and the system would execute them automatically.")
