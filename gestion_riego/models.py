from django.db import models
from datetime import datetime
from django.forms import model_to_dict
# Create your models here.
class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre') #unique evitaria agregar valores repatidos
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    email = models.EmailField(max_length=200)
    tfno = models.CharField(max_length=15, verbose_name='Telefono')
    password = models.CharField(max_length=15, verbose_name='Contraseña')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self) #tambien puedes excluir algunos parametros (self, exclude=['])
        return item

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['id']

class TipoSensor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, null = True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'TipoSensor'
        verbose_name_plural = 'TipoSensores'
        ordering = ['id']

class Planta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    tiempo_produccion = models.IntegerField(null=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Planta'
        verbose_name_plural = 'Plantas'
        ordering = ['id']

class TipoSuelo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    densidad = models.DecimalField(max_digits=1000, decimal_places=2)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        verbose_name = 'TipoSuelo'
        verbose_name_plural = 'TipoSuelos'
        ordering = ['id']

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=300, verbose_name='Descripcion', blank=True)
    ip = models.CharField(max_length = 20, default='192.168.0.254')
    topic = models.CharField(max_length=300, default = 'device1/#', unique=True)
    puerto = models.IntegerField(default=9001)
    
    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'
        ordering = ['id']

class TipoRol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100) #Humano o Logica Difusa
    descripcion = models.CharField(max_length=300)
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'TipoRol'
        verbose_name_plural = 'TipoRoles'
        ordering = ['id']

class Plataforma(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null = True)
    horario1 = models.CharField(max_length = 8, default='8:00')
    horario2 = models.CharField(max_length = 8, default='17:00')
    tipo_suelo = models.ForeignKey(TipoSuelo, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Plataforma'
        verbose_name_plural = 'Plataformas'
        ordering = ['id']

class Siembra(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_siembra = models.DateTimeField()
    cantidad_plantas = models.IntegerField()
    distancia_siembra = models.DecimalField(max_digits=3, decimal_places=2)
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE, null = True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return str(self.id)


class HistorialRiego(models.Model):
    id = models.AutoField(primary_key=True)
    tiempo_riego = models.DecimalField(max_digits=3, decimal_places=2)
    fecha_riego = models.DateTimeField(auto_now_add=True)
    siembra = models.ForeignKey(Siembra, on_delete=models.CASCADE, null = True)
    tipo_rol = models.ForeignKey(TipoRol, on_delete=models.CASCADE, null = True)

    class Meta:
        # sort by "fecha" in descending order unless
        # overridden in the query with order_by()
        verbose_name = 'HistorialRiego'
        verbose_name_plural = 'HistorialRiegos'
        ordering = ['-id']

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
