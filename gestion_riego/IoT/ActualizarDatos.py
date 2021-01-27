# import os
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# application = get_asgi_application()  # modulo para importar los settings django y trabajar con modelos

from django.db.models import Q
from gestion_riego.models import HistorialRiego
# Tipo Sensor: 1 Humedad suelo, 2 Humedad Ambiental, 3 Temperatura Ambiental
from gestion_riego.IoT.LogicaDifusa import LogicaDifusa


class ActualizarDatos:
    def get_historial_riego(self):
        historial_riegos = HistorialRiego.objects.filter(
            Q(image_1_variable='') | Q(image_3_variable='') | Q(image_4_variable=''))
        return historial_riegos

    def actualizar_datos(self):
        historial_riegos = self.get_historial_riego()

        if historial_riegos:

            for historial_riego in historial_riegos:
                tmp_historial_riego = historial_riego
                logica_difusa = LogicaDifusa()
                tiempo_riego_1_variable = round(
                    logica_difusa.fuzzy_logic_1_variables_image(float(tmp_historial_riego.valor_humed_suelo),
                                                          str(tmp_historial_riego.id)), 2)
                tiempo_riego_3_variable = round(
                    logica_difusa.fuzzy_logic_3_variables_image(float(tmp_historial_riego.valor_humed_suelo),
                                                          float(tmp_historial_riego.valor_humed_ambiente),
                                                          float(tmp_historial_riego.valor_temp_ambiente),
                                                          str(tmp_historial_riego.id)), 2)
                tiempo_riego_4_variable = round(
                    logica_difusa.fuzzy_logic_4_variables_image(float(tmp_historial_riego.valor_humed_suelo),
                                                          float(tmp_historial_riego.valor_humed_ambiente),
                                                          float(tmp_historial_riego.valor_temp_ambiente),
                                                          float(tmp_historial_riego.valor_evapotranspiracion),
                                                          str(tmp_historial_riego.id)), 2)
                ruta_imagen_fuzzy1 = 'fuzzy1/' + str(tmp_historial_riego.id) + '.png'
                ruta_imagen_fuzzy3 = 'fuzzy3/' + str(tmp_historial_riego.id) + '.png'
                ruta_imagen_fuzzy4 = 'fuzzy4/' + str(tmp_historial_riego.id) + '.png'
                print("Ruta imagen fuzzy1: ", ruta_imagen_fuzzy1)
                print("Ruta imagen fuzzy3: ", ruta_imagen_fuzzy3)
                print("Ruta imagen fuzzy4: ", ruta_imagen_fuzzy4)
                print("LOGICA DIFUSA====================")
                print(tiempo_riego_1_variable)
                tmp_historial_riego.tiempo_riego_1_variable = tiempo_riego_1_variable
                tmp_historial_riego.tiempo_riego = tiempo_riego_3_variable
                tmp_historial_riego.tiempo_riego_4_variable = tiempo_riego_4_variable
                tmp_historial_riego.image_1_variable = ruta_imagen_fuzzy1
                tmp_historial_riego.image_3_variable = ruta_imagen_fuzzy3
                tmp_historial_riego.image_4_variable = ruta_imagen_fuzzy4
                tmp_historial_riego.save()
        else:
            print("No hay datos")


# actualizar_datos = ActualizarDatos()
# historial_riegos = actualizar_datos.actualizar_datos()
