#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#include <stdlib.h>
#define DHTTYPE DHT11

//********SENSORES INPUT*********

//**************************************
//*********** MQTT CONFIG **************
//**************************************
const char *mqtt_server = "192.168.0.6";
const int mqtt_port = 1883;
const char *mqtt_user = "nOkjkvS9JJPhbRN";
const char *mqtt_pass = "AlmjrvUeyfxygz4";
const char *root_topic_subscribe = "sala/electrovalvula";
const char *root_topic_publish = "sala";


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
int electrovalvula = 2;
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
  pinMode(sensorAmbiental, INPUT);
  pinMode(humedadSuelo, INPUT);
  pinMode(electrovalvula, OUTPUT);
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
  int suelo1 = map(sensorSuelo1, 0, 4095, 100, 0);
  Serial.print("Humedad Suelo:");
  Serial.print(suelo1);
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
    client.publish("casa/sala/SensorTemperatura1", tempstring);

    char humedAmbstring[3];
    dtostrf(humedAmb,3,1,humedAmbstring);
    client.publish("casa/sala/SensorHumedad1", humedAmbstring);

    char suelo1string[6];
    dtostrf(suelo1,4,1,suelo1string);
    client.publish("casa/sala/SensorSuelo1", suelo1string);
    
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
    digitalWrite(electrovalvula,HIGH);
    Serial.println("Abierta");
  }
  if(incoming.equals("ON")){
    digitalWrite(electrovalvula,LOW);
    Serial.println("Cerrada");
  }
  Serial.println("Mensaje -> " + incoming);

}
