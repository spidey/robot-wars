# -*- coding:UTF-8 -*-

import RPi.GPIO as GPIO
import time
from enum import Enum

#Set the GPIO port to BCM encoding mode.
GPIO.setmode(GPIO.BCM)

#RGB pins are initialized into output mode
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)

class LEDStatus(Enum):
  OFF=0
  ON=1

class Color(Enum):
  NO_COLOR=0
  RED=1
  YELLOW=2
  GREEN=3
  TURQUOISE=4
  BLUE=5

class LEDController:
   def setup():
     #Set the GPIO port to BCM encoding mode.
     GPIO.setmode(GPIO.BCM)

     #RGB pins are initialized into output mode
     GPIO.setup(LED_R, GPIO.OUT)
     GPIO.setup(LED_G, GPIO.OUT)
     GPIO.setup(LED_B, GPIO.OUT)


   def set_rgb(led_staus):
    #Definition of RGB module pin
    LED_PINS = {22: 0, 27: 1, 24:2}
    for pin, index in LED_PINS:
      GPIO.output(pin, GPIO.HIGH if led_status[index] == ON else  GPIO.LOW)


class Morser:
  color_to_led_status = {
    Color.RED: [LEDStatus.ON, LEDStatus.OFF, LEDStatus.OFF],
    Color.NO_COLOR: [LEDStatus.ON, LEDStatus.OFF, LEDStatus.OFF]
  }

  def __init__(self, controller):
    self.controller = controller
    self.color = Color.NO_COLOR

  def set_color(color):
    self.color = color
    self.controller.set_rgb(color_to_led_status[color])

#Display 7 color LED
try:
  controller = LEDController()
  controller.setup()
  morser = Morser(controller)
  while True:
    morser.set_color(Color.RED)
    time.sleep(1)
    morser.set_color(Color.NO_COLOR)
except:
    print "except"
GPIO.cleanup()
