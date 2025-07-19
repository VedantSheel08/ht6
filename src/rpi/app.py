from flask import Flask, request, jsonify
import rpi_gpio as GPIO
import time
import threading
import atexit

app = Flask(__name__)

# GPIO Pin Configuration
IN1, IN2, ENA = 17, 27, 22
IN3, IN4, ENB = 23, 24, 25

# Global PWM objects
pwm = None
pwm2 = None


def cleanup_gpio():
    """Clean up GPIO resources"""
    global pwm, pwm2
    try:
        if pwm:
            pwm.stop()
        if pwm2:
            pwm2.stop()
        GPIO.cleanup()
    except:
        pass


def initialize_gpio():
    """Initialize GPIO with proper cleanup"""
    global pwm, pwm2

    # Clean up any existing GPIO setup
    try:
        GPIO.cleanup()
    except:
        pass

    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)

    # Initialize PWM with error handling
    try:
        pwm = GPIO.PWM(ENA, 100)  # right motors
        pwm2 = GPIO.PWM(ENB, 100)  # left motors
        pwm.start(0)
        pwm2.start(0)
    except Exception as e:
        print(f"PWM initialization error: {e}")
        # Fallback: use direct GPIO control without PWM
        pwm = None
        pwm2 = None


# Speed settings
slow_speed = 25
fast_speed = 50


def set_motor_speed(pwm_obj, speed):
    """Set motor speed with PWM or direct GPIO"""
    if pwm_obj:
        pwm_obj.ChangeDutyCycle(speed)
    else:
        # Fallback: use direct GPIO for speed control
        pass


def move_forward(t):
    set_motor_speed(pwm, slow_speed)
    set_motor_speed(pwm2, slow_speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(t)
    stop_motor()


def move_backward(t):
    set_motor_speed(pwm, slow_speed)
    set_motor_speed(pwm2, slow_speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(t)
    stop_motor()


def move_right(t):
    set_motor_speed(pwm2, fast_speed)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_motor_speed(pwm, fast_speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(t)
    stop_motor()


def move_left(t):
    set_motor_speed(pwm2, fast_speed)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_motor_speed(pwm, fast_speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(t)
    stop_motor()


def stop_motor():
    set_motor_speed(pwm, 0)
    set_motor_speed(pwm2, 0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


# Register cleanup function
atexit.register(cleanup_gpio)

# Initialize GPIO when module loads
initialize_gpio()

# Flask Routes


@app.route("/")
def home():
    return jsonify(
        {
            "message": "Motor Control API",
            "endpoints": {
                "/forward": "Move forward for specified duration",
                "/backward": "Move backward for specified duration",
                "/left": "Turn left for specified duration",
                "/right": "Turn right for specified duration",
                "/stop": "Stop all motors",
            },
        }
    )


@app.route("/forward", methods=["POST"])
def forward():
    try:
        data = request.get_json()
        duration = data.get("duration", 0.5)  # Default 0.5 seconds

        # Run motor command in a separate thread to avoid blocking
        thread = threading.Thread(target=move_forward, args=(duration,))
        thread.start()

        return jsonify(
            {
                "status": "success",
                "message": f"Moving forward for {duration} seconds",
                "duration": duration,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/backward", methods=["POST"])
def backward():
    try:
        data = request.get_json()
        duration = data.get("duration", 0.5)  # Default 0.5 seconds

        thread = threading.Thread(target=move_backward, args=(duration,))
        thread.start()

        return jsonify(
            {
                "status": "success",
                "message": f"Moving backward for {duration} seconds",
                "duration": duration,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/left", methods=["POST"])
def left():
    try:
        data = request.get_json()
        duration = data.get("duration", 0.5)  # Default 0.5 seconds

        thread = threading.Thread(target=move_left, args=(duration,))
        thread.start()

        return jsonify(
            {
                "status": "success",
                "message": f"Turning left for {duration} seconds",
                "duration": duration,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/right", methods=["POST"])
def right():
    try:
        data = request.get_json()
        duration = data.get("duration", 0.5)  # Default 0.5 seconds

        thread = threading.Thread(target=move_right, args=(duration,))
        thread.start()

        return jsonify(
            {
                "status": "success",
                "message": f"Turning right for {duration} seconds",
                "duration": duration,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/stop", methods=["POST"])
def stop():
    try:
        thread = threading.Thread(target=stop_motor)
        thread.start()

        return jsonify({"status": "success", "message": "All motors stopped"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    try:
        app.run(
            host="0.0.0.0", port=5000, debug=False
        )  # Set debug=False to avoid reload issues
    finally:
        cleanup_gpio()
