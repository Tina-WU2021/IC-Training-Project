from flask import Flask, render_template
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import time
from RPLCD.i2c import CharLCD
 
app = Flask(__name__, template_folder="template")
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led={'led6':18,
     'led5':23,
     'led4':24,
     'led3':25,
     'led2':8
}
DHT11_pin = 4
lcd=CharLCD('PCF8574',0x27)
 
GPIO.setup(18,GPIO.OUT,initial=0)
GPIO.setup(23,GPIO.OUT,initial=0)
GPIO.setup(24,GPIO.OUT,initial=0)
GPIO.setup(25,GPIO.OUT,initial=0)
GPIO.setup(8,GPIO.OUT,initial=0)
GPIO.setup(26,GPIO.OUT,initial=0)
buzzer=GPIO.PWM(26,50)
 
@app.route("/")
 
def main():
   return render_template('Mini3_Group11.html')
 
@app.route("/<pin>/<action>")
def action(pin, action):
   temperature = ''
   humidity = ''
   if pin == "buzzer":
       if action == "on":
           buzzer.start(100)
    
       if action == "off":
           buzzer.stop()
   
   if pin in led:
       if action == "on":
           GPIO.output(led[pin], GPIO.HIGH)
    
       if action == "off":
           GPIO.output(led[pin], GPIO.LOW)
 
   if pin == "dhtpin" and action == "get":
      humi, temp = dht.read_retry(dht.DHT11, DHT11_pin)  # Reading humidity and temperature
      temperature = 'Temperature: ' + '{0:0.1f}' .format(temp) 
      humidity =  'Humidity: ' + '{0:0.1f}' .format(humi)
      t = time.asctime(time.localtime(time.time()))
      f=open("Mini_project_3_log.txt","a")
      f.write("Time: {} | TEMP:{:0.1f}C | Humidity:{:0.1f}%\n".format(t,temp,humi))
      f.close() 
      lcd.cursor_pos=(0,0)
      lcd.write_string('TEMP={0:0.1f}C'.format(temp))
      lcd.cursor_pos=(1,0)
      lcd.write_string('Humidity={0:0.1f}%'.format(humi))
 
   templateData = {
   'temperature' : temperature,
   'humidity' : humidity
   }
   

   
   return render_template('Mini3_Group11.html', **templateData)
 
if __name__ == "__main__":
   app.run(host='10.0.0.2', port=70, debug=True)

if KeyboardInterrupt:
    buzzer.stop()
    GPIO.cleanup()
    lcd.clear()
    lcd.cursor_pos=(0,4)
    lcd.write_string('THE  END')
    time.sleep(1)
    lcd.backlight_enabled=False  
    print('End of Program') 