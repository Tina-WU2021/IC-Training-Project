import paho.mqtt.client as mqtt
from .models import Event
import json
import datetime
import threading

mqtt_broker = "ia.ic.polyu.edu.hk" # Broker
mqtt_port = 1883 # Default
mqtt_qos = 1 # Quality of Service = 1
mqtt_topic = "iot/sensor-DEF"
mqtt_topic_tag = "iot/sensor-D02"
mqtt_topic_m5 = "iot/sensor-D02-M5"
latest = {}
report = {}

def mqtt_on_message(client, userdata, msg):
    # Do something
    d_msg = str(msg.payload.decode("utf-8"))
    try:
        iotData = json.loads(d_msg)
        p = Event(node_id=iotData["node_id"], node_loc=iotData["loc"], temp=float(iotData["temp"]), hum=float(iotData['hum']), light=float(iotData['light']), snd = float(iotData['snd']))
        latest[iotData["node_id"]] = iotData
        p.save()
        
    except:
        pass

def datareport():
    timer = threading.Timer(60, datareport) 
    timer.start()

    hr_now = int(datetime.datetime.now().strftime("%H"))
    if hr_now >= 23 or hr_now <= 6:
        night = True
    else:
        night = False

    report = {'status': "0", "message": ""}

    for data in latest.values():
        msg = ""
        unusual = False
        if float(data['temp']) > 26:
            unusual = True
            msg += "High Temp"
        elif float(data['temp']) < 20:
            unusual = True
            msg += "Low Temp"

        if night:
            if float(data['light']) >= 55:
                if msg != "":
                    msg += ", "
                unusual = True
                msg += "Light"

            if float(data['snd']) >= 20:
                if msg != "":
                    msg += ", "
                unusual = True
                msg += "Sound"

        if unusual:
            msg += "@{}".format(data['loc'])
            report['status'] = "1"
            report['message'] += msg
    
    if report['status'] == "0":
        report['message'] = "Normal Status"

    report_json = json.dumps(report)
    mqtt_client.publish(mqtt_topic_tag, report_json, mqtt_qos)
    
    datalist = sorted(latest.items())
    for i in range(len(datalist)):
        tmp = datalist[i][1]
        space1 = round((25 - len(tmp['node_id']  + str(tmp['loc']) + str(tmp['temp']))) / 3)
        line1 = " "*round(space1/2) + tmp['node_id'] + " "*space1 + str(tmp['loc']) + " "*space1 + str(tmp['temp'])
        line1 += " "*(25-len(line1))
        space2 = round((25 - len(str(tmp['hum'])  + str(tmp['light']) + str(tmp['snd']))) / 3)
        line2 = " "*round(space2/2) + str(tmp['hum']) + " "*space2 + str(tmp['light']) + " "*space2 + str(tmp['snd'])
        line2 += " "*(25-len(line2))
        data_dict = {"no": str(i), "line1": line1, "line2": line2}
        data_json = json.dumps(data_dict)
        mqtt_client.publish(mqtt_topic_m5, data_json, mqtt_qos)

try:
    mqtt_client = mqtt.Client("django-Team_D02") # Create a Client Instance
    mqtt_client.on_message = mqtt_on_message
    mqtt_client.connect(mqtt_broker, mqtt_port) # Establish a connection to a broker
    print("Connect to MQTT broker")
    mqtt_client.subscribe(mqtt_topic, mqtt_qos)
    mqtt_client.loop_start()
    datareport()

except:
    print("MQTT Server Error")