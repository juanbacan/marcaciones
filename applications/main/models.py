from django.db import models

from core.models import ModeloBase
# Create your models here.

class UsuarioAsistencia(ModeloBase):
    nombre_completo = models.CharField(max_length=255)
    usuario_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.nombre_completo


class RegistroAsistencia(ModeloBase):
    usuario = models.ForeignKey(UsuarioAsistencia, on_delete=models.CASCADE)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    status = models.IntegerField()
    verificacion = models.IntegerField()
    entrada_salida = models.IntegerField()
    extra = models.IntegerField()

    def __str__(self):
        return f"{self.usuario.nombre_completo} - {self.hora.strftime('%Y-%m-%d %H:%M:%S')}"
    
    @property
    def solo_fecha_str_prop(self):
        return self.fecha.strftime('%Y-%m-%d')
    
    @property
    def solo_hora_str_prop(self):
        return self.hora.strftime('%H:%M:%S')


class ArchivoTemporal(ModeloBase):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='archivos_temporales/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Archivo Temporal"
        verbose_name_plural = "Archivos Temporales"