"""
sudo apt install python3-pip
pip3 install pyserial
"""

import serial
import time
import requests
import json

arduino = serial.Serial("/dev/ttyACM0", 9600)
"""address = 'http://192.168.0.2:8080/jorgeortiz.smartnature/srv/tipo-planta/eliminarid?id=3'"""
sensor = 'http://127.0.0.1:8000/gestion_riego/srv/sensor/list/'
headers = {"Content-type": "application/json"}

while True:
    val = arduino.readline()
    if val:
        print(val)
        humedadAmbiente = val.decode().split(";")[0]
        tempAmbiente = val.decode().split(";")[1]
        humedadSuelo = val.decode().split(";")[2]
        
        
        try:
            datos = {"temp_ambiente":float(tempAmbiente),"humed_ambiente":float(humedadAmbiente),"humed_suelo":float(humedadSuelo)}
            print(datos)
            et = requests.post(sensor, data = json.dumps(datos), headers = headers)
            """r = requests.get(url = lastParametro, headers = headers)
            datos = r.json()
            estado = datos['estado']
            con = str(datos['estado'])
            print(con.encode())
            if estado == 0:
                print("Cierro la llave")
                arduino.write(con.encode())
                arduino.close
            elif estado == 1:
                print("Abro la llave")
                arduino.write(con.encode())
                arduino.close
            else:
                print("Error en la codificacion de datos")"""
        except:
            print("sin conexion")
    else:
        print("Error de lectura del puerto")
arduino.close()
        
