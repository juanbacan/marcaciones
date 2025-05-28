from django.shortcuts import render

from core.views import ViewAdministracionBase
from applications.administracion.forms import *

class PanelView(ViewAdministracionBase):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'administracion/administracion.html', context)

