

from core.forms import BaseForm
from django import forms


class EditUsuarioForm(BaseForm):
    username = forms.CharField(max_length=100, label='Nombre de usuario')
    nombres = forms.CharField(max_length=100, label='Nombres')
    apellidos = forms.CharField(max_length=100, label='Apellidos')
    cedula = forms.CharField(max_length=10, label='Cédula o Pasaporte')
    email = forms.CharField(max_length=100, label='Dirección de correo electrónico')


class FormularioUsuario(BaseForm):
    username = forms.CharField(max_length=100, label='Nombre de usuario', widget=forms.TextInput(attrs={'labelwidth': 12, 'disabled': True}))
    nombres = forms.CharField(max_length=100, label='Nombres', widget=forms.TextInput(attrs={'labelwidth': 12, 'disabled': True}))
    apellidos = forms.CharField(max_length=100, label='Apellidos', widget=forms.TextInput(attrs={'labelwidth': 12, 'disabled': True}))
    nombre_visible = forms.CharField(max_length=100, label='Nombre visible', widget=forms.TextInput(attrs={'labelwidth': 12, 'disabled': True}))
    email = forms.CharField(max_length=100, label='Dirección de correo electrónico', widget=forms.TextInput(attrs={'labelwidth': 12, 'disabled': True}))
