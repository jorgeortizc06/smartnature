import ssl
import sys

import paho.mqtt.client
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import time

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='casa/sala/#', qos=2)
	
def on_message(client, userdata, message):
	valor = float(message.payload)
	print('----------------------')
	print('topic: %s' % message.topic)
	print('payload: ', valor)
	if time.strftime("%H:%M") == '10:30':
		fuzzy_logic(valor)
	
	print('qos: %d' % message.qos)
	
	
def fuzzy_logic(humedadSuelo):
	# New Antecedent/Consequent objects hold universe variables and membership
	# functions
	humedad = ctrl.Antecedent(np.arange(0, 4096,1), 'humedad')
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
	print (tipping.output['tiempo_riego'])
	return tipping.output['tiempo_riego']


def main():
	client = paho.mqtt.client.Client(client_id='albert-subs', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='192.168.0.6', port=1883)
	client.loop_forever()
	
if __name__=='__main__':
	main()
	
sys.exit(0)
