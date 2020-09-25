#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#include <stdlib.h>
#define DHTTYPE DHT22

//********SENSORES INPUT*********

//**************************************
//*********** MQTT CONFIG **************
//**************************************
const char *mqtt_server = "ioticos.org";
const int mqtt_port = 1883;
const char *mqtt_user = "nOkjkvS9JJPhbRN";
const char *mqtt_pass = "AlmjrvUeyfxygz4";
const char *root_topic_subscribe = "ZWTjfeO8oyRdP35/electrovalvula";
const char *root_topic_publish = "ZWTjfeO8oyRdP35";


//**************************************
//*********** WIFICONFIG ***************
//**************************************
const char* ssid = "HOWARDS";
const char* password =  "ALOHOMORA";



//**************************************
//*********** GLOBALES   ***************
//**************************************
WiFiClient espClient;
PubSubClient client(espClient);
int sensorAmbiental = 23;
float tempAmb, humedAmb, f;
int humedadSuelo = 34;
DHT dht(sensorAmbiental, DHTTYPE);
char msg[25];

//************************
//** F U N C I O N E S ***
//************************
void callback(char* topic, byte* payload, unsigned int length);
void reconnect();
void setup_wifi();

void setup() {
  Serial.begin(9600);
  setup_wifi();
  dht.begin();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback); //Cuando llega un mensaje
  
}

void loop() {
  
  if (!client.connected()) {
    reconnect();
  }

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

  
  if (client.connected()){
    //String str = "La cuenta es -> " + String(count);
    //str.toCharArray(msg,25);
    char tempstring[3];
    dtostrf(tempAmb,3,1,tempstring);
    client.publish("ZWTjfeO8oyRdP35/sala/SensorTemperatura1",tempstring);

    char humedAmbstring[3];
    dtostrf(humedAmb,3,1,humedAmbstring);
    client.publish("ZWTjfeO8oyRdP35/sala/SensorHumedad1",humedAmbstring);

    char sensorSuelo1string[6];
    dtostrf(sensorSuelo1,6,1,sensorSuelo1string);
    client.publish("ZWTjfeO8oyRdP35/sala/SensorSuelo1",sensorSuelo1string);
    
    delay(1000);
  }
  client.loop();
}




//*****************************
//***    CONEXION WIFI      ***
//*****************************
void setup_wifi(){
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
}



//*****************************
//***    CONEXION MQTT      ***
//*****************************

void reconnect() {

  while (!client.connected()) {
    Serial.print("Intentando conexión Mqtt...");
    // Creamos un cliente ID
    String clientId = "IOTICOS_H_W_";
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
  incoming.trim();
  Serial.println("Mensaje -> " + incoming);

}
