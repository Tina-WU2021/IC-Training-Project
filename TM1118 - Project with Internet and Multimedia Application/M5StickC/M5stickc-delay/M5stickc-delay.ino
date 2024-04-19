/*****************************************************************************
Smart IOT Tag to show staff's status
Using ESP8266

This sketch connects the ESP8266 to a MQTT broker and subscribes to the topic 
/IC/TRIAL. When the button is pressed, the client will toggle among publishing
"Available", "Busy", "Online" and "Leave". When the Json message is received, 
the LED matrix displays "A", "B", "O" and "L", respectively. 
*******************************************************************************/


#include <WiFi.h>               // Wifi driver

#include <PubSubClient.h>       // MQTT server library
#include <ArduinoJson.h>        // JSON library
#include <M5StickC.h>
#define ID 9



// MQTT and WiFi set-up
WiFiClient espClient;
PubSubClient client(espClient);


const char *ssid = "icw502g";      // Your SSID             
const char *password = "8c122ase";  // Your Wifi password
//const char *mqtt_server = "mqtt.eclipse.org"; // MQTT server name
const char *mqtt_server = "ia.ic.polyu.edu.hk"; // MQTT server name
char *mqttTopic = "iot/sensor-D02-M5";


byte reconnect_count = 0;
long currentTime = 0;

char msg[100];
String ipAddress;
String macAddr;
String recMsg="";


StaticJsonDocument<200> Jsondata; // Create a JSON document of 200 characters max
StaticJsonDocument<200> jsonBuffer;


class MyRecord{
  public:
      const char* line1 = "loading...";
      const char* line2 = "loading...";
  };
  
MyRecord record[10];

int n = 0;
int cur = 0;

//Set up the Wifi connection
void setup_wifi() {
  byte count = 0;
  
  WiFi.disconnect();
  delay(100);
  // We start by connecting to a WiFi network
  Serial.printf("\nConnecting to %s\n", ssid);
  WiFi.begin(ssid, password); // start the Wifi connection with defined SSID and PW

  // Indicate "......" during connecting
  // Restart if WiFi cannot be connected for 30sec
  currentTime = millis();
  M5.Lcd.setCursor(0,0);
  M5.Lcd.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    M5.Lcd.print(".");
    count++;
    if (count == 6) {
      count = 0;
      M5.Lcd.setCursor(0,0);
      M5.Lcd.print("Connecting       "); //clear the dots
      M5.Lcd.setCursor(0,0);
    }
      
    if (millis()-currentTime > 30000){
      ESP.restart();
    }
  }
  // Show "WiFi connected" once linked and light up LED1
  Serial.printf("\nWiFi connected\n");
  // Show IP address and MAC address
  ipAddress=WiFi.localIP().toString();
  Serial.printf("\nIP address: %s\n", ipAddress.c_str());
  macAddr=WiFi.macAddress();
  Serial.printf("MAC address: %s\n", macAddr.c_str());
  
  //Show in the small TFT
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setCursor(0,0);
  M5.Lcd.print("WiFi connected!");
  delay(3000);
}


void callback(char* topic, byte* payload, unsigned int length) {
  
  recMsg ="";
  for (int i = 0; i < length; i++) {
    recMsg = recMsg + (char)payload[i];
  }
  Serial.println("Received");
  
   DeserializationError error = deserializeJson(jsonBuffer, recMsg);

  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return;
  }
    char a = jsonBuffer["no"];
    n = int(a);
    record[n].line1 = jsonBuffer["line1"];
    record[n].line2 = jsonBuffer["line2"];

  jsonBuffer.clear(); 
  delay(500);

}


// Reconnect mechanism for MQTT Server
void reconnect() {
  // Loop until we're reconnected
  
  while (!client.connected()) {
    Serial.printf("Attempting MQTT connection...");
    // Attempt to connect
    //if (client.connect("ESP32Client")) {
    if (client.connect(macAddr.c_str())) {
      Serial.println("Connected");
      // Once connected, publish an announcement...
      snprintf(msg, 75, "IoT System (%s) is READY", ipAddress.c_str());
      client.subscribe(mqttTopic);
      delay(1000);
      client.publish(mqttTopic, msg);
      reconnect_count = 0;
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      reconnect_count++;
      
      //reconnect wifi by restart if retrial up to 5 times
      if (reconnect_count == 5){
        ESP.restart();//reset if not connected to server 
      }
        
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {  
  Serial.begin(115200); 
  Serial.println("System Start!");  

  M5.begin();
  M5.IMU.Init();
  M5.Lcd.setRotation(3);
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextSize(1);

  setup_wifi();
  
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  //Initalize Json message
  Jsondata["PART"] = ID;
  Jsondata["MOVED"] = "No"; 

  M5.Lcd.setCursor(40, 0);
  M5.Lcd.println("IMU TEST");
  M5.Lcd.setCursor(0, 20);
  M5.Lcd.println("  sensor  venue    tem");
  M5.Lcd.setCursor(0, 50);
  M5.Lcd.println("   hum    light    snd");
  
}

void loop() {
  if (!client.connected()){
    reconnect();
  }
  client.loop();
  
    M5.Lcd.setCursor(0, 30);
    M5.Lcd.printf(record[cur].line1);
    Serial.println(record[cur].line1);
    
    M5.Lcd.setCursor(0, 60);
    M5.Lcd.printf(record[cur].line2);
    Serial.println(record[cur].line2);

    delay(2000);

}
