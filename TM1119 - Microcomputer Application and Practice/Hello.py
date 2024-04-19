import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18,GPIO.OUT,initial=1)
GPIO.setup(23,GPIO.OUT,initial=1)
GPIO.setup(24,GPIO.OUT,initial=1)
GPIO.setup(25,GPIO.OUT,initial=1)
GPIO.setup(8,GPIO.OUT,initial=1)
GPIO.setwarnings(False)


GPIO.output(18, False)
time.sleep(.3)