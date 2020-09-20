/*
 * Desarrollado por Jorge Ortiz
 * Fecha: 24/08/2020
 * 
 */

#include <DHT.h>//Libreria del sensor DHT11

int sensorAmbiental = 2; //Pin 2 Digital
float tempAmb, humedadAmb; //Variables para sensor ambiental
const int electrovalvula = 13; //Pin 13 Digital: HIGH O LOW
const int humedadSueloA0 = A0; //Pin A0 analogico.
const int humedadSueloA1 = A1; //Pin A1 analogico.
const int humedadSueloA2 = A2; //Pin A2 analogico.
const int idDevice = 100;
const String device = "Dispositivo codigo 100";

DHT dht (sensorAmbiental, DHT11); //Funcion para dht11

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  dht.begin();

  pinMode(humedadSueloA0, INPUT); //Valores como entrada
  pinMode(humedadSueloA1, INPUT); //Valores como entrada
  pinMode(humedadSueloA2, INPUT); //Valores como entrada
  pinMode(sensorAmbiental, INPUT);
  pinMode(electrovalvula, OUTPUT); //Valores como salida, se abre o cierra
}

void loop() {
  // put your main code here, to run repeatedly:
  /*int lectura = analogRead(A0);
  int sensorDH = analogRead(A1);
  Serial.println("Sensor Suelo: ");
  Serial.println(lectura);
  Serial.println("Sensor Ambiental: ");
  Serial.println(sensorDH);

  int lecturaPorcentaje = map(lectura, 1023, 400, 0, 100);

  Serial.print("La humedad es del: ");
  Serial.print(lecturaPorcentaje);
  Serial.println("%");*/

  int sensorSuelo1 = analogRead(humedadSueloA0);
  int sensorSuelo2 = analogRead(humedadSueloA1);
  int sensorSuelo3 = analogRead(humedadSueloA2);

  int promedioHumedadSuelo = (sensorSuelo1 + sensorSuelo2 + sensorSuelo3) / 3;

  humedadAmb = dht.readHumidity(); //Obtengo la humedad ambiental
  tempAmb = dht.readTemperature(); //Temperatura ambiental

   // Calcular el índice de calor en grados centígrados
  float hic = dht.computeHeatIndex(tempAmb, humedadAmb, false);

  //Serial.print("Temperatura ambiental: "); Serial.print(tempAmb);
  //Serial.print("C Humedad ambiental: "); Serial.print(humedadAmb); Serial.println("%");
  //Verificando error del sensor DHT11
  if(isnan(humedadAmb) || isnan(tempAmb)){
    //Serial.print("Error al obtener datos del sensor DHT11");
    return;
  }
 
  Serial.print(humedadAmb);
  Serial.print(";");
  Serial.print(hic);
  Serial.print(";");
  Serial.print(promedioHumedadSuelo);
  Serial.println();
   
  if (Serial.available()) 
   {
      char parametro = Serial.read();
      if (parametro == '0')
      {
         digitalWrite(electrovalvula, LOW);
      }

      if( parametro == '1'){
        digitalWrite(electrovalvula, HIGH);
      }
   }
  delay(2000);
/*
  if(sensorSuelo >= 700) // el valor que considero seco y hay que regar es de 700
  {
   //Si la tierra está seca, comenzara a regar
   //Riega durante 1 segundo y espera a comprobar la humedad otro segundo
   digitalWrite(electrovalvula, HIGH); //se abre
   delay(2000); //Riego por 2 segundos
   digitalWrite(electrovalvula, LOW); //se cierra
   delay(1000);
  }
  */
}
