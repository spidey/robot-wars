#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

NINETY_DEGREES = 0.29

#Definition of  motor pin 
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#Set the GPIO port to BCM encoding mode
GPIO.setmode(GPIO.BCM)

#Ignore warning information
GPIO.setwarnings(False)

#Motor pin initialization operation
def motor_init():
    global pwm_ENA
    global pwm_ENB
    global delaytime
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)

#advance
def run(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(delaytime)
    brake()

#back
def back(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(delaytime)
    brake()

#turn left
def left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(delaytime)
    brake()

#turn right
def right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(delaytime)
    brake()

#turn left in place
def spin_left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(delaytime)
    brake()

#turn right in place
def spin_right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(delaytime)
    brake()

#brake
def brake():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(0.2)

def square():
    SQUARE_SIDE = (0.53 * 2)

    for i in range(4):
        run(SQUARE_SIDE)
        spin_right(NINETY_DEGREES)
    brake()

def tech():
    FONT_PART = 0.2
    # T
    run(FONT_PART)
    spin_right(NINETY_DEGREES)
    run(2 * FONT_PART)
    back(2 * FONT_PART)
    spin_left(NINETY_DEGREES)
    run(FONT_PART)

    time.sleep(0.5)
    run(0.5 * FONT_PART)
    time.sleep(0.5)

    # E
    run(2 * FONT_PART)
    back(2 * FONT_PART)
    spin_right(NINETY_DEGREES)
    run(FONT_PART)
    spin_left(NINETY_DEGREES)
    run(FONT_PART)
    back(FONT_PART)
    spin_right(NINETY_DEGREES)
    run(FONT_PART)
    spin_left(NINETY_DEGREES)
    run(2 * FONT_PART)

    time.sleep(0.5)
    run(0.5 * FONT_PART)
    time.sleep(0.5)

    # C
    run(2 * FONT_PART)
    back(2 * FONT_PART)
    spin_left(NINETY_DEGREES)
    run(2 * FONT_PART)
    spin_right(NINETY_DEGREES)
    run(2 * FONT_PART)

    time.sleep(0.5)
    run(0.5 * FONT_PART)
    time.sleep(0.5)

    # H
    spin_right(NINETY_DEGREES)
    run(2 * FONT_PART)
    back(FONT_PART)
    spin_left(NINETY_DEGREES)
    run(FONT_PART)
    spin_left(NINETY_DEGREES)
    back(FONT_PART)
    run(2 * FONT_PART)

#Delay 2s	
time.sleep(2)

motor_init()

try:
    square()
    time.sleep(2)
    tech()
except KeyboardInterrupt:
    brake()

pwm_ENA.stop()
pwm_ENB.stop()
GPIO.cleanup() 
