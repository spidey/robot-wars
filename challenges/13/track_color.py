#!/usr/bin/env python3

import RPi.GPIO as GPIO
import cv2 as cv
import numpy as np
import time
from enum import Enum

class Color(Enum):
    RED=1
    YELLOW=2
    GREEN=3
    TURQUOISE=4
    BLUE=5
    BLACK=6
    WHITE=7
    MAGENTA=8

color_to_rgb = {
    Color.RED: [255, 0, 0],
    Color.YELLOW: [255, 255, 0],
    Color.GREEN: [0, 255, 0],
    Color.TURQUOISE: [0, 255, 255],
    Color.BLUE: [0, 0, 255],
    Color.BLACK: [0, 0, 0],
    Color.WHITE: [255, 255, 255],
    Color.MAGENTA: [255, 0, 255],
}

class LEDController:
    LED_PINS = [22, 27, 24]

    def setup(self):
        #Set the GPIO port to BCM encoding mode.
        GPIO.setmode(GPIO.BCM)
        #RGB pins are initialized into output mode
        for pin in LEDController.LED_PINS:
            GPIO.setup(pin, GPIO.OUT)

    def set_rgb(self, color):
        led_status = list(map(lambda num: num > 0, color_to_rgb[color]))
        for index, pin in enumerate(LEDController.LED_PINS):
            GPIO.output(pin, led_status[index])

def color_to_hsv_range(color):
    rgb = np.uint8([[color_to_rgb[color]]])
    hsv = cv.cvtColor(rgb,cv.COLOR_RGB2HSV)
    delta = 10
    hue = hsv[0][0][0]
    upper_bound = hue + delta if hue + delta <= 179 else 179
    lower_bound = hue - delta if hue - delta >= 0 else 0
    return (np.array([lower_bound, 50, 50]), np.array([upper_bound, 255, 255]))

cap = cv.VideoCapture(0)
controller = LEDController()
controller.setup()
while(1):
    # Take each frame
    _, frame = cap.read()
    #cv.imshow('frame', frame)
    #cv.waitKey()
    frame_w, frame_h, _ = frame.shape
    threshold = frame_w*frame_h*0.2
    found = False
    for color in color_to_rgb:
        # Convert BGR to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # define range of blue color in HSV
        hsv_range = color_to_hsv_range(color)
        # Threshold the HSV image to get only pixel with the filtered color
        mask = cv.inRange(hsv, hsv_range[0], hsv_range[1])
        if np.sum(mask == 255) > threshold:
            print(color)
            controller.set_rgb(color)
            found = True
            break
    if not found:
        print('No color found')
        controller.set_rgb(Color.BLACK)

