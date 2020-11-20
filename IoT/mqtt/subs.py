import json
import sys
import time
import paho.mqtt.client
import requests

api_sensor = 'http://127.0.0.1:8000/gestion_riego/srv/sensor/'
headers = {"Content-type": "application/json"}

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
        print("Error al obtener datos en mqtt")

def main():
    client = paho.mqtt.client.Client(client_id='albert-subs', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host='192.168.100.254', port=1883)
    client.loop_forever()

if __name__ == '__main__':
    main()

sys.exit(0)
