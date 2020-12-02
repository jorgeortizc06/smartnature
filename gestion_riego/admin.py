from django.contrib import admin

from .models import Persona, TipoRol, Siembra, Sensor

# Register your models here.

admin.site.register(Persona)
admin.site.register(TipoRol)
admin.site.register(Siembra)
admin.site.register(Sensor)
