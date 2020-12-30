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

            if tipo_logica_difusa.id == 1:
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
                tiempo_riego_suelo_promedio = 0

            tdmax = obtenerMax(fechaDesde, fechaHasta, 1, 3)
            tdmin = obtenerMin(fechaDesde, fechaHasta, 1, 3)
            evapo = round(calcularEvapotranspiracion(11.9, float(prom_hum_ambient), float(tdmax), float(tdmin)),2)
            print("Calcular Evapo: ", evapo)
            print("tiempo Sensor 1: ", tiempo_riego_suelo1)
            print("tiempo Sensor 2: ", tiempo_riego_suelo2)
            print("tiempo Sensor 3: ", tiempo_riego_suelo3)
            print("tiempo Sensor 4: ", tiempo_riego_suelo4)
            print("tiempo Sensor 5: ", tiempo_riego_suelo_promedio)

            if tiempo_riego_suelo_promedio > 0:
                ahora = datetime.now()
                futuro = ahora + timedelta(minutes=tiempo_riego_suelo_promedio)
                fin_riego = futuro.strftime("%H:%M:%S")
                print("Fin Riego: ", fin_riego)
                activacion = True
                # historial_riego = {"tiempo_riego": float(tiempo_riego), "siembra": 1, "tipo_rol": 2}
                # et_historial_riego = requests.post(api_historial_riego, data=json.dumps(historial_riego), headers=headers)
                client = paho.mqtt.client.Client(client_id='albert-subs')
                client.connect(host='192.168.100.254', port=1883)
                enviando = client.publish("device1/electrovalvula", "ON")
                print("Mqtt ON: ", enviando)
                riego_promedio = HistorialRiego(tiempo_riego=tiempo_riego_suelo_promedio, siembra=siembra,
                                                codigo_sensor=5,
                                                valor_humed_suelo=promedio_hum_suelo_total,
                                                valor_humed_ambiente=prom_hum_ambient,
                                                valor_temp_ambiente=prom_temp_ambient,
                                                valor_evapotranspiracion=evapo,
                                                tipo_rol=tipo_rol,
                                                tipo_logica_difusa=tipo_logica_difusa)
                riego_promedio.save()
            elif tiempo_riego_suelo_promedio <= 0:
                print("Tiempo 0, no se abrira la llave")
                riego5 = HistorialRiego(tiempo_riego=0, siembra=siembra, codigo_sensor=5,
                                        valor_humed_suelo=promedio_hum_suelo_total,
                                        valor_humed_ambiente=prom_hum_ambient,
                                        valor_temp_ambiente=prom_temp_ambient,
                                        valor_evapotranspiracion=evapo,
                                        tipo_rol=tipo_rol,
                                        tipo_logica_difusa=tipo_logica_difusa)
                riego5.save()

            riego_sensor_suelo_1 = HistorialRiego(tiempo_riego=tiempo_riego_suelo1, siembra=siembra, codigo_sensor=1,
                                                  valor_humed_suelo=prom_hum_suelo1,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_1.save()

            riego_sensor_suelo_2 = HistorialRiego(tiempo_riego=tiempo_riego_suelo2, siembra=siembra, codigo_sensor=2,
                                                  valor_humed_suelo=prom_hum_suelo2,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_2.save()

            riego_sensor_suelo_3 = HistorialRiego(tiempo_riego=tiempo_riego_suelo3, siembra=siembra, codigo_sensor=3,
                                                  valor_humed_suelo=prom_hum_suelo3,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_3.save()
            riego_sensor_suelo_4 = HistorialRiego(tiempo_riego=tiempo_riego_suelo4, siembra=siembra, codigo_sensor=4,
                                                  valor_humed_suelo=prom_hum_suelo4,
                                                  valor_humed_ambiente=prom_hum_ambient,
                                                  valor_temp_ambiente=prom_temp_ambient,
                                                  valor_evapotranspiracion=evapo,
                                                  tipo_rol=tipo_rol,
                                                  tipo_logica_difusa=tipo_logica_difusa)
            riego_sensor_suelo_4.save()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

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
        print("Sali del bucle")





# Funcion para la obtencion de la evapotranspiracion. Fuente: https://hidrologia.usal.es/temas/Evapotransp.pdf
def calcularEvapotranspiracion(R0, tmed, tdmax, tdmin):
    et0 = 0.0023 * (tmed + 17.78) * (R0) * (tdmax - tdmin) ** (0.5)
    return et0


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


def fuzzy_logic_1_variables(par_humedad_suelo):
    try:
        humedad_suelo = ctrl.Antecedent(np.arange(0, 1024, 1), 'humedad_suelo')
        tiempo_riego = ctrl.Consequent(np.arange(-2, 18, 1), 'tiempo_riego')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        humedad_suelo['seco'] = fuzz.trimf(humedad_suelo.universe, [0, 100, 200])
        humedad_suelo['semi_seco'] = fuzz.trimf(humedad_suelo.universe, [120, 310, 500])
        humedad_suelo['humedo'] = fuzz.trimf(humedad_suelo.universe, [450, 572, 694])
        humedad_suelo['semi_humedo'] = fuzz.trimf(humedad_suelo.universe, [658, 725, 792])
        humedad_suelo['encharcado'] = fuzz.trimf(humedad_suelo.universe, [750, 825, 900])

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
        print(tipping.output['tiempo_riego'])
        return tipping.output['tiempo_riego']
    except Exception:
        print("Fuera de rango en las entradas de variables de humedad", sys.exc_info()[1])
        return 0;

def fuzzy_logic_3_variables(par_humedad_suelo, par_humedad_ambiental, par_temperatura_ambiental):
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
        humedad_suelo['encharcado'] = fuzz.trimf(humedad_suelo.universe, [750, 825, 900])

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
        print(tipping.output['tiempo_riego'])
        return tipping.output['tiempo_riego']
    except Exception:
        print("Fuera de rango en las entradas de variables de humedad, temperatura, etc: ", sys.exc_info()[1])
        return 0;
