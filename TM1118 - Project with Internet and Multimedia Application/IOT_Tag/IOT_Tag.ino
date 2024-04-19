#include <SPI.h>
#include <ButtonDebounce.h>     // Button Debounce library
#include <ESP8266WiFi.h>        // 8266 Wifi driver
#include <PubSubClient.h>       // MQTT server library
#include <ArduinoJson.h>        // JSON library
#include "LedMatrix.h"          // LED control library

#define NUMBER_OF_DEVICES 1
#define CS_PIN D4

#define red_light_pin D0    // red light is connected to D0
#define green_light_pin D8  // green light is connected to D8
#define blue_light_pin D3   // blue light is connected to D3
#define TRIG D2             // swith is connected to D2
#define ID 5

LedMatrix ledMatrix = LedMatrix(NUMBER_OF_DEVICES, CS_PIN);

// MQTT and WiFi set-up
WiFiClient espClient;
PubSubClient client(espClient); // Open an MQTT client

// Key debounce set-up
ButtonDebounce trigger(TRIG, 100);

//const char *ssid = "EIA-W311MESH";              // Your SSID             
//const char *password = "42004200";              // Your Wifi password
const char *ssid = "icw502g";                     // Your SSID             
const char *password = "8c122ase";                // Your Wifi password
const char *mqtt_server = "ia.ic.polyu.edu.hk";   // MQTT server name
char *mqttTopic = "iot/sensor-D02";               // Topic to subscribe to    

byte reconnect_count = 0;
int count = 0;
long int currentTime = 0;

char msg[200];
String ipAddress;
String macAddr;
String recMsg="";
String currentmsg="Team D02 IOT Tag";

int buttonState;      // variable to hold the button state
int Mode = 0;         // what mode is the light in?
boolean keypress = 1;
int x = 0;

const char* msgCurtain="2";
const char* message="Team D02 IOT Tag";

StaticJsonDocument<50> Jsondata; // Create a JSON document of 200 characters max
StaticJsonDocument<100> jsonBuffer; 


//Set up the Wifi connection
void setup_wifi() {
  WiFi.disconnect();
  delay(100);
  // We start by connecting to a WiFi network
  Serial.printf("\nConnecting to %s\n", ssid);
  WiFi.begin(ssid, password); // start the Wifi connection with defined SSID and PW

  // Indicate "......" during connecting and flashing LED1
  // Restart if WiFi cannot be connected for 30sec
  currentTime = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    digitalWrite(green_light_pin,LOW);
    digitalWrite(red_light_pin,digitalRead(red_light_pin)^1);
    if (millis()-currentTime > 30000){
      ESP.restart();
    }
  }
  // Show "WiFi connected" once linked and light up LED1
  Serial.printf("\nWiFi connected\n");
  digitalWrite(green_light_pin,LOW);
  delay(2000);
  digitalWrite(green_light_pin,HIGH);
  
  // Show IP address and MAC address
  ipAddress=WiFi.localIP().toString();
  Serial.printf("\nIP address: %s\n", ipAddress.c_str());
  macAddr=WiFi.macAddress();
  Serial.printf("MAC address: %s\n", macAddr.c_str());
}

// Routine to receive message from MQTT server
void callback(char* topic, byte* payload, unsigned int length) {
  recMsg ="";
  for (int i = 0; i < length; i++) {
    recMsg = recMsg + (char)payload[i];
  }
  
  DeserializationError error = deserializeJson(jsonBuffer, recMsg);

  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return;
  }

  msgCurtain = jsonBuffer["status"];
  message = jsonBuffer["message"];
  currentmsg = message;
  
  ledMatrix.setText(currentmsg);
  ledMatrix.commit();

  Serial.print(msgCurtain);
  Serial.println(message);


  //Check the curtain and value#
  if ((strcmp(msgCurtain, "0") == 0) ) {
       digitalWrite(red_light_pin, HIGH);
       digitalWrite(green_light_pin, LOW);
       digitalWrite(blue_light_pin, HIGH);
       Mode=0;
  }

  else if ((strcmp(msgCurtain, "1") == 0) ) {
       digitalWrite(red_light_pin, LOW); // Red
       digitalWrite(green_light_pin, HIGH);
       digitalWrite(blue_light_pin, HIGH);
       Mode=1;
  }

  //Clear the buffer
  jsonBuffer.clear();
  
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
      snprintf(msg, 75, "Team D02 IoT Tag (IP Address: %s) is READY", ipAddress.c_str());
      client.subscribe(mqttTopic);
      delay(1000);
      client.publish(mqttTopic, msg);
      reconnect_count = 0;
    } 
    else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      reconnect_count++;
      
      //Reconnect wifi by restart if retrial up to 5 times
      if (reconnect_count == 5){
        ESP.restart(); // Reset if not connected to server 
      }
        
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// Button control
void buttonChanged(int state){
  if (digitalRead(TRIG)== 0 && keypress==1) {  // If key is pressed and last key is processed
    if (x==0) {
      x=1;
    }
    else if (x==1) {
      ledMatrix.setText(currentmsg);
      x=0;
    }
  }
}


void setup() {
  pinMode(TRIG, INPUT_PULLUP);          // Configure TRIG as an pull-up input
  pinMode(red_light_pin, OUTPUT);
  pinMode(green_light_pin, OUTPUT);
  pinMode(blue_light_pin, OUTPUT);
  
  digitalWrite(red_light_pin, HIGH);
  digitalWrite(green_light_pin, HIGH);
  digitalWrite(blue_light_pin, HIGH);

  buttonState = digitalRead(TRIG);      // Read the initial state
  
  Serial.begin(115200);                 // State serial communication at 115200 baud
  Serial.println("System Start!");

  //Initiate the display first
  ledMatrix.init();                             // Initialize the SPI interface
  ledMatrix.setIntensity(4);                    // Light intensity: 0 - 15
  ledMatrix.clear();
  //ledMatrix.setTextAlignment(TEXT_ALIGN_LEFT);  // Text is aligned to left side of the display

  //Initial state is available
  digitalWrite(green_light_pin, LOW);
  digitalWrite(red_light_pin, HIGH);
  digitalWrite(blue_light_pin, HIGH);
  
  client.setCallback(callback);
  trigger.setCallback(buttonChanged);

  ledMatrix.setText(currentmsg);

  setup_wifi();                         // Connect to network
  digitalWrite(green_light_pin, LOW);
  client.setServer(mqtt_server, 1883);

  //Initalize Json message
  Jsondata["status"] = "0";
  Jsondata["message"] = "Normal Status";  
}

void loop() {
  trigger.update();
  if (!client.connected()){  // Reconnect if connection is lost
    digitalWrite(green_light_pin, LOW);
    digitalWrite(red_light_pin, LOW);
    digitalWrite(blue_light_pin, HIGH);
    currentmsg = "- Connecting -";
    ledMatrix.setNextText(currentmsg);
    Mode=2;
    reconnect();
  }
  client.loop();
  // Now do whatever the lightMode indicates

  if (Mode!=0) {
    digitalWrite(red_light_pin,digitalRead(red_light_pin)^1);
  }

  ledMatrix.clear();
  if (x==0) {
    ledMatrix.scrollTextLeft();
  }
  
  if (x==1) {
    ledMatrix.setText("");    
  }
  delay(60);
  ledMatrix.drawText();
  ledMatrix.commit();
  
}
