from mcp.server.fastmcp import FastMCP
import requests
import time
import json
from typing import Optional, Dict, Any

# Initialize FastMCP server
mcp = FastMCP("car-mcp")

# Configuration
BASE_URL = "http://10.33.35.1:5000"  # Flask server on QNX Pi
DEFAULT_DURATION = 1.5  # Default movement duration in seconds (encouraged for most moves)
MAX_DURATION = 3.0      # Max duration for bold moves
MIN_DURATION = 0.5      # Minimum duration for any movement

# System prompt for autonomous navigation (updated for less frequent camera usage)
SYSTEM_PROMPT = """
You are an autonomous RC car navigation system. Your goal is to find and reach specific objects or locations based on objectives.

## CAR CAPABILITIES:
- Movement: Forward, backward, left, right (all with duration)
- Sensing: Camera with photo capture and AI analysis

## MOVEMENT:
- All moves use a duration (0.2–3.0s). Default is 1.5s (recommended for most moves).
- Use 0.2–0.4s for fine adjustments (e.g., a 0.4s turn ≈ 100° approx).
- Use longer durations (up to 3.0s) to cover more ground or get right up to the object.
- Prefer the default duration unless a shorter/longer move is clearly needed.
- Car responds quickly but may drift slightly.

## NAVIGATION STRATEGY:
1. Take a photo every 2 or 3 moves to check your position. Only take a single photo if you are very unsure or cannot see the object at all.
2. Use confident forward moves when the object is in view, even if not centered.
3. If the object is visible but not centered, move forward (possibly with a slight turn) rather than just turning in place.
4. Only use turns if the object is not visible or you need to reorient.
5. Don't worry about being perfect—keep moving and adjust as you go.
6. Avoid obstacles and use conservative moves if needed.
7. **When searching for an object, DO NOT STOP UNTIL THE CAR IS VERY CLOSE!** Move forward until nearly touching the target.

## PHOTO ANALYSIS:
- Each photo provides visual feedback.
- AI analysis helps determine the next move.
- Use photos every 2 or 3 moves to maintain awareness and verify you are facing the objective.
- Only take a single photo if you are very unsure or cannot see the object at all.

## DECISION MAKING:
- Always consider the current objective.
- Use visual feedback to make informed decisions.
- Be patient and methodical, but keep making progress.
- Adapt based on what you see in photos.

Remember: You are controlling a real RC car. Prioritize safety, but don't worry about being perfect—just keep moving towards the goal and adjust as needed.
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
    Move the RC car forward for a specified duration (default 1.5s, up to 3s).
    Prefer the default duration for most moves unless a shorter/longer move is clearly needed.

    Args:
        duration: Movement duration in seconds (0.2–3.0, default 1.5)

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
    Move the RC car backward for a specified duration (default 1.5s, up to 3s).

    Args:
        duration: Movement duration in seconds (0.2–3.0, default 1.5)

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
    Turn the RC car left for a specified duration (default 1.5s, up to 3s).

    Args:
        duration: Turn duration in seconds (0.2–3.0, default 1.5)

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
    Turn the RC car right for a specified duration (default 1.5s, up to 3s).

    Args:
        duration: Turn duration in seconds (0.2–3.0, default 1.5)

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
            "movement_duration_range": "0.2–3.0 seconds (default 1.5s, use default unless otherwise needed)",
            "safety_priority": "Be careful, but keep moving towards the goal.",
            "photo_frequency": "Take photos every 2 or 3 moves (rarely just 1, only if very unsure or can't see object)",
            "navigation_strategy": "Prefer forward movement when the object is visible, even if not centered. Only turn if you can't see the object. When locating an object, do NOT stop until the car is very close!",
            "available_tools": [
                "move_forward(duration)",
                "move_backward(duration)",
                "turn_left(duration)",
                "turn_right(duration)",
                "take_photo_and_analyze(goal_description)",
            ],
            "turn_context": "A turn of 0.4 seconds is about 100 degrees.",
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
            "frequency_hint": frequency_hint,  # Inform downstream logic of intent
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
            "analysis_result": result.get("action", "No analysis available"),
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
