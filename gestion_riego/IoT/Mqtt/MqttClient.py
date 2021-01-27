# import os
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# application = get_asgi_application()  # modulo para importar los settings django y trabajar con modelos

from gestion_riego.models import Sensor

import paho.mqtt.client

# from config.ubicacion_archivo import ip_mqtt_broker, port_mqtt

class MqttClientDevice:

    def conectar(self, host_mqtt, port_mqtt):
        client = paho.mqtt.client.Client(client_id='albert-subs')
        client.connect(host=host_mqtt, port=port_mqtt)
        return client

    def publish(self, client, topic, mensaje):
        enviando = client.publish(topic, mensaje)
        return enviando



# mqtt = MqttClientDevice()
# client = mqtt.conectar(ip_mqtt_broker, port_mqtt)
# print(client)
# enviando = mqtt.publish(client,"device1/electrovalvula", "OFF")
# print(enviando)