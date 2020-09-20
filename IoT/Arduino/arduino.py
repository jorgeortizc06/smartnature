"""
sudo apt install python3-pip
pip3 install pyserial
"""

import serial
import time
import requests
import json

arduino = serial.Serial("COM3", 9600)
"""address = 'http://192.168.0.2:8080/jorgeortiz.smartnature/srv/tipo-planta/eliminarid?id=3'"""
sensor = 'http://localhost:8080/smartnature/srv/sensor/insertar'
device = 'http://localhost:8080/smartnature/srv/device/insertar'
lastParametro = 'http://localhost:8080/smartnature/srv/parametro/last'
headers = {"Content-type": "application/json"}
while True:
    val = arduino.readline()
    print(val)
    humedadAmbiente = val.decode().split(";")[0]
    tempAmbiente = val.decode().split(";")[1]
    humedadSuelo = val.decode().split(";")[2]
    
    
    try:
        datos = {"id":0,"tempAmbiente":float(tempAmbiente),"humedadAmbiente":float(humedadAmbiente),"humedadSuelo":float(humedadSuelo),"fechaCaptura":0}
        print(datos)
        et = requests.post(sensor, data = json.dumps(datos), headers = headers)
        r = requests.get(url = lastParametro, headers = headers)
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
            print("Error en la codificacion de datos")
        
    except:
        print("sin conexion")
arduino.close()
        
