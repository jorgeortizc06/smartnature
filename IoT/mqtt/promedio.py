import psycopg2


# Tipo Sensor: 1 Humedad suelo, 2 Humedad Ambiental, 3 Temperatura Ambiental
def calcular_promedio_humedad(fecha_inicio, fecha_fin, codigo_sensor, tipo_sensor):
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


#prom_hum_suelo=calcular_promedio('2020-11-10 18:00:00', '2020-11-10 18:10:59', 1, 1)
# prom_hum_ambient = calcular_promedio('2020-11-4 21:00:00', '2020-11-4 21:10:59', 1, 2)
# prom_temp_ambient = calcular_promedio('2020-11-4 21:00:00', '2020-11-4 21:10:59', 1, 3)
