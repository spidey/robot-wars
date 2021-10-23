#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from enum import Enum
import morse

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
   LED_PINS = [22, 27, 24]

   def setup(self):
     #Set the GPIO port to BCM encoding mode.
     GPIO.setmode(GPIO.BCM)
     #RGB pins are initialized into output mode
     for pin in LEDController.LED_PINS:
       GPIO.setup(pin, GPIO.OUT)


   def set_rgb(self, led_status):
    #Definition of RGB module pin
    for index, pin in enumerate(LEDController.LED_PINS):
      value = (GPIO.HIGH if led_status[index] == LEDStatus.ON else GPIO.LOW)
      GPIO.output(pin, value)


class Morser:
  color_to_led_status = {
    Color.RED: [LEDStatus.ON, LEDStatus.OFF, LEDStatus.OFF],
    Color.NO_COLOR: [LEDStatus.OFF, LEDStatus.OFF, LEDStatus.OFF],
    Color.YELLOW: [LEDStatus.ON, LEDStatus.ON, LEDStatus.OFF],
    Color.GREEN: [LEDStatus.OFF, LEDStatus.ON, LEDStatus.OFF],
    Color.BLUE: [LEDStatus.OFF, LEDStatus.OFF, LEDStatus.ON],
    Color.TURQUOISE: [LEDStatus.OFF, LEDStatus.ON, LEDStatus.ON],
  }

  delay = 0.2

  def __init__(self, controller):
    self.controller = controller

  def set_color(self, color):
    self.color = color

  def text(self, text):
      signal = morse.morse_signal(text)
      print(signal)
      for c in signal:
          current_color = self.color
          if c == ' ':
            current_color = Color.NO_COLOR
          self.controller.set_rgb(Morser.color_to_led_status[current_color])
          time.sleep(Morser.delay)

  def letter_delay(self):
    time.sleep(Morser.delay*3)

  def word_delay(self):
    time.sleep(Morser.delay*4)


#Display 7 color LED
controller = LEDController()
controller.setup()
morser = Morser(controller)
pattern = [('a', Color.RED), ('d', Color.YELLOW), ('y', Color.GREEN), ('e', Color.TURQUOISE), ('n', Color.BLUE)]
while True:
  for letter, color in pattern:
    morser.set_color(color)
    morser.text(letter)
    morser.letter_delay()
  morser.word_delay()
GPIO.cleanup()
