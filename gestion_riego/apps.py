from django.apps import AppConfig


class GestionRiegoConfig(AppConfig):
    name = 'gestion_riego'

    # def ready(self):
    #     from logic_fuzzy import fuzzy_logic
    #     fuzzy_logic.start()