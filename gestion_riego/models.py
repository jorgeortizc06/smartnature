from django.db import models
from datetime import datetime

# Create your models here.
class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100) #unique evitaria agregar valores repatidos
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    tfno = models.CharField(max_length=15)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    temp_ambiente = models.DecimalField(max_digits=100, decimal_places=2)
    humed_ambiente = models.DecimalField(max_digits=100, decimal_places=2)
    humed_suelo = models.DecimalField(max_digits=1023, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True) #establece el valor del campo en la fecha y hora actual cada vez que se guarda el campo
    
    class Meta:
        # sort by "fecha" in descending order unless
        # overridden in the query with order_by()
        ordering = ['-id']

    def __str__(self):
        return str(self.temp_ambiente)+' '+str(self.humed_ambiente)+' '+str(self.humed_suelo)