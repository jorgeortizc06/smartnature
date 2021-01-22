import os
from pathlib import Path
import sys

from gestion_riego.models import Plataforma, HistorialRiego, Siembra, TipoRol, TipoLogicaDifusa, Device
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from datetime import datetime, timedelta
import time
import psycopg2
import paho.mqtt.client
import matplotlib.pyplot as plt

activacion = False
fin_riego = ''

def ejecutar_horario_1():
    # Voy un dia atras
    d = datetime.today() - timedelta(days=1)
    fecha_desde = d.strftime("%Y-%m-%d") + " " + '17:00:00'
    # Dia de hoy
    fecha_hasta = time.strftime("%Y-%m-%d") + " " + '08:00:00'
    regar(fecha_desde, fecha_hasta)

def ejecutar_horario_2():
    fecha_desde = time.strftime("%Y-%m-%d") + " " + '08:00:00'
    fecha_hasta = time.strftime("%Y-%m-%d") + " " + '12:00:00'
    regar(fecha_desde, fecha_hasta)

def ejecutar_horario_3():
    fecha_desde = time.strftime("%Y-%m-%d") + " " + '12:00:00'
    fecha_hasta = time.strftime("%Y-%m-%d") + " " + '17:00:00'
    regar(fecha_desde, fecha_hasta)

def on_connect(client, userdata, flags, rc):
    print('connected (%s)' % client._client_id)
    client.subscribe(topic='device1/#', qos=2)

def start():
    scheduler = BackgroundScheduler()
    plataforma = Plataforma.objects.get(id=1)
    scheduler.add_job(ejecutar_horario_1, 'cron', day_of_week='mon-sun', hour=8, minute=0)
    scheduler.add_job(ejecutar_horario_2, 'cron', day_of_week='mon-sun', hour=12, minute=0)
    scheduler.add_job(ejecutar_horario_3, 'cron', day_of_week='mon-sun', hour=17, minute=0)
    scheduler.start()

#Empieza a regar
def regar(fechaDesde, fechaHasta):
    global activacion
    global fin_riego
    print(activacion)
    print(datetime.now())
    if activacion == False:
        try:
            siembra = Siembra.objects.get(id=1)
            tipo_rol = TipoRol.objects.get(id=2)
            device = Device.objects.get(id=1)
            tipo_logica_difusa = TipoLogicaDifusa.objects.get(id=device.tipo_logica_difusa.id)

            print("Fecha Desde", fechaDesde)
            print("Fecha Desde", fechaHasta)
            prom_hum_suelo1 = calcular_promedio(fechaDesde, fechaHasta, 1,
                                                1)  # (fechaDesde, fechaHasta, codigo_sensor, tipo_sensor)
            prom_hum_suelo2 = calcular_promedio(fechaDesde, fechaHasta, 2, 1)
            prom_hum_suelo3 = calcular_promedio(fechaDesde, fechaHasta, 3, 1)
            prom_hum_suelo4 = calcular_promedio(fechaDesde, fechaHasta, 4, 1)
            promedio_hum_suelo_total = (prom_hum_suelo1 + prom_hum_suelo2 + prom_hum_suelo3 + prom_hum_suelo4) / 4

            prom_hum_ambient = calcular_promedio(fechaDesde, fechaHasta, 1, 2)
            prom_temp_ambient = calcular_promedio(fechaDesde, fechaHasta, 1, 3)

            """if tipo_logica_difusa.id == 1:
                print('Logica difusa de 1 variable')
                tiempo_riego_suelo1 = round(fuzzy_logic_1_variables(float(prom_hum_suelo1)), 2)
                tiempo_riego_suelo2 = round(fuzzy_logic_1_variables(float(prom_hum_suelo2)), 2)
                tiempo_riego_suelo3 = round(fuzzy_logic_1_variables(float(prom_hum_suelo3)), 2)
                tiempo_riego_suelo4 = round(fuzzy_logic_1_variables(float(prom_hum_suelo4)), 2)
                tiempo_riego_suelo_promedio = round(fuzzy_logic_1_variables(float(promedio_hum_suelo_total)), 2)
            elif tipo_logica_difusa.id == 2:
                print('Logica difusa de 3 variable')
                tiempo_riego_suelo1 = round(
                    fuzzy_logic_3_variables(float(prom_hum_suelo1), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
                tiempo_riego_suelo2 = round(
                    fuzzy_logic_3_variables(float(prom_hum_suelo2), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
                tiempo_riego_suelo3 = round(
                    fuzzy_logic_3_variables(float(prom_hum_suelo3), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
                tiempo_riego_suelo4 = round(
                    fuzzy_logic_3_variables(float(prom_hum_suelo4), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
                tiempo_riego_suelo_promedio = round(
                    fuzzy_logic_3_variables(float(promedio_hum_suelo_total), float(prom_hum_ambient),
                                            float(prom_temp_ambient)), 2)
            elif tipo_logica_difusa.id == 3:
                print('Logica difusa de 4 variable')
                print('Aun no existe la variable de logica difusa con 4 variables')
                tiempo_riego_suelo1 = 0
                tiempo_riego_suelo2 = 0
                tiempo_riego_suelo3 = 0
                tiempo_riego_suelo4 = 0
                tiempo_riego_suelo_promedio = 0"""

            v1_tiempo_riego_suelo1 = round(fuzzy_logic_1_variables(float(prom_hum_suelo1)), 2)
            v1_tiempo_riego_suelo2= round(fuzzy_logic_1_variables(float(prom_hum_suelo2)), 2)
            v1_tiempo_riego_suelo3 = round(fuzzy_logic_1_variables(float(prom_hum_suelo3)), 2)
            v1_tiempo_riego_suelo4 = round(fuzzy_logic_1_variables(float(prom_hum_suelo4)), 2)
            v1_tiempo_riego_suelo_promedio = round(fuzzy_logic_1_variables(float(promedio_hum_suelo_total)), 2)

            v3_tiempo_riego_suelo1 = round(
                fuzzy_logic_3_variables(float(prom_hum_suelo1), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
            v3_tiempo_riego_suelo2 = round(
                fuzzy_logic_3_variables(float(prom_hum_suelo2), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
            v3_tiempo_riego_suelo3 = round(
                fuzzy_logic_3_variables(float(prom_hum_suelo3), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
            v3_tiempo_riego_suelo4 = round(
                fuzzy_logic_3_variables(float(prom_hum_suelo4), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
            v3_tiempo_riego_suelo_promedio = round(
                fuzzy_logic_3_variables(float(promedio_hum_suelo_total), float(prom_hum_ambient),
                                        float(prom_temp_ambient)), 2)

            tdmax = obtenerMax(fechaDesde, fechaHasta, 1, 3)
            tdmin = obtenerMin(fechaDesde, fechaHasta, 1, 3)
            evapo = round(calcularEvapotranspiracion(11.9, float(prom_temp_ambient), float(tdmax), float(tdmin)), 2)

            v4_tiempo_riego_suelo1 = round(
                fuzzy_logic_4_variables(float(prom_hum_suelo1), float(prom_hum_ambient), float(prom_temp_ambient),
                                        float(evapo)), 2)

            v4_tiempo_riego_suelo2 = round(
                fuzzy_logic_4_variables(float(prom_hum_suelo2), float(prom_hum_ambient), float(prom_temp_ambient),
                                        float(evapo)), 2)

            v4_tiempo_riego_suelo3 = round(
                fuzzy_logic_4_variables(float(prom_hum_suelo3), float(prom_hum_ambient), float(prom_temp_ambient),
                                        float(evapo)), 2)

            v4_tiempo_riego_suelo4 = round(
                fuzzy_logic_4_variables(float(prom_hum_suelo4), float(prom_hum_ambient), float(prom_temp_ambient),
                                        float(evapo)), 2)
            v4_tiempo_riego_suelo_promedio = round(
                fuzzy_logic_4_variables(float(promedio_hum_suelo_total), float(prom_hum_ambient), float(prom_temp_ambient),
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

            if v3_tiempo_riego_suelo_promedio > 0:
                ahora = datetime.now()
                futuro = ahora + timedelta(minutes=v3_tiempo_riego_suelo_promedio)
                fin_riego = futuro.strftime("%H:%M:%S")
                print("Fin Riego: ", fin_riego)
                activacion = True
                # historial_riego = {"tiempo_riego": float(tiempo_riego), "siembra": 1, "tipo_rol": 2}
                # et_historial_riego = requests.post(api_historial_riego, data=json.dumps(historial_riego), headers=headers)
                client = paho.mqtt.client.Client(client_id='albert-subs')
                client.connect(host='192.168.100.254', port=1883)
                enviando = client.publish("device1/electrovalvula", "ON")
                print("Mqtt ON: ", enviando)
                riego_promedio = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo_promedio, tiempo_riego_1_variable=v1_tiempo_riego_suelo_promedio, tiempo_riego_4_variable = v4_tiempo_riego_suelo_promedio, siembra=siembra,
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
                riego5 = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo_promedio, tiempo_riego_1_variable=v1_tiempo_riego_suelo_promedio, tiempo_riego_4_variable = v4_tiempo_riego_suelo_promedio, siembra=siembra, codigo_sensor=5,
                                        valor_humed_suelo=promedio_hum_suelo_total,
                                        valor_humed_ambiente=prom_hum_ambient,
                                        valor_temp_ambiente=prom_temp_ambient,
                                        valor_evapotranspiracion=evapo,
                                        tipo_rol=tipo_rol,
                                        tipo_logica_difusa=tipo_logica_difusa)
                riego5.save()

            riego_sensor_suelo_1 = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo1, tiempo_riego_1_variable=v1_tiempo_riego_suelo1, tiempo_riego_4_variable = v4_tiempo_riego_suelo1, siembra=siembra, codigo_sensor=1,
                                                  valor_humed_suelo=prom_hum_suelo1,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_1.save()

            riego_sensor_suelo_2 = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo2,tiempo_riego_1_variable=v1_tiempo_riego_suelo2, tiempo_riego_4_variable = v4_tiempo_riego_suelo2, siembra=siembra, codigo_sensor=2,
                                                  valor_humed_suelo=prom_hum_suelo2,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_2.save()

            riego_sensor_suelo_3 = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo3,tiempo_riego_1_variable=v1_tiempo_riego_suelo3, tiempo_riego_4_variable = v4_tiempo_riego_suelo3, siembra=siembra, codigo_sensor=3,
                                                  valor_humed_suelo=prom_hum_suelo3,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_3.save()
            riego_sensor_suelo_4 = HistorialRiego(tiempo_riego=v3_tiempo_riego_suelo4,tiempo_riego_1_variable=v1_tiempo_riego_suelo4, tiempo_riego_4_variable = v4_tiempo_riego_suelo4, siembra=siembra, codigo_sensor=4,
                                                  valor_humed_suelo=prom_hum_suelo4,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_4.save()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    #Si el riego esta en proceso continuara ejecutandose hasta que se cierre la llave
    if activacion == True:
        while True:
            print(datetime.now())
            if time.strftime("%H:%M:%S") == fin_riego:
                print("La llave se ha cerrado")
                activacion = False
                client = paho.mqtt.client.Client(client_id='albert-subs')
                client.connect(host='192.168.100.254', port=1883)
                enviando = client.publish("device1/electrovalvula", "OFF")
                break;
            time.sleep(1)
        #Actualizo los ultimos datos para incrustar la imagen de tiempo de riego
        historial_riegos = cargar_historial_riego()
        actualizar_datos(historial_riegos)
        print("Sali del bucle")


# Funcion para la obtencion de la evapotranspiracion. Fuente: https://hidrologia.usal.es/temas/Evapotransp.pdf
def calcularEvapotranspiracion(R0, tmed, tdmax, tdmin):
    et0 = 0.0023 * (tmed + 17.78) * (R0) * (tdmax - tdmin) ** (0.5)
    return et0

#Funcion para obtener el promedio de los sensores de humedad de suelo
def calcular_promedio(fecha_inicio, fecha_fin, codigo_sensor, tipo_sensor):
    promedio = 0
    try:
        connection = psycopg2.connect(host="192.168.100.254", port="5432", database="smartnature", user="jorge",
                                      password="jorge")
        cursor = connection.cursor()
        # Ejecutamos una consulta
        sql = """select round(avg(value), 2) 
        from gestion_riego_sensor grs 
        where fecha_registro >= %s::timestamp AT TIME ZONE 'America/Guayaquil' 
        and fecha_registro <= %s::timestamp AT TIME ZONE 'America/Guayaquil'
        and codigo_sensor = %s
        and tipo_sensor_id = %s
        group by tipo_sensor_id"""
        cursor.execute(sql, (fecha_inicio, fecha_fin, codigo_sensor, tipo_sensor))
        # Recorremos los resultados y los mostramos
        datas = cursor.fetchone()
        if datas is not None:
            promedio = datas[0]
            print(promedio)
        # Cerramos la conexión
        else:
            promedio = 0
        return promedio

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


#Funciona para obtener el valor máximo de un sensor
def obtenerMax(fecha_inicio, fecha_fin, codigo_sensor, tipo_sensor):
    max = 0
    try:
        connection = psycopg2.connect(host="192.168.100.254", port="5432", database="smartnature", user="jorge",
                                      password="jorge")
        cursor = connection.cursor()
        # Ejecutamos una consulta
        sql = """select round(max(value), 2) 
            from gestion_riego_sensor grs 
            where fecha_registro >= %s::timestamp AT TIME ZONE 'America/Guayaquil' 
            and fecha_registro <= %s::timestamp AT TIME ZONE 'America/Guayaquil'
            and codigo_sensor = %s
            and tipo_sensor_id = %s
            group by tipo_sensor_id"""
        cursor.execute(sql, (fecha_inicio, fecha_fin, codigo_sensor, tipo_sensor))
        # Recorremos los resultados y los mostramos
        datas = cursor.fetchone()
        if datas is not None:
            max = datas[0]
            print("Obtener max: ", max)
        # Cerramos la conexión
        else:
            max = 0
        return max

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

#Funciona para obtener el valor mínimo de un sensor
def obtenerMin(fecha_inicio, fecha_fin, codigo_sensor, tipo_sensor):
    min = 0
    try:
        connection = psycopg2.connect(host="192.168.100.254", port="5432", database="smartnature", user="jorge",
                                      password="jorge")
        cursor = connection.cursor()
        # Ejecutamos una consulta
        sql = """select round(min(value), 2) 
                from gestion_riego_sensor grs 
                where fecha_registro >= %s::timestamp AT TIME ZONE 'America/Guayaquil' 
                and fecha_registro <= %s::timestamp AT TIME ZONE 'America/Guayaquil'
                and codigo_sensor = %s
                and tipo_sensor_id = %s
                group by tipo_sensor_id"""
        cursor.execute(sql, (fecha_inicio, fecha_fin, codigo_sensor, tipo_sensor))
        # Recorremos los resultados y los mostramos
        datas = cursor.fetchone()
        if datas is not None:
            min = datas[0]
            print("Obtener min: ", min)
        # Cerramos la conexión
        else:
            min = 0
        return min
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

#Funcion para la lógica difusa de una variable, devuelve tiempo de riego.
def fuzzy_logic_1_variables(par_humedad_suelo):
    try:
        humedad_suelo = ctrl.Antecedent(np.arange(0, 1024, 1), 'humedad_suelo')
        tiempo_riego = ctrl.Consequent(np.arange(-2, 18, 1), 'tiempo_riego')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        humedad_suelo['seco'] = fuzz.trimf(humedad_suelo.universe, [0, 100, 200])
        humedad_suelo['semi_seco'] = fuzz.trimf(humedad_suelo.universe, [120, 310, 500])
        humedad_suelo['humedo'] = fuzz.trimf(humedad_suelo.universe, [450, 572, 694])
        humedad_suelo['semi_humedo'] = fuzz.trimf(humedad_suelo.universe, [658, 725, 792])
        humedad_suelo['encharcado'] = fuzz.trimf(humedad_suelo.universe, [750, 887,1024])

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        tiempo_riego['nada'] = fuzz.trimf(tiempo_riego.universe, [-2, -1, 0])
        tiempo_riego['poco'] = fuzz.trimf(tiempo_riego.universe, [0, 2, 4])
        tiempo_riego['medio'] = fuzz.trimf(tiempo_riego.universe, [3, 6, 9])
        tiempo_riego['bastante'] = fuzz.trimf(tiempo_riego.universe, [7, 9, 12])
        tiempo_riego['mucho'] = fuzz.trapmf(tiempo_riego.universe, [10, 13, 17, 17])

        rule1 = ctrl.Rule(humedad_suelo['encharcado'], tiempo_riego['nada'])
        rule2 = ctrl.Rule(humedad_suelo['semi_humedo'], tiempo_riego['poco'])
        rule3 = ctrl.Rule(humedad_suelo['humedo'], tiempo_riego['medio'])
        rule4 = ctrl.Rule(humedad_suelo['semi_seco'], tiempo_riego['bastante'])
        rule5 = ctrl.Rule(humedad_suelo['seco'], tiempo_riego['mucho'])

        tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
        tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        tipping.input['humedad_suelo'] = par_humedad_suelo
        tipping.compute()
        minutos_riego = tipping.output['tiempo_riego']
        #grafica = tiempo_riego.view(sim=tipping)
        #plt.savefig("C:/casaortiz/django/smartnature/gestion_riego/media/fuzzy1/" + id_historial_riego)
        #plt.close(grafica)
        if minutos_riego > 0:
            return minutos_riego
        else:
            return 0
    except Exception:
        print("Fuera de rango en las entradas de variables de humedad: ", sys.exc_info()[1], ' humedad suelo:' ,par_humedad_suelo)
        return 0;

#funciona para la lógic difusa de 3 variables, devuelve tiempo de riego
def fuzzy_logic_3_variables(par_humedad_suelo, par_humedad_ambiental, par_temperatura_ambiental,):
    try:
        humedad_suelo = ctrl.Antecedent(np.arange(0, 1024, 1), 'humedad_suelo')
        temperatura_ambiental = ctrl.Antecedent(np.arange(5, 46, 1), 'temperatura_ambiental')
        humedad_ambiental = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad_ambiental')
        tiempo_riego = ctrl.Consequent(np.arange(-2, 18, 1), 'tiempo_riego')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        humedad_suelo['seco'] = fuzz.trimf(humedad_suelo.universe, [0, 100, 200])
        humedad_suelo['semi_seco'] = fuzz.trimf(humedad_suelo.universe, [120, 310, 500])
        humedad_suelo['humedo'] = fuzz.trimf(humedad_suelo.universe, [450, 572, 694])
        humedad_suelo['semi_humedo'] = fuzz.trimf(humedad_suelo.universe, [658, 725, 792])
        humedad_suelo['encharcado'] = fuzz.trimf(humedad_suelo.universe, [750, 887,1024])

        temperatura_ambiental['baja'] = fuzz.trimf(temperatura_ambiental.universe, [5, 7, 10])
        temperatura_ambiental['media'] = fuzz.trimf(temperatura_ambiental.universe, [8, 17, 27])
        temperatura_ambiental['alta'] = fuzz.trimf(temperatura_ambiental.universe, [24, 34, 45])

        humedad_ambiental['baja'] = fuzz.trimf(humedad_ambiental.universe, [0, 16, 33])
        humedad_ambiental['media'] = fuzz.trimf(humedad_ambiental.universe, [16, 41, 66])
        humedad_ambiental['alta'] = fuzz.trimf(humedad_ambiental.universe, [41, 70, 100])

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        tiempo_riego['nada'] = fuzz.trimf(tiempo_riego.universe, [-2, -1, 0])
        tiempo_riego['poco'] = fuzz.trimf(tiempo_riego.universe, [0, 2, 4])
        tiempo_riego['medio'] = fuzz.trimf(tiempo_riego.universe, [3, 6, 9])
        tiempo_riego['bastante'] = fuzz.trimf(tiempo_riego.universe, [7, 9, 12])
        tiempo_riego['mucho'] = fuzz.trapmf(tiempo_riego.universe, [10, 13, 17, 17])
        rule1 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                          tiempo_riego['nada'])
        rule2 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                          tiempo_riego['nada'])
        rule3 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                          tiempo_riego['nada'])
        rule4 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                          tiempo_riego['nada'])
        rule5 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                          tiempo_riego['nada'])
        rule6 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                          tiempo_riego['nada'])
        rule7 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                          tiempo_riego['nada'])
        rule8 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                          tiempo_riego['nada'])
        rule9 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                          tiempo_riego['nada'])
        rule10 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                           tiempo_riego['nada'])
        rule11 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                           tiempo_riego['nada'])
        rule12 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule13 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                           tiempo_riego['poco'])
        rule14 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                           tiempo_riego['nada'])
        rule15 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule16 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                           tiempo_riego['medio'])
        rule17 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                           tiempo_riego['poco'])
        rule18 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule19 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                           tiempo_riego['nada'])
        rule20 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                           tiempo_riego['nada'])
        rule21 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule22 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                           tiempo_riego['poco'])
        rule23 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                           tiempo_riego['poco'])
        rule24 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule25 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                           tiempo_riego['medio'])
        rule26 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                           tiempo_riego['poco'])
        rule27 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule28 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                           tiempo_riego['poco'])
        rule29 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                           tiempo_riego['nada'])
        rule30 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule31 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                           tiempo_riego['bastante'])
        rule32 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                           tiempo_riego['medio'])
        rule33 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                           tiempo_riego['poco'])
        rule34 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                           tiempo_riego['mucho'])
        rule35 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                           tiempo_riego['bastante'])
        rule36 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                           tiempo_riego['mucho'])
        rule37 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                           tiempo_riego['medio'])
        rule38 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                           tiempo_riego['medio'])
        rule39 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                           tiempo_riego['poco'])
        rule40 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                           tiempo_riego['mucho'])
        rule41 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                           tiempo_riego['mucho'])
        rule42 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                           tiempo_riego['bastante'])
        rule43 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                           tiempo_riego['mucho'])
        rule44 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                           tiempo_riego['mucho'])
        rule45 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                           tiempo_riego['mucho'])

        tipping_ctrl = ctrl.ControlSystem(
            [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14,
             rule15,
             rule16,
             rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29,
             rule30,
             rule31, rule32, rule33, rule34, rule3, rule36,
             rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45])
        tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        tipping.input['humedad_suelo'] = par_humedad_suelo
        tipping.input['humedad_ambiental'] = par_humedad_ambiental
        tipping.input['temperatura_ambiental'] = par_temperatura_ambiental
        tipping.compute()
        minutos_riego = tipping.output['tiempo_riego']
        #grafica = tiempo_riego.view(sim=tipping)
        #plt.savefig("C:/casaortiz/django/smartnature/gestion_riego/media/fuzzy3/" + id_historial_riego)
        #plt.close(grafica)
        if minutos_riego >0 :
            return minutos_riego
        else:
            return 0
    except Exception:
        print("Fuera de rango: ", sys.exc_info()[1], ' humedad suelo:', par_humedad_suelo)
        print("Humd Ambiente: ", par_humedad_ambiental)
        print("Temp Ambiente: ", par_temperatura_ambiental)
        return 0;

#funciona para la lógic difusa de 4 variables, devuelve tiempo de riego
def fuzzy_logic_4_variables(par_humedad_suelo, par_humedad_ambiental, par_temperatura_ambiental, par_evapo):
    try:
        humedad_suelo = ctrl.Antecedent(np.arange(0, 1024, 1), 'humedad_suelo')
        temperatura_ambiental = ctrl.Antecedent(np.arange(5, 46, 1), 'temperatura_ambiental')
        humedad_ambiental = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad_ambiental')
        evapo = ctrl.Antecedent(np.arange(0, 9, 1), 'evapo')
        tiempo_riego = ctrl.Consequent(np.arange(-2, 18, 1), 'tiempo_riego')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        humedad_suelo['seco'] = fuzz.trimf(humedad_suelo.universe, [0, 100, 200])
        humedad_suelo['semi_seco'] = fuzz.trimf(humedad_suelo.universe, [120, 310, 500])
        humedad_suelo['humedo'] = fuzz.trimf(humedad_suelo.universe, [450, 572, 694])
        humedad_suelo['semi_encharcado'] = fuzz.trimf(humedad_suelo.universe, [658, 725, 792])
        humedad_suelo['encharcado'] = fuzz.trimf(humedad_suelo.universe, [750, 887,1024])

        temperatura_ambiental['baja'] = fuzz.trimf(temperatura_ambiental.universe, [5, 7, 10])
        temperatura_ambiental['media'] = fuzz.trimf(temperatura_ambiental.universe, [8, 17, 27])
        temperatura_ambiental['alta'] = fuzz.trimf(temperatura_ambiental.universe, [24, 34, 45])

        humedad_ambiental['baja'] = fuzz.trimf(humedad_ambiental.universe, [0, 16, 33])
        humedad_ambiental['media'] = fuzz.trimf(humedad_ambiental.universe, [16, 41, 66])
        humedad_ambiental['alta'] = fuzz.trimf(humedad_ambiental.universe, [41, 70, 100])

        evapo['baja'] = fuzz.trimf(evapo.universe, [0, 2, 4])
        evapo['media'] = fuzz.trimf(evapo.universe, [2, 4, 6])
        evapo['alta'] = fuzz.trimf(evapo.universe, [4, 6, 8])

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        tiempo_riego['nada'] = fuzz.trimf(tiempo_riego.universe, [-2, -1, 0])
        tiempo_riego['poco'] = fuzz.trimf(tiempo_riego.universe, [0, 2, 4])
        tiempo_riego['medio'] = fuzz.trimf(tiempo_riego.universe, [3, 6, 9])
        tiempo_riego['bastante'] = fuzz.trimf(tiempo_riego.universe, [7, 9, 12])
        tiempo_riego['mucho'] = fuzz.trapmf(tiempo_riego.universe, [10, 13, 17, 17])
        rule1 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule2 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule3 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['nada'])
        rule4 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule5 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule6 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['nada'])
        rule7 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule8 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule9 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule10 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule11 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule12 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['nada'])
        rule13 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule14 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule15 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['nada'])
        rule16 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule17 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule18 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule19 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule20 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule21 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['nada'])
        rule22 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule23 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule24 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['nada'])
        rule25 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule26 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule27 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule28 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule29 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo[
                'media'], tiempo_riego['nada'])
        rule30 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule31 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule32 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                'media'], tiempo_riego['nada'])
        rule33 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule34 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule35 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo[
                'media'], tiempo_riego['nada'])
        rule36 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule37 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule38 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                'media'], tiempo_riego['nada'])
        rule39 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                'alta'], tiempo_riego['poco'])
        rule40 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule41 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                'media'], tiempo_riego['nada'])
        rule42 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule43 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule44 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                'media'], tiempo_riego['nada'])
        rule45 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule46 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule47 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo[
                'media'], tiempo_riego['nada'])
        rule48 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo[
                'alta'], tiempo_riego['medio'])
        rule49 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule50 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                'media'], tiempo_riego['nada'])
        rule51 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                'alta'], tiempo_riego['poco'])
        rule52 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule53 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo[
                'media'], tiempo_riego['nada'])
        rule54 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule55 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule56 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule57 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['poco'])
        rule58 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule59 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule60 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['nada'])
        rule61 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule62 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule63 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule64 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule65 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule66 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['poco'])
        rule67 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule68 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule69 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['poco'])
        rule70 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule71 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule72 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule73 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule74 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule75 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['medio'])
        rule76 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule77 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule78 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['poco'])
        rule79 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule80 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule81 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['poco'])
        rule82 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule83 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule84 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['poco'])
        rule85 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule86 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule87 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['nada'])
        rule88 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule89 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule90 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule91 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule92 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['medio'])
        rule93 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['bastante'])
        rule94 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule95 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['poco'])
        rule96 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['medio'])
        rule97 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule98 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule99 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['poco'])
        rule100 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['poco'])
        rule101 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['medio'])
        rule102 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['mucho'])
        rule103 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['poco'])
        rule104 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['medio'])
        rule105 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['bastante'])
        rule106 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['poco'])
        rule107 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['medio'])
        rule108 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['bastante'])
        rule109 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule110 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['poco'])
        rule111 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['medio'])
        rule112 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule113 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['poco'])
        rule114 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['medio'])
        rule115 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule116 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule117 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['poco'])
        rule118 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['medio'])
        rule119 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['bastante'])
        rule120 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['mucho'])
        rule121 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['medio'])
        rule122 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['bastante'])
        rule123 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['mucho'])
        rule124 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['poco'])
        rule125 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['medio'])
        rule126 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['bastante'])
        rule127 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['medio'])
        rule128 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['bastante'])
        rule129 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['mucho'])
        rule130 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['medio'])
        rule131 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['bastante'])
        rule132 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['mucho'])
        rule133 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['medio'])
        rule134 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['bastante'])
        rule135 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['mucho'])

        tipping_ctrl = ctrl.ControlSystem([rule1,
                                           rule2,
                                           rule3,
                                           rule4,
                                           rule5,
                                           rule6,
                                           rule7,
                                           rule8,
                                           rule9,
                                           rule10,
                                           rule11,
                                           rule12,
                                           rule13,
                                           rule14,
                                           rule15,
                                           rule16,
                                           rule17,
                                           rule18,
                                           rule19,
                                           rule20,
                                           rule21,
                                           rule22,
                                           rule23,
                                           rule24,
                                           rule25,
                                           rule26,
                                           rule27,
                                           rule28,
                                           rule29,
                                           rule30,
                                           rule31,
                                           rule32,
                                           rule33,
                                           rule34,
                                           rule35,
                                           rule36,
                                           rule37,
                                           rule38,
                                           rule39,
                                           rule40,
                                           rule41,
                                           rule42,
                                           rule43,
                                           rule44,
                                           rule45,
                                           rule46,
                                           rule47,
                                           rule48,
                                           rule49,
                                           rule50,
                                           rule51,
                                           rule52,
                                           rule53,
                                           rule54,
                                           rule55,
                                           rule56,
                                           rule57,
                                           rule58,
                                           rule59,
                                           rule60,
                                           rule61,
                                           rule62,
                                           rule63,
                                           rule64,
                                           rule65,
                                           rule66,
                                           rule67,
                                           rule68,
                                           rule69,
                                           rule70,
                                           rule71,
                                           rule72,
                                           rule73,
                                           rule74,
                                           rule75,
                                           rule76,
                                           rule77,
                                           rule78,
                                           rule79,
                                           rule80,
                                           rule81,
                                           rule82,
                                           rule83,
                                           rule84,
                                           rule85,
                                           rule86,
                                           rule87,
                                           rule88,
                                           rule89,
                                           rule90,
                                           rule91,
                                           rule92,
                                           rule93,
                                           rule94,
                                           rule95,
                                           rule96,
                                           rule97,
                                           rule98,
                                           rule99,
                                           rule100,
                                           rule101,
                                           rule102,
                                           rule103,
                                           rule104,
                                           rule105,
                                           rule106,
                                           rule107,
                                           rule108,
                                           rule109,
                                           rule110,
                                           rule111,
                                           rule112,
                                           rule113,
                                           rule114,
                                           rule115,
                                           rule116,
                                           rule117,
                                           rule118,
                                           rule119,
                                           rule120,
                                           rule121,
                                           rule122,
                                           rule123,
                                           rule124,
                                           rule125,
                                           rule126,
                                           rule127,
                                           rule128,
                                           rule129,
                                           rule130,
                                           rule131,
                                           rule132,
                                           rule133,
                                           rule134,
                                           rule135
                                           ])
        tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        tipping.input['humedad_suelo'] = par_humedad_suelo
        tipping.input['temperatura_ambiental'] = par_temperatura_ambiental
        tipping.input['humedad_ambiental'] = par_humedad_ambiental
        tipping.input['evapo'] = par_evapo
        tipping.compute()
        minutos_riego = tipping.output['tiempo_riego']
        #grafica = tiempo_riego.view(sim=tipping)
        #plt.savefig("C:/casaortiz/django/smartnature/gestion_riego/media/fuzzy4/" + id_historial_riego)
        #plt.close(grafica)
        if minutos_riego >0:
            return minutos_riego
        else:
            return 0
    except Exception:
        print("Fuera de rango: ", sys.exc_info()[1], ' humedad suelo:', par_humedad_suelo)
        print("Humd Ambiente: ", par_humedad_ambiental)
        print("Temp Ambiente: ", par_temperatura_ambiental)
        print("Evapotranspiracion: ", par_evapo)
        return 0;

##################Introducir imagenes de pertenencia: tiempo de riego#####################################
def ubicacion_imagen_fuzzy1():
    return "/casaortiz/django/smartnature/gestion_riego/media/fuzzy1/"

def ubicacion_imagen_fuzzy3():
    return "/casaortiz/django/smartnature/gestion_riego/media/fuzzy3/"

def ubicacion_imagen_fuzzy4():
    return "/casaortiz/django/smartnature/gestion_riego/media/fuzzy4/"
def cargar_historial_riego():
    promedio = 0
    try:
        connection = psycopg2.connect(host="localhost", port="5432", database="smartnature", user="jorge",
                                      password="jorge")
        cursor = connection.cursor()
        # Ejecutamos una consulta
        sql = """select *
                from gestion_riego_historialriego grh
                where image_1_variable = ''
                or image_3_variable = ''
                or image_4_variable = ''
                order by id desc"""
        cursor.execute(sql)
        historial_riego = {}
        list = []
        for data in cursor:

            list.append({'id': data[0], 'tiempo': data[1], 'valor_humed_suelo': data[4], 'valor_humed_ambiente': data[5], 'valor_temp_ambiente': data[6], 'evapotranspiracion': data[7]})

        #print(list)

        return list


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def actualizar_datos(historial_riegos):
    try:
        for i in historial_riegos:
            id_historial_riego = i['id']
            humedad_suelo = i['valor_humed_suelo']
            humedad_ambiente = i['valor_humed_ambiente']
            temperatura_ambiente = i['valor_temp_ambiente']
            evapotranspiracion = i['evapotranspiracion']
            tiempo_riego_1_variable = round(fuzzy_logic_1_variables_image(float(humedad_suelo), str(id_historial_riego)), 2)
            tiempo_riego_3_variable = round(fuzzy_logic_3_variables_image(float(humedad_suelo), float(humedad_ambiente), float(temperatura_ambiente), str(id_historial_riego)),2)
            tiempo_riego_4_variable = round(fuzzy_logic_4_variables_image(float(humedad_suelo), float(humedad_ambiente), float(temperatura_ambiente), float(evapotranspiracion), str(id_historial_riego)), 2)
            ruta_imagen_fuzzy1 = 'fuzzy1/'+str(id_historial_riego)+'.png'
            ruta_imagen_fuzzy3 = 'fuzzy3/'+str(id_historial_riego)+'.png'
            ruta_imagen_fuzzy4 = 'fuzzy4/'+str(id_historial_riego)+'.png'
            print("Ruta imagen fuzzy1: ", ruta_imagen_fuzzy1)
            print("Ruta imagen fuzzy3: ", ruta_imagen_fuzzy3)
            print("Ruta imagen fuzzy4: ", ruta_imagen_fuzzy4)
            connection = psycopg2.connect(host="localhost", port="5432", database="smartnature", user="jorge",
                                         password="jorge")
            cursor = connection.cursor()

            sql = """
                UPDATE public.gestion_riego_historialriego 
                SET tiempo_riego=%s, image_1_variable=%s, image_3_variable=%s, image_4_variable=%s, tiempo_riego_1_variable=%s, tiempo_riego_4_variable=%s 
                WHERE id= %s;
            """

            cursor.execute(sql, (tiempo_riego_3_variable, ruta_imagen_fuzzy1, ruta_imagen_fuzzy3, ruta_imagen_fuzzy4, tiempo_riego_1_variable, tiempo_riego_4_variable, id_historial_riego))
            connection.commit()
            count = cursor.rowcount
            print("Se han actualizado: ", count)
            cursor.close()
            connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def fuzzy_logic_1_variables_image(par_humedad_suelo, id_historial_riego):
    try:
        humedad_suelo = ctrl.Antecedent(np.arange(0, 1024, 1), 'humedad_suelo')
        tiempo_riego = ctrl.Consequent(np.arange(-2, 18, 1), 'tiempo_riego')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        humedad_suelo['seco'] = fuzz.trimf(humedad_suelo.universe, [0, 100, 200])
        humedad_suelo['semi_seco'] = fuzz.trimf(humedad_suelo.universe, [120, 310, 500])
        humedad_suelo['humedo'] = fuzz.trimf(humedad_suelo.universe, [450, 572, 694])
        humedad_suelo['semi_humedo'] = fuzz.trimf(humedad_suelo.universe, [658, 725, 792])
        humedad_suelo['encharcado'] = fuzz.trimf(humedad_suelo.universe, [750, 887,1024])

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        tiempo_riego['nada'] = fuzz.trimf(tiempo_riego.universe, [-2, -1, 0])
        tiempo_riego['poco'] = fuzz.trimf(tiempo_riego.universe, [0, 2, 4])
        tiempo_riego['medio'] = fuzz.trimf(tiempo_riego.universe, [3, 6, 9])
        tiempo_riego['bastante'] = fuzz.trimf(tiempo_riego.universe, [7, 9, 12])
        tiempo_riego['mucho'] = fuzz.trapmf(tiempo_riego.universe, [10, 13, 17, 17])

        rule1 = ctrl.Rule(humedad_suelo['encharcado'], tiempo_riego['nada'])
        rule2 = ctrl.Rule(humedad_suelo['semi_humedo'], tiempo_riego['poco'])
        rule3 = ctrl.Rule(humedad_suelo['humedo'], tiempo_riego['medio'])
        rule4 = ctrl.Rule(humedad_suelo['semi_seco'], tiempo_riego['bastante'])
        rule5 = ctrl.Rule(humedad_suelo['seco'], tiempo_riego['mucho'])

        tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
        tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        tipping.input['humedad_suelo'] = par_humedad_suelo
        tipping.compute()
        minutos_riego = tipping.output['tiempo_riego']
        grafica = tiempo_riego.view(sim=tipping)
        plt.savefig(ubicacion_imagen_fuzzy1() + id_historial_riego)
        plt.close(grafica)
        if minutos_riego > 0:
            return minutos_riego
        else:
            return 0
    except Exception:
        print("Fuera de rango en las entradas de variables de humedad: ", sys.exc_info()[1], ' humedad suelo:' ,par_humedad_suelo)
        return 0;

def fuzzy_logic_3_variables_image(par_humedad_suelo, par_humedad_ambiental, par_temperatura_ambiental, id_historial_riego):
    try:
        humedad_suelo = ctrl.Antecedent(np.arange(0, 1024, 1), 'humedad_suelo')
        temperatura_ambiental = ctrl.Antecedent(np.arange(5, 46, 1), 'temperatura_ambiental')
        humedad_ambiental = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad_ambiental')
        tiempo_riego = ctrl.Consequent(np.arange(-2, 18, 1), 'tiempo_riego')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        humedad_suelo['seco'] = fuzz.trimf(humedad_suelo.universe, [0, 100, 200])
        humedad_suelo['semi_seco'] = fuzz.trimf(humedad_suelo.universe, [120, 310, 500])
        humedad_suelo['humedo'] = fuzz.trimf(humedad_suelo.universe, [450, 572, 694])
        humedad_suelo['semi_humedo'] = fuzz.trimf(humedad_suelo.universe, [658, 725, 792])
        humedad_suelo['encharcado'] = fuzz.trimf(humedad_suelo.universe, [750, 887,1024])

        temperatura_ambiental['baja'] = fuzz.trimf(temperatura_ambiental.universe, [5, 7, 10])
        temperatura_ambiental['media'] = fuzz.trimf(temperatura_ambiental.universe, [8, 17, 27])
        temperatura_ambiental['alta'] = fuzz.trimf(temperatura_ambiental.universe, [24, 34, 45])

        humedad_ambiental['baja'] = fuzz.trimf(humedad_ambiental.universe, [0, 16, 33])
        humedad_ambiental['media'] = fuzz.trimf(humedad_ambiental.universe, [16, 41, 66])
        humedad_ambiental['alta'] = fuzz.trimf(humedad_ambiental.universe, [41, 70, 100])

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        tiempo_riego['nada'] = fuzz.trimf(tiempo_riego.universe, [-2, -1, 0])
        tiempo_riego['poco'] = fuzz.trimf(tiempo_riego.universe, [0, 2, 4])
        tiempo_riego['medio'] = fuzz.trimf(tiempo_riego.universe, [3, 6, 9])
        tiempo_riego['bastante'] = fuzz.trimf(tiempo_riego.universe, [7, 9, 12])
        tiempo_riego['mucho'] = fuzz.trapmf(tiempo_riego.universe, [10, 13, 17, 17])
        rule1 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                          tiempo_riego['nada'])
        rule2 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                          tiempo_riego['nada'])
        rule3 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                          tiempo_riego['nada'])
        rule4 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                          tiempo_riego['nada'])
        rule5 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                          tiempo_riego['nada'])
        rule6 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                          tiempo_riego['nada'])
        rule7 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                          tiempo_riego['nada'])
        rule8 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                          tiempo_riego['nada'])
        rule9 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                          tiempo_riego['nada'])
        rule10 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                           tiempo_riego['nada'])
        rule11 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                           tiempo_riego['nada'])
        rule12 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule13 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                           tiempo_riego['poco'])
        rule14 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                           tiempo_riego['nada'])
        rule15 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule16 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                           tiempo_riego['medio'])
        rule17 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                           tiempo_riego['poco'])
        rule18 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule19 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                           tiempo_riego['nada'])
        rule20 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                           tiempo_riego['nada'])
        rule21 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule22 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                           tiempo_riego['poco'])
        rule23 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                           tiempo_riego['poco'])
        rule24 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule25 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                           tiempo_riego['medio'])
        rule26 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                           tiempo_riego['poco'])
        rule27 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule28 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                           tiempo_riego['poco'])
        rule29 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                           tiempo_riego['nada'])
        rule30 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                           tiempo_riego['nada'])
        rule31 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                           tiempo_riego['bastante'])
        rule32 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                           tiempo_riego['medio'])
        rule33 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                           tiempo_riego['poco'])
        rule34 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                           tiempo_riego['mucho'])
        rule35 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                           tiempo_riego['bastante'])
        rule36 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                           tiempo_riego['mucho'])
        rule37 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                           tiempo_riego['medio'])
        rule38 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                           tiempo_riego['medio'])
        rule39 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                           tiempo_riego['poco'])
        rule40 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                           tiempo_riego['mucho'])
        rule41 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                           tiempo_riego['mucho'])
        rule42 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                           tiempo_riego['bastante'])
        rule43 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                           tiempo_riego['mucho'])
        rule44 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                           tiempo_riego['mucho'])
        rule45 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                           tiempo_riego['mucho'])

        tipping_ctrl = ctrl.ControlSystem(
            [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14,
             rule15,
             rule16,
             rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29,
             rule30,
             rule31, rule32, rule33, rule34, rule3, rule36,
             rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45])
        tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        tipping.input['humedad_suelo'] = par_humedad_suelo
        tipping.input['humedad_ambiental'] = par_humedad_ambiental
        tipping.input['temperatura_ambiental'] = par_temperatura_ambiental
        tipping.compute()
        minutos_riego = tipping.output['tiempo_riego']
        grafica = tiempo_riego.view(sim=tipping)
        plt.savefig(ubicacion_imagen_fuzzy3() + id_historial_riego)
        plt.close(grafica)
        if minutos_riego >0 :
            return minutos_riego
        else:
            return 0
    except Exception:
        print("Fuera de rango: ", sys.exc_info()[1], ' humedad suelo:', par_humedad_suelo)
        print("Humd Ambiente: ", par_humedad_ambiental)
        print("Temp Ambiente: ", par_temperatura_ambiental)
        return 0;

def fuzzy_logic_4_variables_image(par_humedad_suelo, par_humedad_ambiental, par_temperatura_ambiental, par_evapo, id_historial_riego):
    try:
        humedad_suelo = ctrl.Antecedent(np.arange(0, 1024, 1), 'humedad_suelo')
        temperatura_ambiental = ctrl.Antecedent(np.arange(5, 46, 1), 'temperatura_ambiental')
        humedad_ambiental = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad_ambiental')
        evapo = ctrl.Antecedent(np.arange(0, 9, 1), 'evapo')
        tiempo_riego = ctrl.Consequent(np.arange(-2, 18, 1), 'tiempo_riego')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        humedad_suelo['seco'] = fuzz.trimf(humedad_suelo.universe, [0, 100, 200])
        humedad_suelo['semi_seco'] = fuzz.trimf(humedad_suelo.universe, [120, 310, 500])
        humedad_suelo['humedo'] = fuzz.trimf(humedad_suelo.universe, [450, 572, 694])
        humedad_suelo['semi_encharcado'] = fuzz.trimf(humedad_suelo.universe, [658, 725, 792])
        humedad_suelo['encharcado'] = fuzz.trimf(humedad_suelo.universe, [750, 887,1024])

        temperatura_ambiental['baja'] = fuzz.trimf(temperatura_ambiental.universe, [5, 7, 10])
        temperatura_ambiental['media'] = fuzz.trimf(temperatura_ambiental.universe, [8, 17, 27])
        temperatura_ambiental['alta'] = fuzz.trimf(temperatura_ambiental.universe, [24, 34, 45])

        humedad_ambiental['baja'] = fuzz.trimf(humedad_ambiental.universe, [0, 16, 33])
        humedad_ambiental['media'] = fuzz.trimf(humedad_ambiental.universe, [16, 41, 66])
        humedad_ambiental['alta'] = fuzz.trimf(humedad_ambiental.universe, [41, 70, 100])

        evapo['baja'] = fuzz.trimf(evapo.universe, [0, 2, 4])
        evapo['media'] = fuzz.trimf(evapo.universe, [2, 4, 6])
        evapo['alta'] = fuzz.trimf(evapo.universe, [4, 6, 8])

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        tiempo_riego['nada'] = fuzz.trimf(tiempo_riego.universe, [-2, -1, 0])
        tiempo_riego['poco'] = fuzz.trimf(tiempo_riego.universe, [0, 2, 4])
        tiempo_riego['medio'] = fuzz.trimf(tiempo_riego.universe, [3, 6, 9])
        tiempo_riego['bastante'] = fuzz.trimf(tiempo_riego.universe, [7, 9, 12])
        tiempo_riego['mucho'] = fuzz.trapmf(tiempo_riego.universe, [10, 13, 17, 17])
        rule1 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule2 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule3 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['nada'])
        rule4 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule5 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule6 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['nada'])
        rule7 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule8 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule9 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule10 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule11 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule12 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['nada'])
        rule13 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule14 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule15 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['nada'])
        rule16 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule17 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule18 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule19 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule20 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule21 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['nada'])
        rule22 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule23 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule24 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['nada'])
        rule25 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule26 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule27 = ctrl.Rule(
            humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule28 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule29 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo[
                'media'], tiempo_riego['nada'])
        rule30 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule31 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule32 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                'media'], tiempo_riego['nada'])
        rule33 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule34 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule35 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo[
                'media'], tiempo_riego['nada'])
        rule36 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule37 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule38 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                'media'], tiempo_riego['nada'])
        rule39 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                'alta'], tiempo_riego['poco'])
        rule40 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule41 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                'media'], tiempo_riego['nada'])
        rule42 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule43 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule44 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                'media'], tiempo_riego['nada'])
        rule45 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule46 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule47 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo[
                'media'], tiempo_riego['nada'])
        rule48 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo[
                'alta'], tiempo_riego['medio'])
        rule49 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule50 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                'media'], tiempo_riego['nada'])
        rule51 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                'alta'], tiempo_riego['poco'])
        rule52 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo[
                'baja'], tiempo_riego['nada'])
        rule53 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo[
                'media'], tiempo_riego['nada'])
        rule54 = ctrl.Rule(
            humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo[
                'alta'], tiempo_riego['nada'])
        rule55 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule56 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule57 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['poco'])
        rule58 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule59 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule60 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['nada'])
        rule61 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule62 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule63 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule64 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule65 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule66 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['poco'])
        rule67 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule68 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule69 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['poco'])
        rule70 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule71 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule72 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule73 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule74 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule75 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['medio'])
        rule76 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule77 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule78 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['poco'])
        rule79 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule80 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule81 = ctrl.Rule(
            humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['poco'])
        rule82 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule83 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['nada'])
        rule84 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['poco'])
        rule85 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule86 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['nada'])
        rule87 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['nada'])
        rule88 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule89 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule90 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['nada'])
        rule91 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule92 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['medio'])
        rule93 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['bastante'])
        rule94 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule95 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['poco'])
        rule96 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['medio'])
        rule97 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule98 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule99 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['poco'])
        rule100 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['poco'])
        rule101 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['medio'])
        rule102 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['mucho'])
        rule103 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['poco'])
        rule104 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['medio'])
        rule105 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['bastante'])
        rule106 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['poco'])
        rule107 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['medio'])
        rule108 = ctrl.Rule(
            humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['bastante'])
        rule109 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['nada'])
        rule110 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['poco'])
        rule111 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['medio'])
        rule112 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['nada'])
        rule113 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['poco'])
        rule114 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['medio'])
        rule115 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['nada'])
        rule116 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['nada'])
        rule117 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['poco'])
        rule118 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['medio'])
        rule119 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['bastante'])
        rule120 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['mucho'])
        rule121 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['medio'])
        rule122 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['bastante'])
        rule123 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['mucho'])
        rule124 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['poco'])
        rule125 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['medio'])
        rule126 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['bastante'])
        rule127 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
            tiempo_riego['medio'])
        rule128 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['media'],
            tiempo_riego['bastante'])
        rule129 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
            tiempo_riego['mucho'])
        rule130 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['baja'],
            tiempo_riego['medio'])
        rule131 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['media'],
            tiempo_riego['bastante'])
        rule132 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['alta'],
            tiempo_riego['mucho'])
        rule133 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
            tiempo_riego['medio'])
        rule134 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['media'],
            tiempo_riego['bastante'])
        rule135 = ctrl.Rule(
            humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
            tiempo_riego['mucho'])

        tipping_ctrl = ctrl.ControlSystem([rule1,
                                           rule2,
                                           rule3,
                                           rule4,
                                           rule5,
                                           rule6,
                                           rule7,
                                           rule8,
                                           rule9,
                                           rule10,
                                           rule11,
                                           rule12,
                                           rule13,
                                           rule14,
                                           rule15,
                                           rule16,
                                           rule17,
                                           rule18,
                                           rule19,
                                           rule20,
                                           rule21,
                                           rule22,
                                           rule23,
                                           rule24,
                                           rule25,
                                           rule26,
                                           rule27,
                                           rule28,
                                           rule29,
                                           rule30,
                                           rule31,
                                           rule32,
                                           rule33,
                                           rule34,
                                           rule35,
                                           rule36,
                                           rule37,
                                           rule38,
                                           rule39,
                                           rule40,
                                           rule41,
                                           rule42,
                                           rule43,
                                           rule44,
                                           rule45,
                                           rule46,
                                           rule47,
                                           rule48,
                                           rule49,
                                           rule50,
                                           rule51,
                                           rule52,
                                           rule53,
                                           rule54,
                                           rule55,
                                           rule56,
                                           rule57,
                                           rule58,
                                           rule59,
                                           rule60,
                                           rule61,
                                           rule62,
                                           rule63,
                                           rule64,
                                           rule65,
                                           rule66,
                                           rule67,
                                           rule68,
                                           rule69,
                                           rule70,
                                           rule71,
                                           rule72,
                                           rule73,
                                           rule74,
                                           rule75,
                                           rule76,
                                           rule77,
                                           rule78,
                                           rule79,
                                           rule80,
                                           rule81,
                                           rule82,
                                           rule83,
                                           rule84,
                                           rule85,
                                           rule86,
                                           rule87,
                                           rule88,
                                           rule89,
                                           rule90,
                                           rule91,
                                           rule92,
                                           rule93,
                                           rule94,
                                           rule95,
                                           rule96,
                                           rule97,
                                           rule98,
                                           rule99,
                                           rule100,
                                           rule101,
                                           rule102,
                                           rule103,
                                           rule104,
                                           rule105,
                                           rule106,
                                           rule107,
                                           rule108,
                                           rule109,
                                           rule110,
                                           rule111,
                                           rule112,
                                           rule113,
                                           rule114,
                                           rule115,
                                           rule116,
                                           rule117,
                                           rule118,
                                           rule119,
                                           rule120,
                                           rule121,
                                           rule122,
                                           rule123,
                                           rule124,
                                           rule125,
                                           rule126,
                                           rule127,
                                           rule128,
                                           rule129,
                                           rule130,
                                           rule131,
                                           rule132,
                                           rule133,
                                           rule134,
                                           rule135
                                           ])
        tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        tipping.input['humedad_suelo'] = par_humedad_suelo
        tipping.input['temperatura_ambiental'] = par_temperatura_ambiental
        tipping.input['humedad_ambiental'] = par_humedad_ambiental
        tipping.input['evapo'] = par_evapo
        tipping.compute()
        minutos_riego = tipping.output['tiempo_riego']
        grafica = tiempo_riego.view(sim=tipping)
        plt.savefig(ubicacion_imagen_fuzzy4() + id_historial_riego)
        plt.close(grafica)
        if minutos_riego >0:
            return minutos_riego
        else:
            return 0
    except Exception:
        print("Fuera de rango: ", sys.exc_info()[1], ' humedad suelo:', par_humedad_suelo)
        print("Humd Ambiente: ", par_humedad_ambiental)
        print("Temp Ambiente: ", par_temperatura_ambiental)
        print("Evapotranspiracion: ", par_evapo)
        return 0;

#Si activo estas lineas, al activar el servidor empieza a actualizar las tablas con imagenes
#historial_riegos = cargar_historial_riego()
#actualizar_datos(historial_riegos)