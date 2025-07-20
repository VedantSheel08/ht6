from flask import Flask, jsonify, request
import rpi_gpio as GPIO
import time
import subprocess
import os
from google.genai import types
from google import genai

client = genai.Client()

app = Flask(__name__)

# GPIO Pin Configuration
IN1, IN2, ENA = 17, 27, 22
IN3, IN4, ENB = 23, 24, 25

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# PWM Setup
pwm = GPIO.PWM(ENA, 100)  # right motors
pwm2 = GPIO.PWM(ENB, 100)  # left motors
pwm.start(0)
pwm2.start(0)

# Speed settings
slow_speed = 25
fast_speed = 50


def move_forward():
    pwm.ChangeDutyCycle(slow_speed)
    pwm2.ChangeDutyCycle(slow_speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(1)  # Move for 1 second
    stop_motor()


def move_backward():
    pwm.ChangeDutyCycle(slow_speed)
    pwm2.ChangeDutyCycle(slow_speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(1)  # Move for 1 second
    stop_motor()


def move_right():
    pwm2.ChangeDutyCycle(fast_speed)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm.ChangeDutyCycle(fast_speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(0.5)  # Turn for 0.5 seconds
    stop_motor()


def move_left():
    pwm2.ChangeDutyCycle(fast_speed)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm.ChangeDutyCycle(fast_speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(0.5)  # Turn for 0.5 seconds
    stop_motor()


def stop_motor():
    pwm.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


def take_photo():
    """
    Take a photo using the camera_example3_viewfinder application
    Opens the camera app and takes a screenshot
    """
    try:
        # Open the camera application
        print("Opening camera application...")
        camera_process = subprocess.Popen(
            ["camera_example3_viewfinder"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Give the camera app time to start up
        time.sleep(3)

        # Take screenshot using the screenshot command
        print("Taking screenshot...")
        screenshot_result = subprocess.run(
            ["screenshot"], capture_output=True, text=True
        )

        if screenshot_result.returncode == 0:
            print("Photo taken successfully!")
            return True
        else:
            print(f"Screenshot failed: {screenshot_result.stderr}")
            return False

    except Exception as e:
        print(f"Error taking photo: {e}")
        return False


def process_screenshot_with_gemini(goal_description):
    """
    Process the screenshot.bmp file with Gemini API based on the goal description
    """
    try:
        # Check if screenshot.bmp exists
        screenshot_path = "screenshot.bmp"
        if os.path.exists(screenshot_path):
            print(f"Found screenshot at: {screenshot_path}")
            print(f"Processing with Gemini API for goal: {goal_description}")

            # Read the image file
            with open(screenshot_path, "rb") as f:
                image_bytes = f.read()

            # Create comprehensive prompt for motor car navigation
            comprehensive_prompt = f"""
The agent that called you is controlling a motor car with a camera. You are not the motor car or the camera, but you are being called as a function to help the MCP Server decide what to do next. Your goal is: "{goal_description}"

Analyze this image and respond with a short, clear action code (see below), followed by a brief explanation (1-2 sentences) about why you chose that action and any relevant uncertainty or nuance. If you are unsure about the best movement (for example, if moving left might move the target too far, or if the target is only partially visible), mention that in your explanation. The car's hardware interface is not always perfectly accurate—movements may drift or overshoot—so be cautious in your recommendations.

Possible action codes and when to use them:
1. GOAL_ACHIEVED: Use "GOAL_ACHIEVED" if the target object is clearly visible and centered in the camera frame, meaning the car has reached the desired position.
2. MOVE_LEFT: Use "MOVE_LEFT" if the target is visible but positioned to the left side of the frame (left 25% of screen). If you are unsure how much to move left, or if a small move might overshoot, mention this.
3. MOVE_RIGHT: Use "MOVE_RIGHT" if the target is visible but positioned to the right side of the frame (right 25% of screen). Note any uncertainty about how much to move.
4. MOVE_FORWARD: Use "MOVE_FORWARD" if the target is visible but too far away or needs to be approached. If the distance is unclear, mention it.
5. MOVE_BACKWARD: Use "MOVE_BACKWARD" if the target is visible but too close or needs backing up.
6. TURN_RIGHT: Use "TURN_RIGHT" if the target is not visible in the current frame and you recommend rotating right to search.
7. TURN_LEFT: Use "TURN_LEFT" if the target is not visible in the current frame and you recommend rotating left to search.
8. NOT_FOUND: Use "NOT_FOUND" if the target object is completely absent from the current view.

IMPORTANT:
- Respond with the action code (e.g., "MOVE_RIGHT") on the first line, then a short explanation (1-2 sentences) on the next line.
- Be specific about the target's position and any uncertainty about the movement or the car's accuracy.
- If the target is partially visible or ambiguous, explain your reasoning and suggest the most appropriate movement.
- The car's movement is not always precise; mention if a movement might overshoot or if fine adjustment is needed.
- Keep your response concise and focused on helping the car center and approach the target safely.
- Remember, you are assisting the MCP Server by analyzing the image and providing your best recommendation for the next action."""

            # Send to Gemini API
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/bmp",
                    ),
                    comprehensive_prompt,
                ],
            )

            print(f"Gemini response: {response.text}")
            return response.text.strip()

        else:
            print(f"Screenshot file not found at: {screenshot_path}")
            return "ERROR: Screenshot not found"

    except Exception as e:
        print(f"Error processing screenshot with Gemini: {e}")
        return f"ERROR: {str(e)}"


@app.route("/forward", methods=["POST"])
def forward():
    move_forward()
    return jsonify({"status": "success", "message": "Moved forward"})


@app.route("/backward", methods=["POST"])
def backward():
    move_backward()
    return jsonify({"status": "success", "message": "Moved backward"})


@app.route("/left", methods=["POST"])
def left():
    move_left()
    return jsonify({"status": "success", "message": "Turned left"})


@app.route("/right", methods=["POST"])
def right():
    move_right()
    return jsonify({"status": "success", "message": "Turned right"})


@app.route("/stop", methods=["POST"])
def stop():
    stop_motor()
    return jsonify({"status": "success", "message": "Stopped"})


@app.route("/photo", methods=["POST"])
def photo():
    try:
        data = request.get_json()
        goal_description = data.get("goal", "Find the target object")
        print(f"Goal description: {goal_description}")

        success = take_photo()
        if success:
            # Process with Gemini API
            gemini_response = process_screenshot_with_gemini(goal_description)

            return jsonify(
                {
                    "status": "success",
                    "message": "Photo taken and analyzed",
                    "goal": goal_description,
                    "action": gemini_response,
                }
            )
        else:
            return jsonify({"status": "error", "message": "Failed to take photo"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    print("Starting Motor Control Flask Server...")
    print("Available endpoints:")
    print("  POST /forward  - Move forward")
    print("  POST /backward - Move backward")
    print("  POST /left     - Turn left")
    print("  POST /right    - Turn right")
    print("  POST /stop     - Stop motors")
    print("  POST /photo    - Take a photo and analyze with goal")
    print("\nServer running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
