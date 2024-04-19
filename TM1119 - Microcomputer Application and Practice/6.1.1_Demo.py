import time
import Adafruit_ADS1x15

adc=Adafruit_ADS1x15.ADS1015()
print('adc')

GAIN=2

print('Reading press Ctrl+C quit')
print('|{0:>6}|{1:>6}|{2:>6}|{3:>6}|'.format(*range(4)))
print('-'*3)

while True:
    values=[0]*4
    for i in range(4):
        values[i]=adc.read_adc(i,gain=GAIN)
    print('|{0:>6}|{1:>6}|{2:>6}|{3:>6}|'.format(*values))
    time.sleep(0.5)