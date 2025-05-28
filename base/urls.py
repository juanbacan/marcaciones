"""skote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings

from core.views import CustomUserAutocompleteView, ModelAutocompleteView

urlpatterns = [
    path('admin/', admin.site.urls),

    # ***************** Core *****************
    path('', include('core.urls')),
    path('', include('applications.authentication.urls')),

    path('', include('applications.main.urls')),
    path('administracion/', include('applications.administracion.urls')),

    # Allauth
    path('accounts/', include('allauth.urls')),
    # path('ads.txt', AdsView.as_view(), name='ads'),

    # Third Party
    path('tinymce/', include('tinymce.urls')),


    path('model_autocomplete/', ModelAutocompleteView.as_view(), name='model_autocomplete'),
    path('custom_user_autocomplete/', CustomUserAutocompleteView.as_view(), name='custom_user_autocomplete'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [path(r'static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}),
                    path(r'media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}) ]
    

admin.site.site_header = 'Exani'                    # default: "Django Administration"
admin.site.index_title = 'Administración del Sitio'                 # default: "Site administration"
admin.site.site_title = 'Administración del Sitio' # default: "Django site admin"
