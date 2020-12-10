import sys
import time
from datetime import datetime, timedelta
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import psycopg2

activacion = False
fin_riego = ''

def regar(plataforma):
    global activacion
    global fin_riego
    print(activacion)
    print(datetime.now())
    if (time.strftime("%H:%M:%S") ==  plataforma['horario1'] or time.strftime("%H:%M:%S") ==  plataforma['horario2'] or time.strftime("%H:%M:%S") ==  plataforma['horario3'] or time.strftime("%H:%M:%S") == time.strftime("%H:%M:%S") ) and activacion == False:
        try:
            """if time.strftime("%H:%M:%S") == plataforma['horario1']:
                # Voy un dia atras
                d = datetime.today() - timedelta(days=1)
                fechaDesde = d.strftime("%Y-%m-%d") + " " + plataforma['horario3']
                #Dia de hoy
                fechaHasta = time.strftime("%Y-%m-%d") + " " + plataforma['horario1']
            elif time.strftime("%H:%M:%S") == plataforma['horario2']:
                fechaDesde = time.strftime("%Y-%m-%d") + " " + plataforma['horario1']
                fechaHasta = time.strftime("%Y-%m-%d") + " " + plataforma['horario2']
            elif time.strftime("%H:%M:%S") == plataforma['horario3']:
                fechaDesde = time.strftime("%Y-%m-%d") + " " + plataforma['horario2']
                fechaHasta = time.strftime("%Y-%m-%d") + " " + plataforma['horario3']"""
            fechaDesde = time.strftime("%Y-%m-%d") + " " + plataforma['horario2']
            fechaHasta = time.strftime("%Y-%m-%d") + " " + plataforma['horario3']
            print("Fecha Desde", fechaDesde)
            print("Fecha Desde", fechaHasta)
            prom_hum_suelo1 = calcular_promedio(fechaDesde, fechaHasta, 1, 1)
            prom_hum_suelo2 = calcular_promedio(fechaDesde, fechaHasta, 2, 1)
            prom_hum_suelo3 = calcular_promedio(fechaDesde, fechaHasta, 3, 1)
            prom_hum_suelo4 = calcular_promedio(fechaDesde, fechaHasta, 4, 1)
            promedio_hum_suelo_total = (prom_hum_suelo1+prom_hum_suelo2+prom_hum_suelo3+prom_hum_suelo4)/4

            prom_hum_ambient = calcular_promedio(fechaDesde, fechaHasta, 1, 2)
            prom_temp_ambient = calcular_promedio(fechaDesde, fechaHasta, 1, 3)


            tiempo_riego_suelo1 = round(fuzzy_logic_3_variables(float(prom_hum_suelo1), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
            tiempo_riego_suelo2 = round(fuzzy_logic_3_variables(float(prom_hum_suelo2), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
            tiempo_riego_suelo3 = round(fuzzy_logic_3_variables(float(prom_hum_suelo3), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
            tiempo_riego_suelo4 = round(fuzzy_logic_3_variables(float(prom_hum_suelo4), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
            tiempo_riego_suelo_promedio = round(fuzzy_logic_3_variables(float(promedio_hum_suelo_total), float(prom_hum_ambient), float(prom_temp_ambient)), 2)
            if tiempo_riego_suelo_promedio != 0:
                ahora = datetime.datetime.now()
                futuro = ahora + datetime.timedelta(minutes=tiempo_riego_suelo1)
                fin_riego = futuro.strftime("%H:%M:%S")
                print("Fin Riego: ",fin_riego)
                activacion = True
            else:
                print("Tiempo 0, no se abrira la llave")
        except UnboundLocalError:
            print("No hay datos para fecha desde o fecha hasta: ", sys.exc_info()[1])
    elif time.strftime("%H:%M:%S") == fin_riego and activacion == True:
        print("La llave se ha cerrado")
        activacion = False

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


plataforma = {'horario1':'08:00:00', 'horario2':'12:00:00', 'horario3':'18:34:15'}

while True:
    regar(plataforma)
    time.sleep(1)