'''
Group 11

ZHANG Huanyu (21098072D)
WU Xiaotao (21097724D)

'''
import time
import threading
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lcd=CharLCD('PCF8574',0x27)
control=[21,20]

GPIO.setup(control,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(18,GPIO.OUT,initial=0)
GPIO.setup(23,GPIO.OUT,initial=0)
GPIO.setup(24,GPIO.OUT,initial=0)
GPIO.setup(25,GPIO.OUT,initial=0)
GPIO.setup(8,GPIO.OUT,initial=0)
GPIO.setup(26,GPIO.OUT,initial=0)

buzzer=GPIO.PWM(26,50)

a=(
    0b10000,
    0b10000,
    0b10000,
    0b10000,
    0b10000,
    0b10000,
    0b10000,
    0b10000
)
b=(
    0b11000,
    0b11000,
    0b11000,
    0b11000,
    0b11000,
    0b11000,
    0b11000,
    0b11000
)
c=(
    0b11100,
    0b11100,
    0b11100,
    0b11100,
    0b11100,
    0b11100,
    0b11100,
    0b11100
)
d=(
    0b11110,
    0b11110,
    0b11110,
    0b11110,
    0b11110,
    0b11110,
    0b11110,
    0b11110
)
e=(
    0b00000,
    0b01010,
    0b01010,
    0b00000,
    0b11111,
    0b00000,
    0b00000,
    0b00000
)
f=(
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

def welcome():
    lcd.cursor_pos=(0,0)
    lcd.write_string("Mini-Project One")
    lcd.cursor_pos=(1,0)
    lcd.write_string("StopWatch Start!")
    time.sleep(2.5)
    lcd.clear()

blink=False        
def blinking_status():
    global blink
    timer = threading.Timer(0.5,blinking_status) 
    timer.start() 
    blink = not(blink)

def buffer():
    time.sleep(0.4)

def adjust(p,x,limit,index):
    global timelist
    while True:
        if GPIO.input(20)==0:
            p+=1
            if limit==True:
                if p==60:
                    p=0
            buffer()
        
        if blink:
            lcd.cursor_pos=(0,x)
            lcd.write_string("{:02d}".format(p))
        else:
            lcd.cursor_pos=(0,x)
            lcd.write_string("  ")
        
        if GPIO.input(21)==0:
            lcd.cursor_pos=(0,x)
            lcd.write_string("{:02d}".format(p))
            buffer()
            timelist[index]=p
            break

def settings():
    global hr, mins, sec, timelist
    hr=0
    mins=0
    sec=0
    timelist=[hr,mins,sec]
    lcd.cursor_pos=(0,4)
    lcd.write_string("00:00:00")    
    lcd.cursor_pos=(1,0)
    lcd.write_string("SW1:Set  SW2:Add")
    
    adjust(sec,10,True,0)
    sec=timelist[0]
    adjust(mins,7,True,1)
    mins=timelist[1]
    adjust(hr,4,False,2)
    hr=timelist[2]
            
    lcd.cursor_pos=(0,4)
    lcd.write_string("{:02d}:{:02d}:{:02d}".format(hr,mins,sec)) 
    lcd.cursor_pos=(1,0)
    lcd.write_string("---SW1: Start---")

def progressbar():
    emoji=['\x05','\x04']
    full=int((t/total*80)//5)
    if full<15:
        lcd.cursor_pos=(1,full+1)
        lcd.write_string(emoji[t%2])
        if full<14:
            for i in range(full,16):
                lcd.cursor_pos=(1,i+2)
                lcd.write_string(' ')
    for i in range(full,0,-1):
        lcd.cursor_pos=(1,i-1)
        lcd.write_string('\xff')
    lcd.cursor_pos=(1,full)
    bar=[' ','\x00','\x01','\x02','\x03']
    lcd.write_string(bar[int((t/total*80)%5)])

def beep(v):
    for dc in [v,0]*4:
        buzzer.ChangeDutyCycle(dc)
        time.sleep(0.1)
    time.sleep(0.5)

def countdown():
    global hr, mins, sec, t, total
    t=hr*60*60+mins*60+sec
    total=t
    
    while True:
        if GPIO.input(21)==0:
            buffer()
            break 
    
    for i in range(16,0,-1):
            lcd.cursor_pos=(1,i-1)
            lcd.write_string('\xff')
    
    while t>0:
        t-=1
        time.sleep(1)
        h=t//(60*60)
        m=t%(60*60)//60
        s=t%60
        lcd.cursor_pos=(0,4)
        lcd.write_string("{:02d}:{:02d}:{:02d}".format(h,m,s))
        
        progressbar()
        
    if t==0:
        buzzer.start(0)
        lcd.cursor_pos=(1,0)
        lcd.write_string('\x05')
        lcd.cursor_pos=(1,1)
        lcd.write_string(" --Time up!----")
        v=20
        while True:
            beep(v)
            lcd.cursor_pos=(1,0)
            lcd.write_string("-SW1/SW2: Reset-")
            if v<100:
                v+=20
            if GPIO.input(21)==0 or GPIO.input(20)==0:
                buzzer.stop()
                buffer()
                break

try:
    welcome() 
    blinking_status()
    while True:
        settings()
        countdown()

except KeyboardInterrupt:
    buzzer.stop()
    GPIO.cleanup()
    lcd.clear()
    lcd.cursor_pos=(0,4)
    lcd.write_string('THE  END')
    time.sleep(1)
    lcd.backlight_enabled=False  
    print('End of Program')                 