from mcp.server.fastmcp import FastMCP
import requests
import time
import json
from typing import Optional, Dict, Any

# Initialize FastMCP server
mcp = FastMCP("car-mcp")

# Configuration
BASE_URL = "http://10.33.35.1:5000"  # Flask server on QNX Pi
DEFAULT_DURATION = 0.45  # Default movement duration in seconds (a bit longer for close approach)
MAX_DURATION = 0.85      # Maximum safe duration (can touch the object)
MIN_DURATION = 0.2       # Minimum duration for any movement

# System prompt for autonomous navigation
SYSTEM_PROMPT = """
You are an autonomous RC car navigation system. Your primary goal is to navigate the car to find and reach specific objects or locations based on given objectives.

## CAR CAPABILITIES:
- Movement: Forward, backward, left turn, right turn
- Sensing: Camera with photo capture and AI analysis
- Navigation: Autonomous decision-making based on visual feedback

## MOVEMENT CHARACTERISTICS:
- All movements use a duration parameter (0.2-0.85 seconds)
- Default duration is 0.45 seconds for most movements (can touch the object)
- Use short durations (0.2-0.4s) for fine adjustments, longer (up to 0.85s) to get right up to the object
- Never use durations longer than 0.85 seconds
- Car responds quickly but may drift slightly

## NAVIGATION STRATEGY:
1. Always take a photo before and after every move to verify position and orientation towards the objective.
2. Use short, controlled movements to get as close as possible to the target (even touching it is OK).
3. Analyze each photo to determine the next action.
4. Keep the objective in mind with every decision.
5. Avoid obstacles and use conservative movements when needed.

## MOVEMENT GUIDELINES:
- Forward: Use to approach targets. Get as close as possible, right before or even touching the object before stopping.
- Backward: Use for backing away or repositioning.
- Left/Right Turns: Use for changing direction or aligning with targets.
- Fine Adjustments: Use 0.2-0.4s durations for precise positioning.
- Search Patterns: Use systematic turns when target is not visible.

## PHOTO ANALYSIS:
- Each photo provides visual feedback about current position.
- AI analysis helps determine optimal next movement.
- Use photos frequently to maintain situational awareness and verify you are facing the objective.
- Photos help identify obstacles, targets, and navigation cues.

## AUTONOMOUS DECISION MAKING:
- Always consider the current objective.
- Use visual feedback to make informed decisions.
- Be patient and methodical in navigation.
- Adapt strategy based on what you see in photos.
- Maintain awareness of car's position relative to goal.

Remember: You are controlling a physical RC car. Be careful, methodical, and always prioritize safety while working toward the objective. TAKE A PHOTO TO VERIFY YOU ARE FACING THE OBJECTIVE BEFORE MOVING FORWARD, AND AFTER EVERY SINGLE MOVE. THIS IS VERY IMPORTANT.
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
    Move the RC car forward for the specified duration.
    The car should get as close as possible to the object before stopping (it can even touch it).

    Args:
        duration: Movement duration in seconds (0.2-0.85, default 0.45)

    Returns:
        Dict with status and response from the car's movement system

    Notes:
        - Use longer durations (up to 0.85s) to get right up to the object, but never overshoot.
        - The car should stop right before or touching the object, not far away.
        - The car moves quickly.
    """
    duration = max(MIN_DURATION, min(duration, MAX_DURATION))
    result = make_request("forward", method="POST", json_data={"duration": duration})
    return {
        "status": "success",
        "message": f"Moved forward for {duration} seconds (as close as possible to the object).",
        "duration_used": duration,
        "result": result,
    }


@mcp.tool()
def move_backward(duration: float = DEFAULT_DURATION) -> Dict[str, Any]:
    """
    Move the RC car backward for the specified duration.

    Args:
        duration: Movement duration in seconds (0.2-0.85, default 0.45)

    Returns:
        Dict with status and response from the car's movement system

    Notes:
        - Use to back away from obstacles or reposition.
        - Use shorter durations for precise backing up.
        - The car moves quickly.
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
    Turn the RC car left for the specified duration.

    Args:
        duration: Turn duration in seconds (0.2-0.85, default 0.45)

    Returns:
        Dict with status and response from the car's movement system

    Notes:
        - Use for changing direction or aligning with targets.
        - Shorter durations for fine adjustments, longer for wider turns.
        - The car moves quickly.
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
    Turn the RC car right for the specified duration.

    Args:
        duration: Turn duration in seconds (0.2-0.85, default 0.45)

    Returns:
        Dict with status and response from the car's movement system

    Notes:
        - Use for changing direction or aligning with targets.
        - Shorter durations for fine adjustments, longer for wider turns.
        - The car moves quickly.
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
    DO NOT CALL IT AGAIN AFTER STARTING THE NAVIGATION TASK.

    Returns:
        Dict with the complete navigation system prompt and guidelines

    Notes:
        - Provides guidance for autonomous RC car navigation.
        - Includes movement characteristics, safety guidelines, and navigation strategy.
    """
    return {
        "status": "success",
        "system_prompt": SYSTEM_PROMPT,
        "message": "Autonomous navigation system prompt retrieved",
        "key_points": {
            "movement_duration_range": "0.2-0.85 seconds (default 0.45s)",
            "safety_priority": "Always use conservative movements",
            "photo_frequency": "Take photos before and after every move",
            "navigation_strategy": "Continuous assessment with incremental movements",
            "available_tools": [
                "move_forward(duration)",
                "move_backward(duration)",
                "turn_left(duration)",
                "turn_right(duration)",
                "take_photo_and_analyze(goal_description)",
            ],
        },
    }


@mcp.tool()
def take_photo_and_analyze(goal_description: str) -> Dict[str, Any]:
    """
    Take a photo with the car's camera and analyze it for navigation purposes.
    Use this before and after every move to verify the car's position and orientation towards the goal.

    Args:
        goal_description: Description of what the car is trying to find or achieve.

    Returns:
        Dict with photo analysis results and recommended next actions

    Notes:
        - Captures current view from car's camera
        - AI analyzes the image based on the goal description
        - Returns specific action recommendations (MOVE_LEFT, MOVE_RIGHT, etc.)
        - Use frequently to maintain situational awareness and verify you are facing the objective
    """
    try:
        payload = {
            "goal": goal_description,
            "laptop_ip": "10.33.49.88",  # Laptop IP for processing
            "laptop_port": 8000,
        }
        url = f"{BASE_URL}/photo"
        response = requests.post(url, json=payload, timeout=7)
        # Do NOT call raise_for_status() here, because the /photo endpoint may return a non-2xx status with a valid JSON error message
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
            # The endpoint returned an error, but with a JSON body
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
