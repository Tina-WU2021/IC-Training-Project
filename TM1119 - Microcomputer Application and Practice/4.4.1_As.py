import time
import threading
import random
from RPLCD.i2c import CharLCD
lcd=CharLCD('PCF8574',0x27)

blink=False

a=(
    0b00011,
    0b00111,
    0b01111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111
)
b=(
    0b11111,
    0b11111,
    0b11111,
    0b00000,
    0b00000,
    0b00000,
    0b11111,
    0b11111
)
c=(
    0b11000,
    0b11100,
    0b11110,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111
)
d=(
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b01111,
    0b00111,
    0b00011,
)
e=(
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b11111,
    0b11111,
    0b11111
)
f=(
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11110,
    0b11100,
    0b11000,
)
g=(
    0b11111,
    0b11111,
    0b11111,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000)
h=(
    0b00000,
    0b01010,
    0b01010,
    0b00000,
    0b11111,
    0b01010,
    0b01010,
    0b00100
)
lcd.create_char(0,a)
lcd.create_char(1,b)
lcd.create_char(2,c)
lcd.create_char(3,d)
lcd.create_char(4,e)
lcd.create_char(5,f)
lcd.create_char(6,g)
lcd.create_char(7,h)

def display(n,x):
    if n == 0:
        lcd.cursor_pos=(0,x)
        lcd.write_string('\x00')
        lcd.cursor_pos=(0,x+1)
        lcd.write_string('\x06')
        lcd.cursor_pos=(0,x+2)
        lcd.write_string('\x02')
        lcd.cursor_pos=(1,x)
        lcd.write_string('\x03')
        lcd.cursor_pos=(1,x+1)
        lcd.write_string('\x04')
        lcd.cursor_pos=(1,x+2)
        lcd.write_string('\x05')
    if n == 1:
        lcd.cursor_pos=(0,x)
        lcd.write_string('\x06')
        lcd.cursor_pos=(0,x+1)
        lcd.write_string('\x02')
        lcd.cursor_pos=(0,x+2)
        lcd.write_string(' ')
        lcd.cursor_pos=(1,x)
        lcd.write_string('\x04')
        lcd.cursor_pos=(1,x+1)
        lcd.write_string('\xff')
        lcd.cursor_pos=(1,x+2)
        lcd.write_string('\x04')
    if n == 2:
        lcd.cursor_pos=(0,x)
        lcd.write_string('\x01')
        lcd.cursor_pos=(0,x+1)
        lcd.write_string('\x01')
        lcd.cursor_pos=(0,x+2)
        lcd.write_string('\x02')
        lcd.cursor_pos=(1,x)
        lcd.write_string('\x03')
        lcd.cursor_pos=(1,x+1)
        lcd.write_string('\x04')
        lcd.cursor_pos=(1,x+2)
        lcd.write_string('\x04')
    if n == 3:
        lcd.cursor_pos=(0,x)
        lcd.write_string('\x01')
        lcd.cursor_pos=(0,x+1)
        lcd.write_string('\x01')
        lcd.cursor_pos=(0,x+2)
        lcd.write_string('\x02')
        lcd.cursor_pos=(1,x)
        lcd.write_string('\x04')
        lcd.cursor_pos=(1,x+1)
        lcd.write_string('\x04')
        lcd.cursor_pos=(1,x+2)
        lcd.write_string('\x05')
    if n == 4:
        lcd.cursor_pos=(0,x)
        lcd.write_string('\x03')
        lcd.cursor_pos=(0,x+1)
        lcd.write_string('\x04')
        lcd.cursor_pos=(0,x+2)
        lcd.write_string('\xff')
        lcd.cursor_pos=(1,x)
        lcd.write_string(' ')
        lcd.cursor_pos=(1,x+1)
        lcd.write_string(' ')
        lcd.cursor_pos=(1,x+2)
        lcd.write_string('\xff')
    if n == 5:
        lcd.cursor_pos=(0,x)
        lcd.write_string('\x03')
        lcd.cursor_pos=(0,x+1)
        lcd.write_string('\x01')
        lcd.cursor_pos=(0,x+2)
        lcd.write_string('\x01')
        lcd.cursor_pos=(1,x)
        lcd.write_string('\x04')
        lcd.cursor_pos=(1,x+1)
        lcd.write_string('\x04')
        lcd.cursor_pos=(1,x+2)
        lcd.write_string('\x05')
    if n == 6:
        lcd.cursor_pos=(0,x)
        lcd.write_string('\x00')
        lcd.cursor_pos=(0,x+1)
        lcd.write_string('\x01')
        lcd.cursor_pos=(0,x+2)
        lcd.write_string('\x01')
        lcd.cursor_pos=(1,x)
        lcd.write_string('\x03')
        lcd.cursor_pos=(1,x+1)
        lcd.write_string('\x04')
        lcd.cursor_pos=(1,x+2)
        lcd.write_string('\x05')
    if n == 7:
        lcd.cursor_pos=(0,x)
        lcd.write_string('\x00')
        lcd.cursor_pos=(0,x+1)
        lcd.write_string('\x06')
        lcd.cursor_pos=(0,x+2)
        lcd.write_string('\x02')
        lcd.cursor_pos=(1,x)
        lcd.write_string(' ')
        lcd.cursor_pos=(1,x+1)
        lcd.write_string(' ')
        lcd.cursor_pos=(1,x+2)
        lcd.write_string('\xff')
    if n == 8:
        lcd.cursor_pos=(0,x)
        lcd.write_string('\x00')
        lcd.cursor_pos=(0,x+1)
        lcd.write_string('\x01')
        lcd.cursor_pos=(0,x+2)
        lcd.write_string('\x02')
        lcd.cursor_pos=(1,x)
        lcd.write_string('\x03')
        lcd.cursor_pos=(1,x+1)
        lcd.write_string('\x04')
        lcd.cursor_pos=(1,x+2)
        lcd.write_string('\x05')
    if n == 9:
        lcd.cursor_pos=(0,x)
        lcd.write_string('\x00')
        lcd.cursor_pos=(0,x+1)
        lcd.write_string('\x01')
        lcd.cursor_pos=(0,x+2)
        lcd.write_string('\x02')
        lcd.cursor_pos=(1,x)
        lcd.write_string('\x04')
        lcd.cursor_pos=(1,x+1)
        lcd.write_string('\x04')
        lcd.cursor_pos=(1,x+2)
        lcd.write_string('\x05')

def current_time():
    timer = threading.Timer(1,current_time) 
    timer.start()
    global t
    t = time.asctime(time.localtime(time.time()))

def blinking():
    global blink
    timer = threading.Timer(0.5,blinking) 
    timer.start() 
    blink = not(blink)

def display_time(light):    
    display(int(t[11]),0)
    display(int(t[12]),3)
    display(int(t[14]),7)
    display(int(t[15]),10)
    lcd.cursor_pos=(1,14)
    lcd.write_string(t[17:19])
    if light == True:
        lcd.cursor_pos=(0,6)
        lcd.write_string('\xa5')
        lcd.cursor_pos=(1,6)
        lcd.write_string('\xa5')
        lcd.cursor_pos=(1,13)
        lcd.write_string(':')
    else:
        lcd.cursor_pos=(0,6)
        lcd.write_string(' ')
        lcd.cursor_pos=(1,6)
        lcd.write_string(' ')
        lcd.cursor_pos=(1,13)
        lcd.write_string(' ')
    
def clean():
    lcd.cursor_pos=(0,13)
    lcd.write_string(' ')
    lcd.cursor_pos=(0,14)
    lcd.write_string(' ')
    lcd.cursor_pos=(0,15)
    lcd.write_string(' ')    
    
current_time()
blinking()
try:
    while True:    
        if blink:
            display_time(True)                    
        else:
            display_time(False)
        clean()
        lcd.cursor_pos=(0,(random.randint(13,15)))
        lcd.write_string('\x07')

except KeyboardInterrupt:
    lcd.clear()
    lcd.cursor_pos=(0,4)
    lcd.write_string('THE  END')
    time.sleep(1)
    lcd.backlight_enabled=False    