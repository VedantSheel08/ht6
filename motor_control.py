import RPi.GPIO as GPIO
import time

IN1, IN2, ENA = 17, 27, 22
IN3, IN4, ENB = 23, 24, 25

GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)

pwm = GPIO.PWM(ENA, 100)
pwm.start(0)

rearSpeed = 50
frontSpeed = 100

def move_forward(t):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(rearSpeed)
    time.sleep(t)

def move_backward(t):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(rearSpeed)
    time.sleep(t)

def move_right(t):
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm.ChangeDutyCycle(frontSpeed)

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(rearSpeed)

    time.sleep(t)

def move_left(t):
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm.ChangeDutyCycle(frontSpeed)

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(rearSpeed)

    time.sleep(t)

def stop_motor():
    pwm.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

move_right(2)
