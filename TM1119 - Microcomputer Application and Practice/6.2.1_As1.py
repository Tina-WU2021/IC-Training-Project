import time
import Adafruit_ADS1x15
from RPLCD.i2c import CharLCD
lcd=CharLCD('PCF8574',0x27)

adc=Adafruit_ADS1x15.ADS1015()
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
    lcd.cursor_pos=(1,0)
    lcd.write_string("  Voltage: {0:>4.1f}V".format(V))
