import os
import sys
#Las configuraciones esta en el proyecto princial, necesito estar alli, asi que primero
#print(sys.path) veo mi path, estoy dentro de de varias carpetas de la raiz
#asi que dejo posicionarme en el proyecto raiz como ha continuacion
PROJECT_ROOT = sys.path.insert(0,"/casaortiz/smartnature")
#print("Tu base es:", PROJECT_ROOT)
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_asgi_application()  # modulo para importar los settings django y trabajar con modelos

import time
import paho.mqtt.client
from config.ubicacion_archivo import ip_mqtt_broker, port_mqtt
from gestion_riego.models import Sensor, Device, TipoSensor


class Suscripcion:
    def on_connect(self, client, userdata, flags, rc):
        print('connected (%s)' % client._client_id)
        client.subscribe(topic='device1/#', qos=2)

    def on_message(self, client, userdata, message):
        valor = float(message.payload)
        print('----------------------')
        print('topic: %s' % message.topic)
        device = Device.objects.first()
        tipo_sensores = TipoSensor.objects.all()
        if message.topic == 'device1/promedioSensorSuelo':
            # promedioHumedAmbiental = calcular_promedio_humedad('2020-11-4 21:00:00', '2020-11-4 21:10:59', 1, 2)

            print(device.frecuencia_actualizacion)
            frecuencia_actualizacion_segundos = device.frecuencia_actualizacion * 60
            time.sleep(frecuencia_actualizacion_segundos)
            print("===============================")

        if message.topic == 'device1/sensorSuelo1':
            sensor = Sensor(value=float(message.payload), codigo_sensor=int(1), estado="A",
                            tipo_sensor=tipo_sensores[0],
                            device=device)
            sensor.save()

        if message.topic == 'device1/sensorSuelo2':
            sensor = Sensor(value=float(message.payload), codigo_sensor=int(2), estado="A",
                            tipo_sensor=tipo_sensores[0],
                            device=device)
            sensor.save()
        if message.topic == 'device1/sensorSuelo3':
            sensor = Sensor(value=float(message.payload), codigo_sensor=int(3), estado="A",
                            tipo_sensor=tipo_sensores[0],
                            device=device)
            sensor.save()
        if message.topic == 'device1/sensorSuelo4':
            sensor = Sensor(value=float(message.payload), codigo_sensor=int(4), estado="A",
                            tipo_sensor=tipo_sensores[0],
                            device=device)
            sensor.save()
        if message.topic == 'device1/sensorHumedad1':
            sensor = Sensor(value=float(message.payload), codigo_sensor=int(1), estado="A",
                            tipo_sensor=tipo_sensores[1],
                            device=device)
            sensor.save()
        if message.topic == 'device1/sensorTemperatura1':
            sensor = Sensor(value=float(message.payload), codigo_sensor=int(1), estado="A",
                            tipo_sensor=tipo_sensores[2],
                            device=device)
            sensor.save()
        if message.topic == 'device1/sensorCaudal1':
            sensor = Sensor(value=float(message.payload), codigo_sensor=int(1), estado="A",
                            tipo_sensor=tipo_sensores[3],
                            device=device)
            sensor.save()
        if message.topic == 'device1/sensorConsumoAgua1':
            sensor = Sensor(value=float(message.payload), codigo_sensor=int(1), estado="A",
                            tipo_sensor=tipo_sensores[4],
                            device=device)
            sensor.save()

    def main(self):
        client = paho.mqtt.client.Client(client_id='albert-subs', clean_session=False)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        # client.tls_set('/etc/mosquitto/ca_certificates/ca.crt', tls_version=ssl.PROTOCOL_TLSv1_2)
        # client.tls_insecure_set(True)
        while True:
            try:
                client.connect(host=ip_mqtt_broker, port=port_mqtt)
                break
            except OSError as err:
                print("No se puede conectar con el host mqtt: ", sys.exc_info()[1], " ...intentando de nuevo")
                time.sleep(3)
        client.loop_forever()


mqtt = Suscripcion()
mqtt.main()
