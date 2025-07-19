from flask import Flask, jsonify
import rpi_gpio as GPIO
import time

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


if __name__ == "__main__":
    print("Starting Motor Control Flask Server...")
    print("Available endpoints:")
    print("  POST /forward  - Move forward")
    print("  POST /backward - Move backward")
    print("  POST /left     - Turn left")
    print("  POST /right    - Turn right")
    print("  POST /stop     - Stop motors")
    print("\nServer running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
