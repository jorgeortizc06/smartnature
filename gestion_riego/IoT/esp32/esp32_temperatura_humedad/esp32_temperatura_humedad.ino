//Ejemplo MQTT & ESP32 con sensor de temperatura DHT22 by Biblioman
#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#include <stdlib.h>

#define DHTTYPE DHT22
const char* ssid = "HOWARDS";
const char* password =  "ALOHOMORA";
const char* mqttServer = "192.168.0.11";
const int mqttPort = 1883;
const char* mqttUser = "dqyoxjgo";
const char* mqttPassword = "tyzFA$ye4FW8";
int sensorAmbiental = 23;
float tempAmb, humedAmb, f;
int humedadSuelo = 34;
 
WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(sensorAmbiental, DHTTYPE);
 
void setup() {
 
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  dht.begin();
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Conectando a red WiFi...");
  }
 
  Serial.println("Conectado a la red WiFi");
 
  client.setServer(mqttServer, mqttPort);
 
  while (!client.connected()) {
    Serial.println("Conectando a Broquer MQTT...");
 
    if (client.connect("ESP32", mqttUser, mqttPassword )) {
 
      Serial.println("conectado");
 
    } else {
 
      Serial.print("conexion fallida ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }
 
 
 
}
 
void loop() {
  tempAmb = dht.readTemperature();
  humedAmb = dht.readHumidity();
  if (isnan(humedAmb) || isnan(tempAmb)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(1000); // wait a bit
    return;
  }

  int const sensorSuelo1 = analogRead(humedadSuelo);
  Serial.print("Humedad Suelo:");
  Serial.print(sensorSuelo1);
  Serial.print(" Temperatura Ambiental:");
  Serial.print(tempAmb);
  Serial.print(" Humedad Ambiental:");
  Serial.print(humedAmb);
  Serial.println();
  
  char tempstring[3];
  dtostrf(tempAmb,3,1,tempstring);
  client.publish("casa/sala/SensorTemperatura1", tempstring);
  
  char humedAmbstring[3];
  dtostrf(humedAmb,3,1,humedAmbstring);
  client.publish("casa/sala/SensorHumedad1", humedAmbstring);

  char sensorSuelo1string[6];
  dtostrf(sensorSuelo1,6,1,sensorSuelo1string);
  client.publish("casa/sala/SensorSuelo1", sensorSuelo1string);
 
  client.loop();
  delay(1000);
}
