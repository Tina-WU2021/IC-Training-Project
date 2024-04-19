'''
Group 11

ZHANG Huanyu (21098072D)
WU Xiaotao (21097724D)

'''
import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import numpy as np
from RPLCD.i2c import CharLCD

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lcd=CharLCD('PCF8574',0x27)
GPIO.setup([21,20],GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(18,GPIO.OUT,initial=0)
GPIO.setup(23,GPIO.OUT,initial=0)
GPIO.setup(24,GPIO.OUT,initial=0)
GPIO.setup(25,GPIO.OUT,initial=0)
GPIO.setup(8,GPIO.OUT,initial=0)
adc=Adafruit_ADS1x15.ADS1015()
LED=[8,25,24,23,18]

print('Reading press Ctrl+C quit')
print('|{0:>6}|{1:>6}|{2:>6}|{3:>6}|'.format(*range(4)))
print('-'*3)

def welcome():
    lcd.cursor_pos=(0,0)
    lcd.write_string("Mini-Project Two")
    lcd.cursor_pos=(1,0)
    lcd.write_string("SoundLevel Meter")
    time.sleep(2.5)
    lcd.clear()

values=[0]*4
GAIN=1
def info():
    global values
    for i in range(4):
        values[i]=adc.read_adc(i,gain=GAIN)
    print('|{0:>6}|{1:>6}|{2:>6}|{3:>6}|'.format(*values))

peak=0
def peak_detect(v):
    global peak
    if v>peak:
        peak=v
    peak_db=20*np.log(peak/standard)
    lcd.cursor_pos=(0,11)
    lcd.write_string("Peak")
    lcd.cursor_pos=(1,10)
    lcd.write_string("{:4.0f}dB".format(peak_db))
    if GPIO.input(20)==0:        
        peak=0
        time.sleep(0.5)

def light(db):
    if db >= -60:
        for i in range(0,5):
            GPIO.output(LED[i], GPIO.HIGH)
    elif db < -85:
        for i in range(0,5):
            GPIO.output(LED[i], GPIO.LOW)
    else:
        for i in range(0,int(round((db+85)//5))):
            GPIO.output(LED[i], GPIO.HIGH)
        for i in range(int(round((db+85)//5)),5):
            GPIO.output(LED[i], GPIO.LOW)

def LCD_bar(db):
    if db >= -60:
        for i in range(0,9):
            lcd.cursor_pos=(1,i)
            lcd.write_string('\xff')
    elif db < -84:
        time.sleep(1)
        lcd.cursor_pos=(1,0)
        lcd.write_string('SW2:Reset ')
    else:
        for i in range(0,int(round(db+84))//3):
            lcd.cursor_pos=(1,i)
            lcd.write_string('\xff')
        for i in range(int(round(db+84))//3,9):
            lcd.cursor_pos=(1,i)
            lcd.write_string(' ')

try:
    welcome()
    while True:
        info()
    
        standard=50
        v=values[2]
        db=20*np.log(v/standard)
    
        lcd.cursor_pos=(0,0)
        lcd.write_string("{:^6.0f}dB".format(db))
    
        peak_detect(v)
        light(db)
        LCD_bar(db)

except KeyboardInterrupt:
    time.sleep(0.5)
    GPIO.cleanup()
    lcd.clear()
    lcd.cursor_pos=(0,4)
    lcd.write_string('THE  END')
    time.sleep(1)
    lcd.backlight_enabled=False  
    print('End of Program')