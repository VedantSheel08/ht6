from mcp.server.fastmcp import FastMCP
import requests
import time
import json
from typing import Optional, Dict, Any

# Initialize FastMCP server
mcp = FastMCP("car-mcp")

# Configuration
BASE_URL = "http://10.33.35.1:5000"  # Flask server on QNX Pi
DEFAULT_DURATION = 1.1  # Default movement duration in seconds (slightly slower)
MAX_DURATION = 2.2      # Max duration for bold moves (reduced)
MIN_DURATION = 0.5      # Minimum duration for any movement

# System prompt for autonomous navigation (short, with camera retry logic)
SYSTEM_PROMPT = """
You are an autonomous RC car navigation system. Your goal is to find and reach specific objects or locations.

- Movement: Forward, backward, left, right (all with duration)
- Camera: Take photos and analyze with AI

## Movement
- All moves use a duration (0.2–2.2s). Default is 1.1s (recommended).
- Use 0.2–0.4s for small adjustments (0.4s turn ≈ 100°).
- Use longer moves (up to 2.2s) to get close to the object.
- Prefer default unless a shorter/longer move is clearly needed.
- The car may not move perfectly straight due to natural hardware drift—account for this in your planning.

## Navigation
- Take a photo every 2 or 3 moves to check your position.
- Only take a single photo if you are very unsure or can't see the object.
- If the object is visible, move forward (even if not centered).
- Only turn if you can't see the object.
- Don't stop until you are very close to the target. If you see even a partial section of the target (e.g., a banner) in the frame, you are likely already there—be generous about stopping when this happens!

## If photo/analysis is not available (e.g. Gemini output says image not available):
- Do NOT move forward to scan.
- Just try the camera again until you get a valid image.

Be safe, keep moving toward the goal, and retry the camera if needed.
"""

def make_request(
    endpoint: str, method: str = "POST", json_data: Optional[dict] = None
) -> Dict[str, Any]:
    """Make HTTP request to Flask server with error handling."""
    try:
        url = f"{BASE_URL}/{endpoint}"
        response = requests.request(method, url, timeout=7, json=json_data)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Request failed: {str(e)}"}


@mcp.tool()
def move_forward(duration: float = DEFAULT_DURATION) -> Dict[str, Any]:
    """
    Move the RC car forward for a specified duration (default 1.1s, up to 2.2s).
    Prefer the default duration for most moves unless a shorter/longer move is clearly needed.

    Args:
        duration: Movement duration in seconds (0.2–2.2, default 1.1)

    Returns:
        Dict with status and response from the car's movement system

    Notes:
        - Prefer moving forward whenever the object is visible, even if not perfectly centered.
        - When locating an object, do NOT stop until the car is very close!
    """
    duration = max(MIN_DURATION, min(duration, MAX_DURATION))
    result = make_request("forward", method="POST", json_data={"duration": duration})
    return {
        "status": "success",
        "message": f"Moved forward for {duration} seconds (confidently approaching the object).",
        "duration_used": duration,
        "result": result,
    }


@mcp.tool()
def move_backward(duration: float = DEFAULT_DURATION) -> Dict[str, Any]:
    """
    Move the RC car backward for a specified duration (default 1.1s, up to 2.2s).

    Args:
        duration: Movement duration in seconds (0.2–2.2, default 1.1)

    Returns:
        Dict with status and response from the car's movement system

    Notes:
        - Use to back away from obstacles or reposition.
    """
    duration = max(MIN_DURATION, min(duration, MAX_DURATION))
    result = make_request("backward", method="POST", json_data={"duration": duration})
    return {
        "status": "success",
        "message": f"Moved backward for {duration} seconds",
        "duration_used": duration,
        "result": result,
    }


@mcp.tool()
def turn_left(duration: float = DEFAULT_DURATION) -> Dict[str, Any]:
    """
    Turn the RC car left for a specified duration (default 1.1s, up to 2.2s).

    Args:
        duration: Turn duration in seconds (0.2–2.2, default 1.1)

    Returns:
        Dict with status and response from the car's movement system

    Notes:
        - Use for changing direction or aligning with targets, but prefer forward movement if the object is visible.
        - For context, a turn of 0.4s is about 100 degrees.
    """
    duration = max(MIN_DURATION, min(duration, MAX_DURATION))
    result = make_request("left", method="POST", json_data={"duration": duration})
    return {
        "status": "success",
        "message": f"Turned left for {duration} seconds",
        "duration_used": duration,
        "result": result,
    }


@mcp.tool()
def turn_right(duration: float = DEFAULT_DURATION) -> Dict[str, Any]:
    """
    Turn the RC car right for a specified duration (default 1.1s, up to 2.2s).

    Args:
        duration: Turn duration in seconds (0.2–2.2, default 1.1)

    Returns:
        Dict with status and response from the car's movement system

    Notes:
        - Use for changing direction or aligning with targets, but prefer forward movement if the object is visible.
        - For context, a turn of 0.4s is about 100 degrees.
    """
    duration = max(MIN_DURATION, min(duration, MAX_DURATION))
    result = make_request("right", method="POST", json_data={"duration": duration})
    return {
        "status": "success",
        "message": f"Turned right for {duration} seconds",
        "duration_used": duration,
        "result": result,
    }


@mcp.tool()
def get_navigation_system_prompt() -> Dict[str, Any]:
    """
    Get the autonomous navigation system prompt and guidelines.
    Call this at the beginning of any navigation task to understand the system capabilities and strategy.

    Returns:
        Dict with the complete navigation system prompt and guidelines

    Notes:
        - Provides guidance for autonomous RC car navigation.
    """
    return {
        "status": "success",
        "system_prompt": SYSTEM_PROMPT,
        "message": "Autonomous navigation system prompt retrieved",
        "key_points": {
            "movement_duration_range": "0.2–2.2 seconds (default 1.1s, use default unless otherwise needed)",
            "safety_priority": "Be careful, but keep moving towards the goal.",
            "photo_frequency": "Take photos every 2 or 3 moves (rarely just 1, only if very unsure or can't see object)",
            "navigation_strategy": "Prefer forward movement when the object is visible, even if not centered. Only turn if you can't see the object. When locating an object, do NOT stop until the car is very close! If you see even a partial section of the target (e.g., a banner) in the frame, you are likely already there—be generous about stopping when this happens!",
            "available_tools": [
                "move_forward(duration)",
                "move_backward(duration)",
                "turn_left(duration)",
                "turn_right(duration)",
                "take_photo_and_analyze(goal_description)",
            ],
            "turn_context": "A turn of 0.4 seconds is about 100 degrees.",
            "camera_retry": "If the image is not available, do not move forward to scan. Just try the camera again until you get a valid image.",
        },
    }


@mcp.tool()
def take_photo_and_analyze(goal_description: str, frequency_hint: str = "normal") -> Dict[str, Any]:
    """
    Take a photo with the car's camera and analyze it for navigation.
    Use this every 2 or 3 moves to verify the car's position and orientation.
    Only use after a single move if you are very unsure or cannot see the object at all.

    Args:
        goal_description: Description of what the car is trying to find or achieve.
        frequency_hint: "normal" (default, for every 2-3 moves), or "urgent" (use after a single move if very unsure/can't see object)

    Returns:
        Dict with photo analysis results and recommended next actions

    Notes:
        - Captures current view from car's camera
        - AI analyzes the image based on the goal description
        - Returns specific action recommendations (MOVE_LEFT, MOVE_RIGHT, MOVE_FORWARD, etc.)
        - Use every 2 or 3 moves to maintain situational awareness and verify you are facing the objective
        - Only use after a single move if you are very unsure or cannot see the object at all
        - If the object is visible, prefer moving forward, even if not perfectly centered.
        - When locating an object, do NOT stop until the car is very close!
    """
    try:
        payload = {
            "goal": goal_description,
            "laptop_ip": "10.33.49.88",  # Laptop IP for processing
            "laptop_port": 8000,
        }
        url = f"{BASE_URL}/photo"
        response = requests.post(
            url, json=payload, timeout=30
        )  # Increased timeout for photo processing
        try:
            result = response.json()
        except Exception as json_err:
            return {
                "status": "error",
                "message": f"Photo endpoint did not return valid JSON: {json_err}",
                "goal": goal_description,
                "http_status": response.status_code,
                "raw_response": response.text,
            }
        if response.status_code >= 400:
            return {
                "status": "error",
                "message": f"Photo endpoint returned error: {result.get('message', 'Unknown error')}",
                "goal": goal_description,
                "http_status": response.status_code,
                "full_response": result,
            }
        return {
            "status": "success",
            "message": "Photo taken and analyzed",
            "goal": goal_description,
            "analysis_result": result.get("annotation", "No analysis available"),
            "full_response": result,
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Failed to take photo: {str(e)}",
            "goal": goal_description,
        }


# The system prompt is now available as a tool: get_navigation_system_prompt()
# This allows the LLM to access the navigation guidelines whenever needed

if __name__ == "__main__":
    mcp.run(transport="stdio")
