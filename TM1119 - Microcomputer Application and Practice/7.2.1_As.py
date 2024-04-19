import time
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import Adafruit_DHT

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lcd=CharLCD('PCF8574',0x27)

DHT_SENSOR=Adafruit_DHT.DHT11
DHT_PIN=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(DHT_PIN,GPIO.IN,GPIO.PUD_UP)

try:
    Adafruit_DHT.DHT11=1
except NotImplementedError:
    Adafruit_DHT.DHT11=None
try:
    while True:
        humidity,temperature=Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
        if humidity is not None and temperature is not None:
            lcd.cursor_pos=(0,0)
            lcd.write_string('TEMP={0:0.1f}C'.format(temperature))
            lcd.cursor_pos=(1,0)
            lcd.write_string('Humidity={0:0.1f}%'.format(humidity))
        else:
            print('Sensor failure. Check wiring')
            lcd.clear()
            lcd.cursor_pos=(0,0)
            lcd.write_string('Sensor failure')
        time.sleep(3)
    
except KeyboardInterrupt:
    time.sleep(0.5)
    GPIO.cleanup()
    lcd.clear()
    lcd.cursor_pos=(0,4)
    lcd.write_string('THE  END')
    time.sleep(1)
    lcd.backlight_enabled=False  
    print('End of Program')