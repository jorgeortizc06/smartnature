from django.views.generic import TemplateView


class PresentacionView(TemplateView):
    template_name = "gestion_riego/presentacion/presentacion.html"