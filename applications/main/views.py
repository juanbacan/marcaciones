import datetime

from django.shortcuts import render
from django.views.generic import View

from .forms import ProcesoMarcacionForm
from core.utils import success_json, error_json

from .models import UsuarioAsistencia, RegistroAsistencia
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
    for linea in archivo:
        try:
            partes = linea.decode('utf-8').strip().split('\t')
            if len(partes) >= 6:
                usuario_id = int(partes[0])
                fecha_hora = datetime.datetime.strptime(partes[1], "%Y-%m-%d %H:%M:%S")
                status = int(partes[2])
                verificacion = int(partes[3])
                entrada_salida = int(partes[4])
                extra = int(partes[5])

                usuario = UsuarioAsistencia.objects.filter(usuario_id=usuario_id).first()
                if usuario:
                    RegistroAsistencia.objects.create(
                        usuario=usuario,
                        fecha_hora=fecha_hora,
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
        
        return render(request, 'core/administracion/grupos/lista.html', context)
    
    # def get(self, request, *args, **kwargs):
    #     context = {}
    #     context['form'] = ProcesoMarcacionForm()
    #     return render(request, 'main/home.html', context)
    

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.action and hasattr(self, f'post_{self.action}'):
            return getattr(self, f'post_{self.action}')(request, context, *args, **kwargs)
        return error_json(mensaje="Acción no permitida")
    
    # def post(self, request, *args, **kwargs):
    #     context = {}
    #     form = ProcesoMarcacionForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         archivo_marcaciones = form.cleaned_data['archivo_marcaciones']
    #         for linea in archivo_marcaciones:
    #             partes = linea.decode('utf-8').strip().split('\t')
    #             if len(partes) >= 6:
    #                 usuario_id=int(partes[0]),
    #                 fecha_hora=datetime.datetime.strptime(partes[1], "%Y-%m-%d %H:%M:%S"),
    #                 status=int(partes[2]),
    #                 verificacion=int(partes[3]),
    #                 entrada_salida=int(partes[4]),
    #                 extra=int(partes[5])

    #                 print(f"Usuario ID: {usuario_id}, Fecha y Hora: {fecha_hora}, Status: {status}, Verificación: {verificacion}, Entrada/Salida: {entrada_salida}, Extra: {extra}")
    #             else:
    #                 print("Error en la línea:", linea)
    #                 continue
    #         return success_json(url='/')
    #     else:
    #         print("Error en el formulario:", form.errors)
    #         return error_json(forms=[form])


