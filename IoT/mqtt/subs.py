import datetime
import json
import sys
import time

import numpy as np
import paho.mqtt.client
import psycopg2
import requests
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from promedio import calcular_promedio_humedad

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
            #promedioHumedAmbiental = calcular_promedio_humedad('2020-11-4 21:00:00', '2020-11-4 21:10:59', 1, 2)
            r = requests.get(api_plataforma, headers=headers)
            plataforma = r.json()
            # horarios = {'horario1': str(plataforma['horario1']),'horario2': str(plataforma['horario2'])}
            for a in plataforma:
                horarios = {'horario1': a['horario1'], 'horario2': a['horario2']}
            print(horarios)
            for k, v in horarios.items():
                regar(v, float(message.payload), client)

            time.sleep(180)
            print("===============================")

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
        """if message.topic == 'device1/sensorCaudal1':
            sensores = {"value": float(message.payload), "codigo_sensor": int(1), "estado": "A", "tipo_sensor": 4,
                        "device": 1}
            et = requests.post(api_sensor, data=json.dumps(sensores), headers=headers)
        if message.topic == 'device1/sensorConsumoAgua1':
            sensores = {"value": float(message.payload), "codigo_sensor": int(1), "estado": "A", "tipo_sensor": 5,
                        "device": 1}
            et = requests.post(api_sensor, data=json.dumps(sensores), headers=headers)"""

    except:
        print("Error en la coneccion")


# print('payload: ', message.payload)
# print('qos: %d' % message.qos)
def regar(hora, humedad_suelo, client):
    global activacion
    global fin_riego
    print(activacion)
    print(datetime.datetime.now())
    if time.strftime("%H:%M:%S") == '14:45:00' and activacion == False:
        #prom_hum_suelo = calcular_promedio_humedad('2020-11-4 21:00:00', '2020-11-4 21:10:59', 1, 1)
        prom_hum_suelo = 899
        #prom_hum_ambient = calcular_promedio_humedad('2020-11-4 21:00:00', '2020-11-4 21:10:59', 1, 2)
        prom_hum_ambient = 60
        #prom_temp_ambient = calcular_promedio_humedad('2020-11-4 21:00:00', '2020-11-4 21:10:59', 1, 3)
        prom_temp_ambient = 16
        activacion = True
        tiempo_riego = round(fuzzy_logic(float(prom_hum_suelo), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
        print(tiempo_riego)
        ahora = datetime.datetime.now()
        futuro = ahora + datetime.timedelta(minutes=tiempo_riego)
        fin_riego = futuro.strftime("%H:%M:%S")
        print(fin_riego)
        historial_riego = {"tiempo_riego": float(tiempo_riego), "siembra": 1, "tipo_rol": 2}
        et_historial_riego = requests.post(api_historial_riego, data=json.dumps(historial_riego), headers=headers)
        client.publish("device1/electrovalvula", "ON")
    elif time.strftime("%H:%M:%S") == fin_riego and activacion == True:
        print("La llave se ha cerrado")
        activacion = False
        client.publish("device1/electrovalvula", "OFF")


def fuzzy_logic(par_humedad_suelo, par_humedad_ambiental, par_temperatura_ambiental):
    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    humedad = ctrl.Antecedent(np.arange(0, 1024, 1), 'humedad')
    temperatura_ambiental = ctrl.Antecedent(np.arange(-5, 46, 1), 'temperatura_ambiental')
    humedad_ambiental = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad_ambiental')
    tiempo_riego = ctrl.Consequent(np.arange(0, 17, 1), 'tiempo_riego')

    # Auto-membership function population is possible with .automf(3, 5, or 7)
    humedad['seco'] = fuzz.trimf(humedad.universe, [0, 100, 200])
    humedad['semi_seco'] = fuzz.trimf(humedad.universe, [120, 310, 500])
    humedad['humedo'] = fuzz.trimf(humedad.universe, [450, 572, 694])
    humedad['semi_humedo'] = fuzz.trimf(humedad.universe, [658, 725, 792])
    humedad['encharcado'] = fuzz.trimf(humedad.universe, [750, 825, 900])

    temperatura_ambiental['baja'] = fuzz.trimf(temperatura_ambiental.universe, [-5, 2, 10])
    temperatura_ambiental['media'] = fuzz.trimf(temperatura_ambiental.universe, [2, 17, 27])
    temperatura_ambiental['alta'] = fuzz.trimf(temperatura_ambiental.universe, [24, 34, 45])

    humedad_ambiental['baja'] = fuzz.trimf(humedad_ambiental.universe, [0, 16, 33])
    humedad_ambiental['media'] = fuzz.trimf(humedad_ambiental.universe, [16, 41, 66])
    humedad_ambiental['alta'] = fuzz.trimf(humedad_ambiental.universe, [41, 70, 100])

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    tiempo_riego['nada'] = fuzz.trimf(tiempo_riego.universe, [0, 0, 0])
    tiempo_riego['poco'] = fuzz.trimf(tiempo_riego.universe, [0, 2, 4])
    tiempo_riego['medio'] = fuzz.trimf(tiempo_riego.universe, [3, 6, 9])
    tiempo_riego['bastante'] = fuzz.trimf(tiempo_riego.universe, [7, 9, 12])
    tiempo_riego['mucho'] = fuzz.trapmf(tiempo_riego.universe, [10, 13, 17, 17])
    rule1 = ctrl.Rule(humedad['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                      tiempo_riego['nada'])
    rule2 = ctrl.Rule(humedad['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                      tiempo_riego['nada'])
    rule3 = ctrl.Rule(humedad['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                      tiempo_riego['nada'])
    rule4 = ctrl.Rule(humedad['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                      tiempo_riego['nada'])
    rule5 = ctrl.Rule(humedad['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                      tiempo_riego['nada'])
    rule6 = ctrl.Rule(humedad['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                      tiempo_riego['nada'])
    rule7 = ctrl.Rule(humedad['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                      tiempo_riego['nada'])
    rule8 = ctrl.Rule(humedad['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                      tiempo_riego['nada'])
    rule9 = ctrl.Rule(humedad['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                      tiempo_riego['nada'])
    rule10 = ctrl.Rule(humedad['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                       tiempo_riego['nada'])
    rule11 = ctrl.Rule(humedad['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                       tiempo_riego['nada'])
    rule12 = ctrl.Rule(humedad['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                       tiempo_riego['nada'])
    rule13 = ctrl.Rule(humedad['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                       tiempo_riego['poco'])
    rule14 = ctrl.Rule(humedad['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                       tiempo_riego['nada'])
    rule15 = ctrl.Rule(humedad['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                       tiempo_riego['nada'])
    rule16 = ctrl.Rule(humedad['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                       tiempo_riego['medio'])
    rule17 = ctrl.Rule(humedad['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                       tiempo_riego['poco'])
    rule18 = ctrl.Rule(humedad['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                       tiempo_riego['nada'])
    rule19 = ctrl.Rule(humedad['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                       tiempo_riego['nada'])
    rule20 = ctrl.Rule(humedad['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                       tiempo_riego['nada'])
    rule21 = ctrl.Rule(humedad['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                       tiempo_riego['nada'])
    rule22 = ctrl.Rule(humedad['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                       tiempo_riego['poco'])
    rule23 = ctrl.Rule(humedad['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                       tiempo_riego['poco'])
    rule24 = ctrl.Rule(humedad['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                       tiempo_riego['nada'])
    rule25 = ctrl.Rule(humedad['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                       tiempo_riego['medio'])
    rule26 = ctrl.Rule(humedad['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                       tiempo_riego['poco'])
    rule27 = ctrl.Rule(humedad['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                       tiempo_riego['nada'])
    rule28 = ctrl.Rule(humedad['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                       tiempo_riego['poco'])
    rule29 = ctrl.Rule(humedad['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                       tiempo_riego['nada'])
    rule30 = ctrl.Rule(humedad['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                       tiempo_riego['nada'])
    rule31 = ctrl.Rule(humedad['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                       tiempo_riego['bastante'])
    rule32 = ctrl.Rule(humedad['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                       tiempo_riego['medio'])
    rule33 = ctrl.Rule(humedad['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                       tiempo_riego['poco'])
    rule34 = ctrl.Rule(humedad['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                       tiempo_riego['mucho'])
    rule35 = ctrl.Rule(humedad['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                       tiempo_riego['bastante'])
    rule36 = ctrl.Rule(humedad['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                       tiempo_riego['mucho'])
    rule37 = ctrl.Rule(humedad['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                       tiempo_riego['medio'])
    rule38 = ctrl.Rule(humedad['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                       tiempo_riego['medio'])
    rule39 = ctrl.Rule(humedad['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                       tiempo_riego['poco'])
    rule40 = ctrl.Rule(humedad['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                       tiempo_riego['mucho'])
    rule41 = ctrl.Rule(humedad['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                       tiempo_riego['mucho'])
    rule42 = ctrl.Rule(humedad['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                       tiempo_riego['bastante'])
    rule43 = ctrl.Rule(humedad['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                       tiempo_riego['mucho'])
    rule44 = ctrl.Rule(humedad['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                       tiempo_riego['mucho'])
    rule45 = ctrl.Rule(humedad['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                       tiempo_riego['mucho'])

    tipping_ctrl = ctrl.ControlSystem(
        [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15,
         rule16,
         rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30,
         rule31, rule32, rule33, rule34, rule3, rule36,
         rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
    tipping.input['humedad'] = par_humedad_suelo
    tipping.input['humedad_ambiental'] = par_humedad_ambiental
    tipping.input['temperatura_ambiental'] = par_temperatura_ambiental
    tipping.compute()
    print(tipping.output['tiempo_riego'])
    return tipping.output['tiempo_riego']


def main():
    client = paho.mqtt.client.Client(client_id='albert-subs', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host='192.168.100.254', port=1883)
    client.loop_forever(20)


if __name__ == '__main__':
    main()

sys.exit(0)
