from django.db import models

from core.models import ModeloBase
# Create your models here.

class UsuarioAsistencia(ModeloBase):
    nombre_completo = models.CharField(max_length=255)
    usuario_id = models.IntegerField(unique=True)


class RegistroAsistencia(ModeloBase):
    usuario = models.ForeignKey(UsuarioAsistencia, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    status = models.IntegerField()
    verificacion = models.IntegerField()
    entrada_salida = models.IntegerField()
    extra = models.IntegerField()

    def __str__(self):
        return f"{self.usuario.nombre_completo} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')} - {self.get_status_display()}"