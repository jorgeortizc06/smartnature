import ssl
import sys

import paho.mqtt.client

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='casa/cocina/#', qos=2)
	
def on_message(client, userdata, message):
	print('----------------------')
	print('topic: %s' % message.topic)
	print('parload: %s' % message.payload)
	print('qos: %d' % message.qos)
	
def main():
	client = paho.mqtt.client.Client(client_id='albert-subs', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_forever()
	
if __name__=='__main__':
	main()
	
sys.exit(0)
