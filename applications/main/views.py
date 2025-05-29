import datetime
import pandas as pd
import io
from django.core.files.base import ContentFile
from django.utils.timezone import make_aware
from zoneinfo import ZoneInfo  # desde Python 3.9
from django.shortcuts import render
from django.views.generic import View

from .forms import ProcesoMarcacionForm
from core.utils import success_json, error_json
from core.utils import queryset_to_excel

from .models import UsuarioAsistencia, RegistroAsistencia, ArchivoTemporal
from core.views import ViewClassBase

def cargar_usuarios_desde_dat(archivo):
    for linea in archivo:
        try:
            linea = linea.decode('utf-8').strip()
            partes = linea.split()
            if partes and partes[-1].isdigit():
                usuario_id = int(partes[-1])
                nombre = ' '.join(partes[:-1])
                UsuarioAsistencia.objects.update_or_create(
                    usuario_id=usuario_id,
                    defaults={"nombre_completo": nombre}
                )
        except Exception as e:
            print(f"Error procesando línea: {linea} -> {e}")


def procesar_archivo_attlog(archivo):
    RegistroAsistencia.objects.all().delete()

    for linea in archivo:
        try:
            partes = linea.decode('utf-8').strip().split('\t')
            if partes[1] == '2025-05-01 07:08:16':
                print("Here")
            if len(partes) >= 6:
                usuario_id = int(partes[0])
                dt = datetime.datetime.strptime(partes[1], "%Y-%m-%d %H:%M:%S")
                solo_fecha = dt.date()  # → datetime.date(2025, 5, 1)
                solo_hora = dt.time()   # → datetime.time(7, 8, 16)

                status = int(partes[2])
                verificacion = int(partes[3])
                entrada_salida = int(partes[4])
                extra = int(partes[5])

                usuario = UsuarioAsistencia.objects.filter(usuario_id=usuario_id).first()
                if usuario:
                    registro = RegistroAsistencia.objects.create(
                        usuario=usuario,
                        fecha = solo_fecha,
                        hora = solo_hora,
                        status=status,
                        verificacion=verificacion,
                        entrada_salida=entrada_salida,
                        extra=extra
                    )
                else:
                    print(f"⚠️ Usuario con ID {usuario_id} no encontrado.")
        except Exception as e:
            print(f"❌ Error procesando línea: {linea} -> {e}")


class HomeView(ViewClassBase):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        if self.action and hasattr(self, f'get_{self.action}'):
            return getattr(self, f'get_{self.action}')(request, context, *args, **kwargs)
        
        context['form'] = ProcesoMarcacionForm()
        return render(request, 'main/home.html', context)
    
    # def get(self, request, *args, **kwargs):
    #     context = {}
    #     context['form'] = ProcesoMarcacionForm()
    #     return render(request, 'main/home.html', context)
    

    def post(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
            if self.action and hasattr(self, f'post_{self.action}'):
                return getattr(self, f'post_{self.action}')(request, context, *args, **kwargs)
            
            form = ProcesoMarcacionForm(request.POST, request.FILES)
            if form.is_valid():
                archivo_usuarios = form.cleaned_data.get('archivo_usuarios')
                cargar_usuarios_desde_dat(archivo_usuarios)

                archivo_marcaciones = form.cleaned_data.get('archivo_marcaciones')
                procesar_archivo_attlog(archivo_marcaciones)


                fecha_inicio = form.cleaned_data.get('fecha_inicio')
                fecha_fin = form.cleaned_data.get('fecha_fin')

                # Generar un DataFrame de pandas para exportar a Excel y guardar en un archivo temporal

                registros = RegistroAsistencia.objects.filter(
                    fecha__gte=fecha_inicio,
                    fecha__lte=fecha_fin
                ).order_by('usuario__usuario_id')

                output = queryset_to_excel(
                    queryset=registros,
                    headers = ['Nombre', 'Fecha', 'Hora'],
                    fields = ['usuario', 'solo_fecha_str_prop', 'solo_hora_str_prop'],
                    sheet_name='Registros Asistencia',
                )

                archivo_temporal = ArchivoTemporal.objects.create(nombre='archivo.xlsx')  # Crea el objeto sin archivo

                # Guardar el archivo en el campo FileField con un nombre
                archivo_temporal.archivo.save(
                    f'registros_asistencia_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                    ContentFile(output.read())
                )

                return error_json(mensaje='La url de descarga del archivo es: ' + "http://localhost:8000" +  archivo_temporal.archivo.url)
            else:
                return error_json(forms=[form])
            
        except Exception as e:
            print(f"Error en la carga de archivos: {e}")
            return error_json(mensaje=str(e))
    
