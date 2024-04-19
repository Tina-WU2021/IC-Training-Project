# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:50:20 2022

@author: ic2140
"""

import json
import time
import threading
import numpy as np
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import Adafruit_DHT as dht
from RPLCD.i2c import CharLCD

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

adc = Adafruit_ADS1x15.ADS1015()
DHT11_pin = 4
lcd = CharLCD('PCF8574', 0x27)
led = [18, 23, 24, 25, 8]
GPIO.setup(led, GPIO.OUT, initial = 0)

led_status = False

def status():
    global led_status
    
    timer_led = threading.Timer(0.5, status) 
    timer_led.start()
    
    lcd.cursor_pos = (0, 1)
    lcd.write_string("TEAM D02 Node")
    lcd.cursor_pos = (1, 1)
    lcd.write_string("Now Operating!")
    
    led_status = not led_status
    
    if led_status:
        GPIO.output(led, GPIO.HIGH)
    
    else:
        GPIO.output(led, GPIO.LOW)

adc_values = [0] * 4
sound_std = 1050
light_max = 1625

mqtt_broker = "ia.ic.polyu.edu.hk"
mqtt_port = 1883
mqtt_qos = 1
mqtt_client = mqtt.Client("iot-TEAM_D02") 
mqtt_client.connect(mqtt_broker, mqtt_port)
mqtt_topic = "iot/sensor-DEF"

def info():
    timer_info = threading.Timer(60, info) 
    timer_info.start() 
    
    humi, temp = dht.read_retry(dht.DHT11, DHT11_pin)
    for i in range(4):
        adc_values[i] = adc.read_adc(i, gain = 1)
    light = adc_values[3] / light_max * 100
    if adc_values[2] <= 0:
        sound = -99
    else:
        sound = 80 + 20 * np.log(adc_values[2] / sound_std)
    
    data = {
        'node_id': "D02",
        'loc': "W311B",
        'temp': str(temp),
        'hum': str(humi),
        'light': str(round(light + 0.5)),
        'snd': str(round(sound + 0.5))
        }
    data_json = json.dumps(data)
    
    mqtt_client.publish(mqtt_topic, data_json, mqtt_qos)
    
try:
    status()
    info()
          
except KeyboardInterrupt:
    GPIO.cleanup()
    lcd.clear()
    lcd.cursor_pos = (0, 4)
    lcd.write_string('THE  END')
    time.sleep(1)
    lcd.backlight_enabled = False  
    print('End of Program')