import rpi_gpio as GPIO
import time

IN1, IN2, ENA = 17, 27, 22
IN3, IN4, ENB = 23, 24, 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

pwm = GPIO.PWM(ENA, 100) # right motors
pwm2 = GPIO.PWM(ENB, 100) # left motors
pwm.start(0)
pwm2.start(0)

slow_speed = 25
fast_speed = 50


def move_forward(t):
    pwm.ChangeDutyCycle(slow_speed)
    pwm2.ChangeDutyCycle(slow_speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(t)
    stop_motor()


def move_backward(t):
    pwm.ChangeDutyCycle(slow_speed)
    pwm2.ChangeDutyCycle(slow_speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(t)
    stop_motor()

def move_right(t):
    pwm2.ChangeDutyCycle(fast_speed)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

    pwm.ChangeDutyCycle(fast_speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

    time.sleep(t)
    stop_motor()

def move_left(t):
    pwm2.ChangeDutyCycle(fast_speed)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

    pwm.ChangeDutyCycle(fast_speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

    time.sleep(t)
    stop_motor()

def stop_motor():
    pwm.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


move_forward(1)
time.sleep(1)
move_right(0.25)
time.sleep(1)
move_backward(1)
time.sleep(1)
move_left(0.25)
time.sleep(1)

