import os
import sys
#Las configuraciones esta en el proyecto princial, necesito estar alli, asi que primero
#print(sys.path) veo mi path, estoy dentro de de varias carpetas de la raiz
#asi que dejo posicionarme en el proyecto raiz como ha continuacion
PROJECT_ROOT = sys.path.insert(0,"/casaortiz/django/smartnature")
#print("Tu base es:", PROJECT_ROOT)
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_asgi_application()  # modulo para importar los settings django y trabajar con modelos

from apscheduler.schedulers.blocking import BlockingScheduler
from gestion_riego.models import Plataforma
import time
from datetime import datetime, timedelta
from gestion_riego.IoT.ProcesoRiego import Regar


class DefinirRiego:
    riego = Regar()

    def job(self, text):
        print(Plataforma.objects.first())

    #tarea programa para el riego de las 8:00
    def ejecutar_horario_1(self):
        # Voy un dia atras
        plataformas = Plataforma.objects.all()
        for plataforma in plataformas:
            tipo_logica_difusa = plataforma.device.tipo_logica_difusa
            d = datetime.today() - timedelta(days=1)
            fecha_desde = d.strftime("%d/%m/%Y") + " " + '17:00:00'
            # Dia de hoy
            fecha_hasta = time.strftime("%d/%m/%Y") + " " + '08:00:00'
            self.riego.proceder_riego(fecha_desde, fecha_hasta, tipo_logica_difusa)

    # tarea programa para el riego de las 12:00
    def ejecutar_horario_2(self):
        plataformas = Plataforma.objects.all()
        for plataforma in plataformas:
            tipo_logica_difusa = plataforma.device.tipo_logica_difusa
            fecha_desde = time.strftime("%d/%m/%Y") + " " + '08:00:00'
            fecha_hasta = time.strftime("%d/%m/%Y") + " " + '12:00:00'
            self.riego.proceder_riego(fecha_desde, fecha_hasta, tipo_logica_difusa)

    # tarea programa para el riego de las 17:00
    def ejecutar_horario_3(self):
        plataformas = Plataforma.objects.all()
        for plataforma in plataformas:
            tipo_logica_difusa = plataforma.device.tipo_logica_difusa
            print("Id de tipo logica difusa: ", tipo_logica_difusa)
            fecha_desde = time.strftime("%d/%m/%Y") + " " + '12:00:00'
            fecha_hasta = time.strftime("%d/%m/%Y") + " " + '17:00:00'
            self.riego.proceder_riego(fecha_desde, fecha_hasta, tipo_logica_difusa)

    #Inicializa la tarea con los horarios definidos para apscheduler
    def start(self):
        scheduler = BlockingScheduler()
        scheduler.add_job(self.ejecutar_horario_1, 'cron', day_of_week='mon-sun', hour=8, minute=0)
        scheduler.add_job(self.ejecutar_horario_2, 'cron', day_of_week='mon-sun', hour=12, minute=0)
        scheduler.add_job(self.ejecutar_horario_3, 'cron', day_of_week='mon-sun', hour=17, minute=0)
        scheduler.start()


definir_riego = DefinirRiego()
definir_riego.start()
