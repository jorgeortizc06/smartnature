from datetime import datetime, timedelta
import time
import psycopg2

def ejecutar_horario_1():
    # Voy un dia atras
    d = datetime.today() - timedelta(days=1)
    fecha_desde = d.strftime("%Y-%m-%d") + " " + '17:00:00'
    # Dia de hoy
    fecha_hasta = time.strftime("%Y-%m-%d") + " " + '08:00:00'
    regar(fecha_desde, fecha_hasta)



def regar(fechaDesde, fechaHasta):
    prom_temp_ambient = calcular_promedio(fechaDesde, fechaHasta, 1, 3)
    prom_hum_ambient = calcular_promedio(fechaDesde, fechaHasta, 1, 2)
    tdmax = obtenerMax(fechaDesde, fechaHasta, 1, 3)
    tdmin = obtenerMin(fechaDesde, fechaHasta, 1, 3)
    evapo = round(calcularEvapotranspiracion(11.9, float(prom_temp_ambient), float(tdmax), float(tdmin)), 2)
    print("La evapotranspiracion es: ", evapo)


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

ejecutar_horario_1()