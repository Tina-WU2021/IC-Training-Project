import RPi.GPIO as GPIO
import Adafruit_DHT
import time

DHT_SENSOR=Adafruit_DHT.DHT11
DHT_PIN=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(DHT_PIN,GPIO.IN,GPIO.PUD_UP)

try:
    Adafruit_DHT.DHT11=1
except NotImplementedError:
    Adafruit_DHT.DHT11=None
while True:
    humidity,temperature=Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
    if humidity is not None and temperature is not None:
        print('TEMP={0:0.1f}C Humidity={1:0.1f}'.format(temperature,humidity))
    else:
        print('Sensor failure. Check wiring')
    time.sleep(3)