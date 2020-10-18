#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#include <stdlib.h>
#include <WiFiManager.h>
#define DHTTYPE DHT11

//********SENSORES INPUT*********

//**************************************
//*********** MQTT CONFIG **************
//**************************************
const char *mqtt_server = "192.168.0.7";
const int mqtt_port = 1883;
const char *mqtt_user = "nOkjkvS9JJPhbRN";
const char *mqtt_pass = "AlmjrvUeyfxygz4";
const char *root_topic_subscribe = "device1/electrovalvula";
const char *topicSensorTemperatura1 = "device1/sensorTemperatura1";
const char *topicSensorHumedad1 = "device1/sensorHumedad1";
const char *topicSensorCaudal1 = "device1/sensorCaudal1";
const char *topicSensorConsumoAgua1 = "device1/sensorConsumoAgua1";
const char *topicSensorSuelo1 = "device1/sensorSuelo1";
const char *topicSensorSuelo2 = "device1/sensorSuelo2";
const char *topicSensorSuelo3 = "device1/sensorSuelo3";
const char *topicSensorSuelo4 = "device1/sensorSuelo4";
const char *topicPromedioSensorSuelo = "device1/promedioSensorSuelo";



//**************************************
//*********** WIFICONFIG ***************
//**************************************
//const char* ssid = "HOWARDS";
//const char* password =  "ALOHOMORA";



//**************************************
//*********** GLOBALES   ***************
//**************************************
WiFiClient espClient;
PubSubClient client(espClient);
int pinElectrovalvula = 15;
int pinSensorAmbiental = 4;
float tempAmb, humedAmb, f;
int pinHumedadSuelo1 = 32;
int pinHumedadSuelo2 = 33;
int pinHumedadSuelo3 = 34;
int pinHumedadSuelo4 = 35;
//Para medir el consumo de agua
const int sensorPin = 5;
const int measureInterval = 2500;
volatile int pulseConter;
// YF-S201
const float factorK = 7.5;
// FS300A
//const float factorK = 5.5;
// FS400A
//const float factorK = 3.5;
float volume = 0;
long t0 = 0;
DHT dht(pinSensorAmbiental, DHTTYPE);
char msg[25];

//************************
//** F U N C I O N E S ***
//************************
void callback(char* topic, byte* payload, unsigned int length);
void reconnect();
//void setup_wifi();
//Calcular consumo de agua
void ISRCountPulse()
{
   pulseConter++;
}
 
float GetFrequency()
{
   pulseConter = 0;
 
   interrupts();
   delay(measureInterval);
   noInterrupts();
 
   return (float)pulseConter * 1000 / measureInterval;
}
 
void SumVolume(float dV)
{
   volume += dV / 60 * (millis() - t0) / 1000.0;
   t0 = millis();
}
void setup() {
  Serial.begin(9600);
  //setup_wifi();
  attachInterrupt(digitalPinToInterrupt(sensorPin), ISRCountPulse, RISING);
  t0 = millis();
  WiFiManager wifiManager;
  wifiManager.autoConnect("AutoConnectAP");
  Serial.println("connected...yeey :)");
  pinMode(pinSensorAmbiental, INPUT);
  pinMode(pinHumedadSuelo1, INPUT);
  pinMode(pinHumedadSuelo2, INPUT);
  pinMode(pinHumedadSuelo3, INPUT);
  pinMode(pinHumedadSuelo4, INPUT);
  pinMode(pinElectrovalvula, OUTPUT);
  digitalWrite(pinElectrovalvula,HIGH);
  dht.begin();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback); //Cuando llega un mensaje
  
  
}

void loop() {
  
  if (!client.connected()) {
    reconnect();
  }
  
  client.loop();

  // obtener frecuencia en Hz
   float frequency = GetFrequency();
 
   // calcular caudal L/min
   float flow_Lmin = frequency / factorK;
   SumVolume(flow_Lmin);
 
   Serial.print(" Caudal: ");
   Serial.print(flow_Lmin, 3);
   Serial.print(" (L/min)\tConsumo:");
   Serial.print(volume, 1);
   Serial.println(" (L)");

  tempAmb = dht.readTemperature();
  humedAmb = dht.readHumidity();
  
  if (isnan(humedAmb) || isnan(tempAmb)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(1000); // wait a bit
    return;
  }
  int const readSensorSuelo1 = analogRead(pinHumedadSuelo1);
  int const readSensorSuelo2 = analogRead(pinHumedadSuelo2);
  int const readSensorSuelo3 = analogRead(pinHumedadSuelo3);
  int const readSensorSuelo4 = analogRead(pinHumedadSuelo4);
  int const promedioSensorSuelo = (readSensorSuelo1+readSensorSuelo2+readSensorSuelo3+readSensorSuelo4)/4;
  Serial.print("Humedad Suelo1:");
  Serial.print(readSensorSuelo1);
  Serial.print("Humedad Suelo2:");
  Serial.print(readSensorSuelo2);
  Serial.print("Humedad Suelo3:");
  Serial.print(readSensorSuelo3);
  Serial.print("Humedad Suelo4:");
  Serial.print(readSensorSuelo4);
  Serial.print("Promedio Humedad Suelo:");
  Serial.print(promedioSensorSuelo);
  Serial.print(" Temperatura Ambiental:");
  Serial.print(tempAmb);
  Serial.print(" Humedad Ambiental:");
  Serial.print(humedAmb);
  Serial.println();

  
  if (client.connected()){
    //String str = "La cuenta es -> " + String(count);
    //str.toCharArray(msg,25);
    char tempstring[3];
    dtostrf(tempAmb,3,1,tempstring);
    client.publish(topicSensorTemperatura1, tempstring);

    char humedAmbstring[3];
    dtostrf(humedAmb,3,1,humedAmbstring);
    client.publish(topicSensorHumedad1, humedAmbstring);

    char humedadSuelo1string[6];
    dtostrf(readSensorSuelo1,6,1,humedadSuelo1string);
    client.publish(topicSensorSuelo1, humedadSuelo1string);

    char humedadSuelo2string[6];
    dtostrf(readSensorSuelo2,6,1,humedadSuelo2string);
    client.publish(topicSensorSuelo2, humedadSuelo2string);

    char humedadSuelo3string[6];
    dtostrf(readSensorSuelo3,6,1,humedadSuelo3string);
    client.publish(topicSensorSuelo3, humedadSuelo3string);
    
    char humedadSuelo4string[6];
    dtostrf(readSensorSuelo4,6,1,humedadSuelo4string);
    client.publish(topicSensorSuelo4, humedadSuelo4string);

    char promedioHumedadSuelostring[6];
    dtostrf(promedioSensorSuelo,6,1,promedioHumedadSuelostring);
    client.publish(topicPromedioSensorSuelo, promedioHumedadSuelostring);

    char caudalAguastring[6];
    dtostrf(flow_Lmin,4,1,caudalAguastring);
    client.publish(topicSensorCaudal1, caudalAguastring);

    char consumoAguastring[6];
    dtostrf(volume,4,1,consumoAguastring);
    client.publish(topicSensorConsumoAgua1, consumoAguastring);
    
    delay(1000);
  }
  
}




//*****************************
//***    CONEXION WIFI      ***
//*****************************
/*void setup_wifi(){
  delay(10);
  // Nos conectamos a nuestra red Wifi
  Serial.println();
  Serial.print("Conectando a ssid: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Conectado a red WiFi!");
  Serial.println("Dirección IP: ");
  Serial.println(WiFi.localIP());
}*/



//*****************************
//***    CONEXION MQTT      ***
//*****************************

void reconnect() {

  while (!client.connected()) {
    Serial.print("Intentando conexión Mqtt...");
    // Creamos un cliente ID
    String clientId = "RIEGO";
    clientId += String(random(0xffff), HEX);
    // Intentamos conectar
    if (client.connect(clientId.c_str(),mqtt_user,mqtt_pass)) {
      Serial.println("Conectado!");
      // Nos suscribimos
      if(client.subscribe(root_topic_subscribe)){
        Serial.println("Suscripcion ok");
      }else{
        Serial.println("fallo Suscripciión");
      }
    } else {
      Serial.print("falló :( con error -> ");
      Serial.print(client.state());
      Serial.println(" Intentamos de nuevo en 5 segundos");
      delay(5000);
    }
  }
}


//*****************************
//***       CALLBACK        ***
//*****************************

void callback(char* topic, byte* payload, unsigned int length){
  String incoming = "";
  Serial.print("Mensaje recibido desde -> ");
  Serial.print(topic);
  Serial.println("");
  for (int i = 0; i < length; i++) {
    incoming += (char)payload[i];
  }
  incoming.trim(); //el rele funciona al revez, jqc 3ff sz
  if(incoming.equals("OFF")){
    digitalWrite(pinElectrovalvula,HIGH);
    Serial.println("CERRADA");
  }
  if(incoming.equals("ON")){
    digitalWrite(pinElectrovalvula,LOW);
    Serial.println("ABIERTA");
  }
  Serial.println("Mensaje -> " + incoming);

}
