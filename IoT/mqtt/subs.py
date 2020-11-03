import datetime
import json
import sys
import time

import numpy as np
import paho.mqtt.client
import requests
import skfuzzy as fuzz
from skfuzzy import control as ctrl

api_sensor = 'http://127.0.0.1:8000/gestion_riego/srv/sensor/'
api_historial_riego = 'http://127.0.0.1:8000/gestion_riego/srv/historial_riego/'
api_plataforma = 'http://127.0.0.1:8000/gestion_riego/srv/plataforma/'
headers = {"Content-type": "application/json"}
activacion = False
fin_riego = ''


# horarios = {'horario1':'8:00', 'horario2:':'17:12'}
def on_connect(client, userdata, flags, rc):
    print('connected (%s)' % client._client_id)
    client.subscribe(topic='device1/#', qos=2)


def on_message(client, userdata, message):
    # valor = float(message.payload)
    # print('----------------------')
    # print('topic: %s' % message.topic)
    try:
        if message.topic == 'device1/promedioSensorSuelo':

            r = requests.get(api_plataforma, headers=headers)
            plataforma = r.json()
            # horarios = {'horario1': str(plataforma['horario1']),'horario2': str(plataforma['horario2'])}
            for a in plataforma:
                horarios = {'horario1': a['horario1'], 'horario2': a['horario2']}
            print(horarios)
            for k, v in horarios.items():
                regar(v, float(message.payload), client)

        if message.topic == 'device1/sensorSuelo1':
            sensores = {"value": float(message.payload), "codigo_sensor": int(1), "estado": "A", "tipo_sensor": 1,
                        "device": 1}
            et_sensores = requests.post(api_sensor, data=json.dumps(sensores), headers=headers)
        if message.topic == 'device1/sensorSuelo2':
            sensores = {"value": float(message.payload), "codigo_sensor": int(2), "estado": "A", "tipo_sensor": 1,
                        "device": 1}
            et = requests.post(api_sensor, data=json.dumps(sensores), headers=headers)
        if message.topic == 'device1/sensorSuelo3':
            sensores = {"value": float(message.payload), "codigo_sensor": int(3), "estado": "A", "tipo_sensor": 1,
                        "device": 1}
            et = requests.post(api_sensor, data=json.dumps(sensores), headers=headers)
        if message.topic == 'device1/sensorSuelo4':
            sensores = {"value": float(message.payload), "codigo_sensor": int(4), "estado": "A", "tipo_sensor": 1,
                        "device": 1}
            et = requests.post(api_sensor, data=json.dumps(sensores), headers=headers)
        if message.topic == 'device1/sensorHumedad1':
            sensores = {"value": float(message.payload), "codigo_sensor": int(1), "estado": "A", "tipo_sensor": 2,
                        "device": 1}
            et = requests.post(api_sensor, data=json.dumps(sensores), headers=headers)
        if message.topic == 'device1/sensorTemperatura1':
            sensores = {"value": float(message.payload), "codigo_sensor": int(1), "estado": "A", "tipo_sensor": 3,
                        "device": 1}
            et = requests.post(api_sensor, data=json.dumps(sensores), headers=headers)
        if message.topic == 'device1/sensorCaudal1':
            sensores = {"value": float(message.payload), "codigo_sensor": int(1), "estado": "A", "tipo_sensor": 4,
                        "device": 1}
            et = requests.post(api_sensor, data=json.dumps(sensores), headers=headers)
        if message.topic == 'device1/sensorConsumoAgua1':
            sensores = {"value": float(message.payload), "codigo_sensor": int(1), "estado": "A", "tipo_sensor": 5,
                        "device": 1}
            et = requests.post(api_sensor, data=json.dumps(sensores), headers=headers)
    except:
        print("Error en la coneccion")


# print('payload: ', message.payload)
# print('qos: %d' % message.qos)

def regar(hora, humedad_suelo, client):
    global activacion
    global fin_riego
    print(activacion)
    if time.strftime("%H:%M") == hora and activacion == False:
        activacion = True
        tiempo_riego = round(fuzzy_logic(humedad_suelo), 2)
        ahora = datetime.datetime.now()
        futuro = ahora + datetime.timedelta(minutes=tiempo_riego)
        fin_riego = futuro.strftime("%H:%M")
        print(fin_riego)
        historial_riego = {"tiempo_riego": float(tiempo_riego), "siembra": 1, "tipo_rol": 2}
        et_historial_riego = requests.post(api_historial_riego, data=json.dumps(historial_riego), headers=headers)
        client.publish("device1/electrovalvula", "ON")
    elif time.strftime("%H:%M") == fin_riego and activacion == True:
        print("La llave se ha cerrado")
        activacion = False
        client.publish("device1/electrovalvula", "OFF")


def fuzzy_logic(humedadSuelo):
    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    humedad = ctrl.Antecedent(np.arange(0, 4096, 1), 'humedad')
    tiempo_riego = ctrl.Consequent(np.arange(0, 16, 1), 'tiempo_riego')

    # Auto-membership function population is possible with .automf(3, 5, or 7)
    humedad.automf(3)

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    tiempo_riego['low'] = fuzz.trimf(tiempo_riego.universe, [0, 1, 2])
    tiempo_riego['medium'] = fuzz.trimf(tiempo_riego.universe, [1, 4, 8])
    tiempo_riego['high'] = fuzz.trimf(tiempo_riego.universe, [4, 9, 15])
    rule1 = ctrl.Rule(humedad['poor'], tiempo_riego['low'])
    rule2 = ctrl.Rule(humedad['average'], tiempo_riego['medium'])
    rule3 = ctrl.Rule(humedad['good'], tiempo_riego['high'])
    tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
    tipping.input['humedad'] = humedadSuelo
    tipping.compute()
    print(tipping.output['tiempo_riego'])
    return tipping.output['tiempo_riego']


def main():
    client = paho.mqtt.client.Client(client_id='albert-subs', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host='192.168.0.254', port=1883)
    client.loop_forever()


if __name__ == '__main__':
    main()

sys.exit(0)
