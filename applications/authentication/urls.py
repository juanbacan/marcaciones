from django.urls import path
from .views import *

app_name = 'authentication'

urlpatterns = [
    path('notificaciones/', NotificacionesView.as_view(), name='notificaciones'),
    path('mi_perfil/', MyUserView.as_view(), name='my_usuario'),
    path('usuario/<int:id>/', MyUserView.as_view(), name='usuario'),
]
