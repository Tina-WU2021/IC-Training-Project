import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lcd=CharLCD('PCF8574',0x27)
GPIO.setup(18,GPIO.OUT,initial=0)
GPIO.setup(23,GPIO.OUT,initial=0)
GPIO.setup(24,GPIO.OUT,initial=0)
GPIO.setup(25,GPIO.OUT,initial=0)
GPIO.setup(8,GPIO.OUT,initial=0)
adc=Adafruit_ADS1x15.ADS1015()
LED=[8,25,24,23,18]
print('adc')

GAIN=1

print('Reading press Ctrl+C quit')
print('|{0:>6}|{1:>6}|{2:>6}|{3:>6}|'.format(*range(4)))
print('-'*3)

while True:
    values=[0]*4
    for i in range(4):
        values[i]=adc.read_adc(i,gain=GAIN)
    print('|{0:>6}|{1:>6}|{2:>6}|{3:>6}|'.format(*values))
    time.sleep(0.5)
    lcd.cursor_pos=(0,0)
    lcd.write_string("ADC Value: {0:>5}".format(values[1]))
    V=values[1]/GAIN/500
    for i in range(0,int(round(V/3.3*5))):
        GPIO.output(LED[i], GPIO.HIGH)
    for i in range(int(round(V/3.3*5)),5):
        GPIO.output(LED[i], GPIO.LOW)
    lcd.cursor_pos=(1,0)
    lcd.write_string("  Voltage: {0:>4.1f}V".format(V))

