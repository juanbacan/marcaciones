from django.urls import path

from core.views_admin import ParametrosAppView, NotificacionesCorreoView, \
    NotificacionesPushAppView, UsuariosView, ModulosView, AgrupacionModulosView, GroupsView, NotificacionesAppView

from .views import PanelView

from core.utils import gestionar_modulos

# Definición de las URLs del sistema
sistema_urls = (
    {
        "nombre": "Parámetros del Sitio",
        "url": 'parametros_sitio/',
        "vista": ParametrosAppView.as_view(),
        "namespace": 'admin_parametros_sitio',
    },
    {
        "nombre": "Usuarios",
        "url": 'usuarios/',
        "vista": UsuariosView.as_view(),
        "namespace": 'admin_usuarios',
    },
    {
        "nombre": "Modulos",
        "url": 'modulos/',
        "vista": ModulosView.as_view(),
        "namespace": 'admin_modulos',
    },
    {
        "nombre": "Agrupacion Modulos",
        "url": 'agrupacion-modulos/',
        "vista": AgrupacionModulosView.as_view(),
        "namespace": 'admin_agrupacion_modulos',
    },
    {
        "nombre": "Grupos",
        "url": 'grupos/',
        "vista": GroupsView.as_view(),
        "namespace": 'admin_grupos',
    }
)

notificaciones_urls = (
    {
        "nombre": "Notificaciones App",
        "url": 'notificaciones_app/',
        "vista": NotificacionesAppView.as_view(),
        "namespace": 'admin_notificaciones_app',
    },
    {
        "nombre": "Correo",
        "url": 'correo/',
        "vista": NotificacionesCorreoView.as_view(),
        "namespace": 'admin_correos',
    },
    {
        "nombre": "PushApp",
        "url": 'pushapp/',
        "vista": NotificacionesPushAppView.as_view(),
        "namespace": 'admin_pushapp',
    },
)

urls_sistema = (
    {
        "nombre": "Sistema",
        "url": 'sistema/',
        "sub_urls": sistema_urls,
    },
    {
        "nombre": "Notificaciones",
        "url": 'notificaciones/',
        "sub_urls": notificaciones_urls,
    },
)



urlpatterns = [
    path('', PanelView.as_view(), name='administracion'),
]

# Construcción de urlpatterns
urlpatterns += [
        path(url['url'] + sub_url['url'], sub_url['vista'], name=sub_url['namespace'])
        for url in urls_sistema
        for sub_url in url['sub_urls'] if sub_url['vista']
]


gestionar_modulos(urls_sistema)