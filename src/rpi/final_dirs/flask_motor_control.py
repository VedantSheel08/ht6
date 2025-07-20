from flask import Flask, jsonify, request
import rpi_gpio as GPIO
import time
import subprocess
import os
import requests

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
fast_speed = 45

def move_forward(duration=0.3):
    pwm.ChangeDutyCycle(slow_speed)
    pwm2.ChangeDutyCycle(slow_speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(duration)
    stop_motor()


def move_backward(duration=0.3):
    pwm.ChangeDutyCycle(slow_speed)
    pwm2.ChangeDutyCycle(slow_speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(duration)
    stop_motor()


def move_right(duration=0.3):
    pwm2.ChangeDutyCycle(fast_speed)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm.ChangeDutyCycle(fast_speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(duration)
    stop_motor()


def move_left(duration=0.3):
    pwm2.ChangeDutyCycle(fast_speed)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm.ChangeDutyCycle(fast_speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(duration)
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


def send_image_to_laptop(
    image_path, goal_description, laptop_ip="10.33.49.88", laptop_port=8000
):
    """
    Send the captured image to the laptop via HTTP POST
    Returns the annotation string from the server response
    """
    try:
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return None

        # Prepare the file for upload
        with open(image_path, "rb") as f:
            files = {"image": ("screenshot.bmp", f, "image/bmp")}
            data = {"goal": goal_description}

            # Send to laptop
            laptop_url = f"http://{laptop_ip}:{laptop_port}/receive_image"
            print(f"Sending image to: {laptop_url}")
            print(f"Goal: {goal_description}")

            response = requests.post(laptop_url, files=files, data=data, timeout=10)

            if response.status_code == 200:
                print("Image sent successfully to laptop")
                # Return the annotation string from the response
                return response.text
            else:
                print(f"Failed to send image. Status: {response.status_code}")
                return None

    except Exception as e:
        print(f"Error sending image to laptop: {e}")
        return None


@app.route("/forward", methods=["POST"])
def forward():
    data = request.get_json(silent=True) or {}
    duration = float(data.get("duration", 0.3))
    move_forward(duration)
    return jsonify({"status": "success", "message": f"Moved forward for {duration} seconds"})


@app.route("/backward", methods=["POST"])
def backward():
    data = request.get_json(silent=True) or {}
    duration = float(data.get("duration", 0.3))
    move_backward(duration)
    return jsonify({"status": "success", "message": f"Moved backward for {duration} seconds"})


@app.route("/left", methods=["POST"])
def left():
    data = request.get_json(silent=True) or {}
    duration = float(data.get("duration", 0.3))
    move_left(duration)
    return jsonify({"status": "success", "message": f"Turned left for {duration} seconds"})


@app.route("/right", methods=["POST"])
def right():
    data = request.get_json(silent=True) or {}
    duration = float(data.get("duration", 0.3))
    move_right(duration)
    return jsonify({"status": "success", "message": f"Turned right for {duration} seconds"})


@app.route("/stop", methods=["POST"])
def stop():
    stop_motor()
    return jsonify({"status": "success", "message": "Stopped"})


@app.route("/photo", methods=["POST"])
def photo():
    try:
        data = request.get_json()
        goal_description = data.get("goal", "Find the target object")
        laptop_ip = data.get("laptop_ip", "10.33.49.88")  # Default laptop IP
        laptop_port = data.get("laptop_port", 8000)  # Default laptop port

        print(f"Goal description: {goal_description}")
        print(f"Sending to laptop: {laptop_ip}:{laptop_port}")

        success = take_photo()
        if success:
            # Send image to laptop
            annotation_string = send_image_to_laptop(
                "screenshot.bmp", goal_description, laptop_ip, laptop_port
            )

            if annotation_string:
                return jsonify(
                    {
                        "status": "success",
                        "message": "Photo taken and sent to laptop",
                        "goal": goal_description,
                        "image_sent": True,
                        "annotation": annotation_string,
                    }
                )
            else:
                return jsonify(
                    {
                        "status": "partial_success",
                        "message": "Photo taken but failed to send to laptop",
                        "goal": goal_description,
                        "image_sent": False,
                    }
                )
        else:
            return jsonify({"status": "error", "message": "Failed to take photo"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    print("Starting Motor Control Flask Server...")
    print("Available endpoints:")
    print("  POST /forward  - Move forward (optional JSON: {\"duration\": seconds})")
    print("  POST /backward - Move backward (optional JSON: {\"duration\": seconds})")
    print("  POST /left     - Turn left (optional JSON: {\"duration\": seconds})")
    print("  POST /right    - Turn right (optional JSON: {\"duration\": seconds})")
    print("  POST /stop     - Stop motors")
    print("  POST /photo    - Take a photo and send to laptop")
    print("\nServer running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
