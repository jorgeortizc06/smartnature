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

class TipoSensor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, null = True)

    def __str__(self):
        return self.nombre

class Planta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre

class TipoSuelo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    densidad = models.DecimalField(max_digits=1000, decimal_places=2)

    def __str__(self):
        return self.nombre

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    ip = models.CharField(max_length = 20, default='192.168.0.6')
    topic = models.CharField(max_length=300, default = 'device1/#')
    puerto = models.IntegerField(default=9001)
    def __str__(self):
        return self.nombre

class TipoRol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100) #Humano o Logica Difusa
    descripcion = models.CharField(max_length=300)
    def __str__(self):
        return self.nombre

class HistorialRiego(models.Model):
    id = models.AutoField(primary_key=True)
    tiempo_riego = models.DecimalField(max_digits=3, decimal_places=2)
    fecha_riego = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null = True)
    tipo_rol = models.ForeignKey(TipoRol, on_delete=models.CASCADE, null = True)

class Plataforma(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, null = True)
    tipo_suelo = models.ForeignKey(TipoSuelo, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.nombre

class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=1000, decimal_places=2)
    codigo_sensor = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True) #establece el valor del campo en la fecha y hora actual cada vez que se guarda el campo
    estado = models.CharField(max_length=1)
    tipo_sensor = models.ForeignKey(TipoSensor, on_delete=models.CASCADE, null = True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null = True)
    
    class Meta:
        # sort by "fecha" in descending order unless
        # overridden in the query with order_by()
        ordering = ['-id']
