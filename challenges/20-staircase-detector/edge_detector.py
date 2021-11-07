#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

#Definition of  motor pins
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#Definition of  button
key = 8
buzzer = 8

#TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
#      3                 5                  4                   18
TrackSensorLeftPin1  =  3   #The first tracking infrared sensor pin on the left is connected to  BCM port 3 of Raspberry pi
TrackSensorLeftPin2  =  5   #The second tracking infrared sensor pin on the left is connected to  BCM port 5 of Raspberry pi
TrackSensorRightPin1 =  4   #The first tracking infrared sensor pin on the right is connected to  BCM port 4 of Raspberry pi
TrackSensorRightPin2 =  18  #The second tracking infrared sensor pin on the right is connected to  BCMport 18 of Raspberry pi

#Set the GPIO port to BCM encoding mode.
GPIO.setmode(GPIO.BCM)

#Ignore warning information
GPIO.setwarnings(False)

#Motor pins are initialized into output mode
#Key pin is initialized into input mode
#Track sensor module pins are initialized into input mode
def init():
    global pwm_ENA
    global pwm_ENB
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(key,GPIO.IN)
    GPIO.setup(TrackSensorLeftPin1,GPIO.IN)
    GPIO.setup(TrackSensorLeftPin2,GPIO.IN)
    GPIO.setup(TrackSensorRightPin1,GPIO.IN)
    GPIO.setup(TrackSensorRightPin2,GPIO.IN)
     #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    LEDController.setup()
    GPIO.setup(buzzer,GPIO.OUT,initial=GPIO.HIGH)

#advance
def run(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#back
def back(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#turn left 
def left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#turn right
def right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#turn left in place
def spin_left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#turn right in place
def spin_right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#brake
def brake():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

#Button detection
def key_scan():
    while GPIO.input(key):
        pass
    while not GPIO.input(key):
        time.sleep(0.01)
        if not GPIO.input(key):
            time.sleep(0.01)
            while not GPIO.input(key):
                pass

class LEDController:
    LED_PINS = [22, 27, 24]

    def setup():
        #Set the GPIO port to BCM encoding mode.
        GPIO.setmode(GPIO.BCM)
        #RGB pins are initialized into output mode
        for pin in LEDController.LED_PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def set_rgb(rgb):
        #Definition of RGB module pin
        for index, value in enumerate(rgb):
            GPIO.output(LEDController.LED_PINS[index], value)

def wait_for_help():
    while True:
        LEDController.set_rgb([1,0,0])
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(0.3)
        LEDController.set_rgb([0,0,1])
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(0.3)
        TrackSensorLeftValue1  = GPIO.input(TrackSensorLeftPin1)
        TrackSensorLeftValue2  = GPIO.input(TrackSensorLeftPin2)
        TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
        TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)
        all_on = TrackSensorLeftValue1 and TrackSensorLeftValue2 and TrackSensorRightValue1 and TrackSensorRightValue2
        if all_on:
            LEDController.set_rgb([0,0,0])
            break

#delay 2s
time.sleep(2)

#The try/except statement is used to detect errors in the try block.
#the except statement catches the exception information and processes it.
try:
    init()
    key_scan()

    while True:
        TrackSensorLeftValue1  = GPIO.input(TrackSensorLeftPin1)
        TrackSensorLeftValue2  = GPIO.input(TrackSensorLeftPin2)
        TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
        TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)
        all_on = TrackSensorLeftValue1 and TrackSensorLeftValue2 and TrackSensorRightValue1 and TrackSensorRightValue2
        while all_on:
            run(1, 1)
            time.sleep(0.1)
            print(f"{TrackSensorLeftValue1} {TrackSensorLeftValue2} {TrackSensorRightValue1} {TrackSensorRightValue2} {all_on}")
            TrackSensorLeftValue1  = GPIO.input(TrackSensorLeftPin1)
            TrackSensorLeftValue2  = GPIO.input(TrackSensorLeftPin2)
            TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
            TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)
            all_on = TrackSensorLeftValue1 and TrackSensorLeftValue2 and TrackSensorRightValue1 and TrackSensorRightValue2
        brake()
        wait_for_help()
except KeyboardInterrupt:
    pass
pwm_ENA.stop()
pwm_ENB.stop()
GPIO.cleanup()

