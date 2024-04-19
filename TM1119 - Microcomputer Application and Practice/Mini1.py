import time
import threading
import random
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

blink=False


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

lcd.create_char(0,a)
lcd.create_char(1,b)
lcd.create_char(2,c)
lcd.create_char(3,d)



def welcome():
    lcd.cursor_pos=(0,0)
    lcd.write_string("Mini-Project One")
    lcd.cursor_pos=(1,0)
    lcd.write_string("StopWatch Start!")
    time.sleep(3)
    lcd.clear()
        
def blinking_status():
    global blink
    timer = threading.Timer(0.5,blinking_status) 
    timer.start() 
    blink = not(blink)
'''
def blinking(p,x):
    if blink:
        lcd.cursor_pos=(0,x)
        lcd.write_string("{0:02d}".format(p))
    else:
        lcd.cursor_pos=(0,x)
        lcd.write_string("  ")
        

def add(p):
    if GPIO.input(20)==0:
        p+=1
        if p==60:
            p=0
        time.sleep(0.5)
        print(p)
    return p
'''
def settings():
    global hr, mins, sec
    hr=0
    mins=0
    sec=0
    lcd.cursor_pos=(0,4)
    lcd.write_string("00:00:00")    
    lcd.cursor_pos=(1,0)
    lcd.write_string("SW1:Set  SW2:Add")
    changing = "Seconds"
    
    # Seconds Settings
    while True:
        if GPIO.input(20)==0:
            sec+=1
            if sec==60:
                sec=0
            time.sleep(0.5)
        
        if blink:
            lcd.cursor_pos=(0,10)
            lcd.write_string("{:02d}".format(sec))
        else:
            lcd.cursor_pos=(0,10)
            lcd.write_string("  ")
        
        if GPIO.input(21)==0:
            lcd.cursor_pos=(0,10)
            lcd.write_string("{:02d}".format(sec))
            time.sleep(0.5)
            break
                
    # Minutes Settings
    while True:
        if GPIO.input(20)==0:
            mins+=1
            if mins==60:
                mins=0
            time.sleep(0.5)
        
        if blink:
            lcd.cursor_pos=(0,7)
            lcd.write_string("{:02d}".format(mins))
        else:
            lcd.cursor_pos=(0,7)
            lcd.write_string("  ")
        
        if GPIO.input(21)==0:
            lcd.cursor_pos=(0,7)
            lcd.write_string("{:02d}".format(mins))
            time.sleep(0.5)
            break
    
    # Hours Settings
    while True:
        if GPIO.input(20)==0:
            hr+=1
            time.sleep(0.5)
        
        if blink:
            lcd.cursor_pos=(0,4)
            lcd.write_string("{:02d}".format(hr))
        else:
            lcd.cursor_pos=(0,4)
            lcd.write_string("  ")
        
        if GPIO.input(21)==0:
            lcd.cursor_pos=(0,4)
            lcd.write_string("{:02d}".format(hr))
            time.sleep(0.5)
            break
            
    lcd.cursor_pos=(0,4)
    lcd.write_string("{:02d}:{:02d}:{:02d}".format(hr,mins,sec)) 
    lcd.cursor_pos=(1,0)
    lcd.write_string("---SW1: Start---")

def countdown():
    global hr, mins, sec
    t=hr*60*60+mins*60+sec
    total=t
    
    while True:
        if GPIO.input(21)==0:
            time.sleep(0.5)
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
        if int((t/total*80)//5)<16:
            for i in range(int((t/total*80)//5),16):
                lcd.cursor_pos=(1,i+1)
                lcd.write_string(' ')
        for i in range(int((t/total*80)//5),0,-1):
            lcd.cursor_pos=(1,i-1)
            lcd.write_string('\xff')
        lcd.cursor_pos=(1,int((t/total*80)//5))
        index=[' ','\x00','\x01','\x02','\x03']
        lcd.write_string(index[int((t/total*80)%5)])

    if t==0:
        buzzer.start(0)
        while True:
            for dc in [0,100,0,100,0,100,0,100,0]:
                buzzer.ChangeDutyCycle(dc)
                time.sleep(0.1)
            time.sleep(0.5)


try:
    welcome() 
    blinking_status() 
    settings()
    countdown()

except KeyboardInterrupt:
    buzzer.stop()
    GPIO.cleanup()
    print('End Of Program')                 
