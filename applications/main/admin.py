from django.contrib import admin

# Register your models here.
from .models import UsuarioAsistencia, RegistroAsistencia


class UsuarioAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'usuario_id')
    search_fields = ('nombre_completo', 'usuario_id')

admin.site.register(UsuarioAsistencia, UsuarioAsistenciaAdmin)


class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'hora', 'status')
    search_fields = ('usuario__nombre_completo', 'fecha', 'hora')
    list_filter = ('usuario', 'status', 'entrada_salida')

admin.site.register(RegistroAsistencia, RegistroAsistenciaAdmin)