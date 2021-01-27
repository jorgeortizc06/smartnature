import time
from datetime import datetime, timedelta

import psycopg2
from apscheduler.schedulers.background import BackgroundScheduler
from gestion_riego.models import Plataforma

from gestion_riego.IoT.ProcesoRiego import Regar
riego = Regar()


def ejecutar_horario_1():
    # Voy un dia atras
    d = datetime.today() - timedelta(days=1)
    fecha_desde = d.strftime("%d/%m/%Y") + " " + '17:00:00'
    # Dia de hoy
    fecha_hasta = time.strftime("%d/%m/%Y") + " " + '08:00:00'
    riego.proceder_riego(fecha_desde, fecha_hasta)


def ejecutar_horario_2():
    fecha_desde = time.strftime("%d/%m/%Y") + " " + '08:00:00'
    fecha_hasta = time.strftime("%d/%m/%Y") + " " + '12:00:00'
    riego.proceder_riego(fecha_desde, fecha_hasta)


def ejecutar_horario_3():
    fecha_desde = time.strftime("%d/%m/%Y") + " " + '12:00:00'
    fecha_hasta = time.strftime("%d/%m/%Y") + " " + '17:00:00'
    riego.proceder_riego(fecha_desde, fecha_hasta)


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