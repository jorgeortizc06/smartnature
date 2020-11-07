import psycopg2
import datetime
import numpy as np
import paho.mqtt.client
import psycopg2
import requests
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Tipo Sensor: 1 Humedad suelo, 2 Humedad Ambiental, 3 Temperatura Ambiental
def calcular_promedio(fecha_inicio, fecha_fin, codigo_sensor, tipo_sensor):
    conexion = psycopg2.connect(host="192.168.0.254", database="smartnature", user="jorge", password="jorge")
    cur = conexion.cursor()
    # Ejecutamos una consulta
    sql = """select round(avg(value), 2) 
    from gestion_riego_sensor grs 
    where fecha_registro >= %s::timestamp AT TIME ZONE 'America/Guayaquil' 
    and fecha_registro <= %s::timestamp AT TIME ZONE 'America/Guayaquil'
    and codigo_sensor = %s
    and tipo_sensor_id = %s
    group by tipo_sensor_id"""
    cur.execute(sql, (fecha_inicio, fecha_fin, codigo_sensor, tipo_sensor))
    # Recorremos los resultados y los mostramos
    datas = cur.fetchone()
    print(datas[0])
    cur.close()
    # Cerramos la conexión
    conexion.close()

    return datas[0]

prom_hum_suelo = calcular_promedio('2020-11-4 21:00:00', '2020-11-4 21:10:59', 1, 1)
prom_hum_ambient = calcular_promedio('2020-11-4 21:00:00', '2020-11-4 21:10:59', 1, 2)
prom_temp_ambient = calcular_promedio('2020-11-4 21:00:00', '2020-11-4 21:10:59', 1, 3)



