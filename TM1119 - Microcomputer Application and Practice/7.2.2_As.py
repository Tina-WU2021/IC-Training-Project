import time
import Adafruit_DHT

DHT_SENSOR=Adafruit_DHT.DHT11
DHT_PIN=4

try:
    Adafruit_DHT.DHT11=1
except NotImplementedError:
    Adafruit_DHT.DHT11=None
try:
    i = 0
    while True:
        humidity,temperature=Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
        if humidity is not None and temperature is not None:
            t = time.asctime(time.localtime(time.time()))
            f=open("/home/pi/Desktop/Demo_code/Assignment 7.2_log.txt","a")
            f.write("Time: {} | TEMP:{:0.1f}C | Humidity:{:0.1f}%\n".format(t,temperature,humidity))
            f.close()
        else:
            print('Sensor failure. Check wiring')
        i+=1
        time.sleep(3)
        if i == 19:
            break
        
except KeyboardInterrupt: 
    print('End of Program')