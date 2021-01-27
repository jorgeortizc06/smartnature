# import os
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# application = get_asgi_application()  # modulo para importar los settings django y trabajar con modelos

import time
from datetime import datetime, timedelta

from gestion_riego.models import Siembra, TipoRol, Device, HistorialRiego, TipoLogicaDifusa
from gestion_riego.IoT.LogicaDifusa import LogicaDifusa, CalcularVariableEntrada
from gestion_riego.IoT.Mqtt.MqttClient import MqttClientDevice
from gestion_riego.IoT.ActualizarDatos import ActualizarDatos

from config.ubicacion_archivo import ip_mqtt_broker, port_mqtt


class Regar:
    activacion = False
    fin_riego = ''

    def proceder_riego(self, fecha_desde, fecha_hasta):
        if self.activacion == False:
            logica_difusa = LogicaDifusa()
            calcular_variable_entrada = CalcularVariableEntrada()
            siembra = Siembra.objects.get(id=1)
            tipo_rol = TipoRol.objects.get(id=2)
            device = Device.objects.get(id=1)
            tipo_logica_difusa = TipoLogicaDifusa.objects.get(id=device.tipo_logica_difusa.id)
            print("Fecha Desde", fecha_desde)
            print("Fecha Desde", fecha_hasta)
            prom_hum_suelo1 = calcular_variable_entrada.calcular_promedio_sensor(fecha_desde, fecha_hasta, 1,
                                                                                 1)  # (fechaDesde, fechaHasta, codigo_sensor, tipo_sensor)
            prom_hum_suelo2 = calcular_variable_entrada.calcular_promedio_sensor(fecha_desde, fecha_hasta, 2, 1)
            prom_hum_suelo3 = calcular_variable_entrada.calcular_promedio_sensor(fecha_desde, fecha_hasta, 3, 1)
            prom_hum_suelo4 = calcular_variable_entrada.calcular_promedio_sensor(fecha_desde, fecha_hasta, 4, 1)
            promedio_hum_suelo_total = (prom_hum_suelo1 + prom_hum_suelo2 + prom_hum_suelo3 + prom_hum_suelo4) / 4

            prom_hum_ambient = calcular_variable_entrada.calcular_promedio_sensor(fecha_desde, fecha_hasta, 1, 2)
            prom_temp_ambient = calcular_variable_entrada.calcular_promedio_sensor(fecha_desde, fecha_hasta, 1, 3)

            v1_tiempo_riego_suelo1 = round(logica_difusa.fuzzy_logic_1_variables(float(prom_hum_suelo1)), 2)
            v1_tiempo_riego_suelo2 = round(logica_difusa.fuzzy_logic_1_variables(float(prom_hum_suelo2)), 2)
            v1_tiempo_riego_suelo3 = round(logica_difusa.fuzzy_logic_1_variables(float(prom_hum_suelo3)), 2)
            v1_tiempo_riego_suelo4 = round(logica_difusa.fuzzy_logic_1_variables(float(prom_hum_suelo4)), 2)
            v1_tiempo_riego_suelo_promedio = round(
                logica_difusa.fuzzy_logic_1_variables(float(promedio_hum_suelo_total)), 2)

            v3_tiempo_riego_suelo1 = round(
                logica_difusa.fuzzy_logic_3_variables(float(prom_hum_suelo1), float(prom_hum_ambient),
                                                      float(prom_temp_ambient)), 2)
            v3_tiempo_riego_suelo2 = round(
                logica_difusa.fuzzy_logic_3_variables(float(prom_hum_suelo2), float(prom_hum_ambient),
                                                      float(prom_temp_ambient)), 2)
            v3_tiempo_riego_suelo3 = round(
                logica_difusa.fuzzy_logic_3_variables(float(prom_hum_suelo3), float(prom_hum_ambient),
                                                      float(prom_temp_ambient)), 2)
            v3_tiempo_riego_suelo4 = round(
                logica_difusa.fuzzy_logic_3_variables(float(prom_hum_suelo4), float(prom_hum_ambient),
                                                      float(prom_temp_ambient)), 2)
            v3_tiempo_riego_suelo_promedio = round(
                logica_difusa.fuzzy_logic_3_variables(float(promedio_hum_suelo_total), float(prom_hum_ambient),
                                                      float(prom_temp_ambient)), 2)

            tdmax = calcular_variable_entrada.calcular_max_sensor(fecha_desde, fecha_hasta, 1, 3)
            tdmin = calcular_variable_entrada.calcular_min_sensor(fecha_desde, fecha_hasta, 1, 3)
            evapo = round(
                calcular_variable_entrada.calcular_evapotranspiracion(11.9, float(prom_temp_ambient), float(tdmax),
                                                                      float(tdmin)), 2)

            v4_tiempo_riego_suelo1 = round(
                logica_difusa.fuzzy_logic_4_variables(float(prom_hum_suelo1), float(prom_hum_ambient),
                                                      float(prom_temp_ambient),
                                                      float(evapo)), 2)

            v4_tiempo_riego_suelo2 = round(
                logica_difusa.fuzzy_logic_4_variables(float(prom_hum_suelo2), float(prom_hum_ambient),
                                                      float(prom_temp_ambient),
                                                      float(evapo)), 2)

            v4_tiempo_riego_suelo3 = round(
                logica_difusa.fuzzy_logic_4_variables(float(prom_hum_suelo3), float(prom_hum_ambient),
                                                      float(prom_temp_ambient),
                                                      float(evapo)), 2)

            v4_tiempo_riego_suelo4 = round(
                logica_difusa.fuzzy_logic_4_variables(float(prom_hum_suelo4), float(prom_hum_ambient),
                                                      float(prom_temp_ambient),
                                                      float(evapo)), 2)
            v4_tiempo_riego_suelo_promedio = round(
                logica_difusa.fuzzy_logic_4_variables(float(promedio_hum_suelo_total), float(prom_hum_ambient),
                                                      float(prom_temp_ambient),
                                                      float(evapo)), 2)

            print("Calcular Evapo: ", evapo)
            print("==================TIEMPO: 1 VARIABLE========================")
            print("tiempo Sensor 1: ", v1_tiempo_riego_suelo1)
            print("tiempo Sensor 2: ", v1_tiempo_riego_suelo2)
            print("tiempo Sensor 3: ", v1_tiempo_riego_suelo3)
            print("tiempo Sensor 4: ", v1_tiempo_riego_suelo4)
            print("tiempo Sensor 5: ", v1_tiempo_riego_suelo_promedio)
            print("==================TIEMPO: 3 VARIABLES========================")
            print("tiempo Sensor 1: ", v3_tiempo_riego_suelo1)
            print("tiempo Sensor 2: ", v3_tiempo_riego_suelo2)
            print("tiempo Sensor 3: ", v3_tiempo_riego_suelo3)
            print("tiempo Sensor 4: ", v3_tiempo_riego_suelo4)
            print("tiempo Sensor 5: ", v3_tiempo_riego_suelo_promedio)
            print("==================TIEMPO: 4 VARIABLES========================")
            print("tiempo Sensor 1: ", v4_tiempo_riego_suelo1)
            print("tiempo Sensor 2: ", v4_tiempo_riego_suelo2)
            print("tiempo Sensor 3: ", v4_tiempo_riego_suelo3)
            print("tiempo Sensor 4: ", v4_tiempo_riego_suelo4)
            print("tiempo Sensor 5: ", v4_tiempo_riego_suelo_promedio)

            if v3_tiempo_riego_suelo_promedio > 0:
                ahora = datetime.now()
                futuro = ahora + timedelta(minutes=v3_tiempo_riego_suelo_promedio)
                fin_riego = futuro.strftime("%H:%M:%S")
                print("Fin Riego: ", fin_riego)
                activacion = True
                mqtt = MqttClientDevice()
                client = mqtt.conectar(ip_mqtt_broker, port_mqtt)
                enviando = mqtt.publish(client,"device1/electrovalvula", "ON")
                print("Electrovalvula ON: ", enviando)
                riego_promedio = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo_promedio,
                                                tiempo_riego_1_variable=v1_tiempo_riego_suelo_promedio,
                                                tiempo_riego_4_variable=v4_tiempo_riego_suelo_promedio, siembra=siembra,
                                                codigo_sensor=5,
                                                valor_humed_suelo=promedio_hum_suelo_total,
                                                valor_humed_ambiente=prom_hum_ambient,
                                                valor_temp_ambiente=prom_temp_ambient,
                                                valor_evapotranspiracion=evapo,
                                                tipo_rol=tipo_rol,
                                                tipo_logica_difusa=tipo_logica_difusa)
                riego_promedio.save()
            elif v3_tiempo_riego_suelo_promedio <= 0:
                print("Tiempo 0, no se abrira la llave")
                riego5 = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo_promedio,
                                        tiempo_riego_1_variable=v1_tiempo_riego_suelo_promedio,
                                        tiempo_riego_4_variable=v4_tiempo_riego_suelo_promedio, siembra=siembra,
                                        codigo_sensor=5,
                                        valor_humed_suelo=promedio_hum_suelo_total,
                                        valor_humed_ambiente=prom_hum_ambient,
                                        valor_temp_ambiente=prom_temp_ambient,
                                        valor_evapotranspiracion=evapo,
                                        tipo_rol=tipo_rol,
                                        tipo_logica_difusa=tipo_logica_difusa)
                riego5.save()

            riego_sensor_suelo_1 = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo1,
                                                  tiempo_riego_1_variable=v1_tiempo_riego_suelo1,
                                                  tiempo_riego_4_variable=v4_tiempo_riego_suelo1, siembra=siembra,
                                                  codigo_sensor=1,
                                                  valor_humed_suelo=prom_hum_suelo1,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_1.save()

            riego_sensor_suelo_2 = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo2,
                                                  tiempo_riego_1_variable=v1_tiempo_riego_suelo2,
                                                  tiempo_riego_4_variable=v4_tiempo_riego_suelo2, siembra=siembra,
                                                  codigo_sensor=2,
                                                  valor_humed_suelo=prom_hum_suelo2,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_2.save()

            riego_sensor_suelo_3 = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo3,
                                                  tiempo_riego_1_variable=v1_tiempo_riego_suelo3,
                                                  tiempo_riego_4_variable=v4_tiempo_riego_suelo3, siembra=siembra,
                                                  codigo_sensor=3,
                                                  valor_humed_suelo=prom_hum_suelo3,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_3.save()
            riego_sensor_suelo_4 = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo4,
                                                  tiempo_riego_1_variable=v1_tiempo_riego_suelo4,
                                                  tiempo_riego_4_variable=v4_tiempo_riego_suelo4, siembra=siembra,
                                                  codigo_sensor=4,
                                                  valor_humed_suelo=prom_hum_suelo4,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_4.save()


        # Si el riego esta en proceso continuara ejecutandose hasta que se cierre la llave
        if self.activacion == True:
            while True:
                print(datetime.now())
                if time.strftime("%H:%M:%S") == fin_riego:
                    print("La llave se ha cerrado")
                    activacion = False
                    enviando = mqtt.publish(client, "device1/electrovalvula", "OFF")
                    print("Electrovalvula ON: ", enviando)
                    # client = paho.mqtt.client.Client(client_id='albert-subs')
                    # client.connect(host=host_database, port=1883)
                    # enviando = client.publish("device1/electrovalvula", "OFF")
                    break;
                time.sleep(1)

        # Actualizo los ultimos datos para incrustar la imagen de tiempo de riego
        actualizar_datos = ActualizarDatos()
        historial_riegos = actualizar_datos.actualizar_datos()
        print("Sali del bucle")


# riego1 = Regar()
# fecha_desde = time.strftime("%d/%m/%Y") + " " + '08:00:00'
# fecha_hasta = time.strftime("%d/%m/%Y") + " " + '12:00:00'
# riego1.proceder_riego(fecha_desde, fecha_hasta)
