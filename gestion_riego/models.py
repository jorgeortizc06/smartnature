from django.db import models
from django.db.models import DateTimeField
from django.forms import model_to_dict

# Create your models here.
class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='nombre')  # unique evitaria agregar valores repatidos
    apellido = models.CharField(max_length=100, verbose_name='apellido')
    email = models.EmailField(max_length=200)
    tfno = models.CharField(max_length=15, verbose_name='teléfono')
    password = models.CharField(max_length=15, verbose_name='contraseña')

    def __str__(self):
        return self.nombre

    # Transforma mis datos del modelo Persona a JSON para mejor manejo en javascript
    def toJSON(self):
        item = model_to_dict(self)  # tambien puedes excluir algunos parametros (self, exclude=['])
        return item

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['id']


class TipoSensor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, null=True, blank=True, verbose_name='descripción')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'TipoSensor'
        verbose_name_plural = 'TipoSensores'
        ordering = ['id']


class Planta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, verbose_name='descripción')
    tiempo_produccion = models.IntegerField(null=True, verbose_name='tiempo de Producción')

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
    descripcion = models.CharField(max_length=300, blank=True, verbose_name='descripción')
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


class TipoLogicaDifusa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=300, blank=True, verbose_name='descripción')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'TipoLogicaDifusa'
        verbose_name_plural = 'TiposLogicaDifusa'
        ordering = ['id']

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=300, blank=True, verbose_name='descripción')
    ip = models.CharField(max_length=20, default='192.168.100.254')
    topic = models.CharField(max_length=300, default='device1/#', unique=True, verbose_name='tópico')
    puerto = models.IntegerField(default=9001)
    frecuencia_actualizacion = models.IntegerField(default=30, verbose_name='frecuencia de actualización')
    tipo_logica_difusa = models.ForeignKey(TipoLogicaDifusa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo_logica_difusa'] = self.tipo_logica_difusa.nombre
        return item

    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'
        ordering = ['id']


class TipoRol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)  # Humano o Logica Difusa
    descripcion = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'TipoRol'
        verbose_name_plural = 'TipoRoles'
        ordering = ['id']


class Plataforma(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, verbose_name='descripción')
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    horario1 = models.CharField(max_length=10, default='08:00:00')
    horario2 = models.CharField(max_length=10, default='12:00:00')
    horario3 = models.CharField(max_length=10, default='17:00:00')
    tipo_suelo = models.ForeignKey(TipoSuelo, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo_suelo'] = self.tipo_suelo.nombre
        item['device'] = self.device.nombre
        return item

    class Meta:
        verbose_name = 'Plataforma'
        verbose_name_plural = 'Plataformas'
        ordering = ['id']


class Siembra(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_siembra = models.DateTimeField()
    cantidad_plantas = models.IntegerField()
    distancia_siembra = models.DecimalField(max_digits=3, decimal_places=2)
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['plataforma'] = self.plataforma.nombre
        item['planta'] = self.planta.nombre
        return item

    class Meta:
        verbose_name = 'Siembra'
        verbose_name_plural = 'Siembras'
        ordering = ['id']


class HistorialRiego(models.Model):
    id = models.AutoField(primary_key=True)
    tiempo_riego = models.DecimalField(max_digits=3, decimal_places=2)
    fecha_riego = models.DateTimeField(auto_now_add=True)
    codigo_sensor = models.IntegerField()
    valor_humed_suelo = models.DecimalField(max_digits=1000, decimal_places=2)
    valor_humed_ambiente = models.DecimalField(max_digits=1000, decimal_places=2)
    valor_temp_ambiente = models.DecimalField(max_digits=1000, decimal_places=2)
    valor_evapotranspiracion = models.DecimalField(max_digits=1000, decimal_places=2)
    siembra = models.ForeignKey(Siembra, on_delete=models.CASCADE)
    tipo_rol = models.ForeignKey(TipoRol, on_delete=models.CASCADE)
    tipo_logica_difusa = models.ForeignKey(TipoLogicaDifusa, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_riego'] = self.fecha_riego.strftime('%d-%m-%Y %H:%M')
        item['device'] = self.siembra.plataforma.device.nombre
        item['persona'] = self.siembra.plataforma.persona.nombre + ' ' + self.siembra.plataforma.persona.apellido
        item['tipo_rol'] = self.tipo_rol.nombre
        item['tipo_logica_difusa'] = self.tipo_logica_difusa.nombre
        return item

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
    fecha_registro = models.DateTimeField(
        auto_now_add=True)  # establece el valor del campo en la fecha y hora actual cada vez que se guarda el campo
    estado = models.CharField(max_length=1)
    tipo_sensor = models.ForeignKey(TipoSensor, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_registro'] = self.fecha_registro.strftime('%d-%m-%Y %H:%M')
        item['tipo_sensor'] = self.tipo_sensor.toJSON()  # llamar al metodo toJSON() en caso de ser foreignKey
        item['value'] = format(self.value, '.2f')
        item['device'] = self.device.toJSON()
        return item

    class Meta:
        # sort by "fecha" in descending order unless
        # overridden in the query with order_by()
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'
        ordering = ['-id']
