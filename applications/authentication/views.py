from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.core.paginator import Paginator

from core.models import CustomUser, NotificacionUsuario
from core.utils import get_query_params, get_url_params, save_error, error_json, success_json

from.forms import EditUsuarioForm, FormularioUsuario



class NotificacionesView(LoginRequiredMixin, ListView):
    template_name = 'authentication/notificaciones/notificaciones.html'
    context_object_name = 'notificaciones'
    paginate_by = 20
    page_kwarg = 'pagina'
    model = NotificacionUsuario

    def get_queryset(self):
        usuario = self.request.user
        return NotificacionUsuario.objects.filter(usuario_notificado=usuario).order_by('-id')
    


class MyUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            action, data = get_query_params(request)
            context = {}
            if action:  
                context['action'] = action  

                if action == 'edit_perfil':
                    context['title'] = "Editar perfil"
                    context['action'] = "edit_perfil"
                    context["form"] = EditUsuarioForm(initial={
                        "username": request.user.username,
                        "nombres": request.user.first_name,
                        "apellidos": request.user.last_name,
                        "email": request.user.email,
                    })
                    return render(request, 'authentication/usuarios/edit_perfil.html', context)

            else:
                usuario = request.user

                tp = 'perfil'
                if 'tp' in request.GET:
                    tp = request.GET['tp']
                context["tp"] = tp

                if tp == 'perfil': # Perfil de usuario
                    context["form"] = FormularioUsuario(initial={
                        "username": request.user.username,
                        "nombres": request.user.first_name,
                        "apellidos": request.user.last_name,
                        "nombre_visible": request.user.get_nombre_completo,
                        "email": request.user.email,
                    })

                    return render(request, 'authentication/usuarios/usuario_perfil.html', context)
              
                        
        except Exception as ex:
            print(ex)
            save_error(request, ex, "MY_USER_VIEW GET")
            return error_json(error=ex)

    def post(self, request, *args, **kwargs):
        try:
            action, data = get_query_params(request)
            user = request.user
            context = {}
            context['action'] = action

            if not action:
                return error_json(mensaje="No se ha enviado el parametro action")
            
            if action == 'edit_perfil':
                form = EditUsuarioForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    email = form.cleaned_data['email']
                    if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
                        return error_json(mensaje="El nombre de usuario ya existe")
                    
                    if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
                        return error_json(mensaje="El correo electrónico ya existe")

                    user.username = form.cleaned_data['username']
                    user.first_name = form.cleaned_data['nombres']
                    user.last_name = form.cleaned_data['apellidos']
                    user.email = form.cleaned_data['email']
                    user.save()

                    if 'imagen' in request.FILES:
                        imagen = request.FILES['imagen']
                        user.imagen = imagen
                        user.save()
                    else:
                        user.imagen = None
                        user.save()

                    if 'fondo_horizontal' in request.FILES:
                        fondo_horizontal = request.FILES['fondo_horizontal']
                        perfil = user.mi_perfil_profesor()
                        perfil.fondo_horizontal = fondo_horizontal
                        perfil.save()
                    else:
                        perfil = user.mi_perfil_profesor()
                        perfil.fondo_horizontal = None
                        perfil.save()

                    if 'fondo_cuadrado' in request.FILES:
                        fondo_cuadrado = request.FILES['fondo_cuadrado']
                        perfil = user.mi_perfil_profesor()
                        perfil.fondo_cuadrado = fondo_cuadrado
                        perfil.save()
                    else:
                        perfil = user.mi_perfil_profesor()
                        perfil.fondo_cuadrado = None
                        perfil.save()

                    url = reverse_lazy('authentication:my_usuario') + "?tp=perfil"
                    return success_json(mensaje="Perfil actualizado", url=url)
                else:
                    return error_json(mensaje="Error al actualizar el perfil")


        except Exception as ex:
            print(ex)
            save_error(request, ex, "MY_USER_VIEW POST")
            return error_json(mensaje=str(ex))
