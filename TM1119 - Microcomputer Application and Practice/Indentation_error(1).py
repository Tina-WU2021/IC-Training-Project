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

try:
    while True:
        GPIO.output(18, False)
        time.sleep(.3)
        GPIO.output(18, True)
        time.sleep(.3)

        for i in range(23, 26):
            GPIO.output(i, False)
            time.sleep(.3)
            GPIO.output(i, True)
            time.sleep(.3)
            GPIO.output(8, 0)
            time.sleep(.3)
            GPIO.output(8, 1)
            time.sleep(.3)
            time.sleep(1)
            
#GPIO.cleanup()
except KeyboardInterrupt:
    pass
GPIO.cleanup()
print("END OF PROGRAM")