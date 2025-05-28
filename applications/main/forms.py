from core.forms import BaseForm, ModelBaseForm
from tinymce.widgets import TinyMCE
from django import forms
from dal import autocomplete, forward

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 200,
    "menubar": False,
    "plugins": "preview,advlist,lists,link,charmap,image,media,table,paste,wordcount",
    "external_plugins": {
        "tiny_mce_wiris": 'https://www.wiris.net/demo/plugins/tiny_mce/plugin.min.js',                  
    },
    "toolbar":  "image | "
    "bold italic | alignleft aligncenter "
    "| bullist numlist | "
    "tiny_mce_wiris_formulaEditor tiny_mce_wiris_formulaEditorChemistry "
    "table superscript subscript charmap preview",
    "images_upload_url": "/upload_image/",
    "document_base_url": "https://goeducativa.com/",
    "relative_urls": False,
    "convert_urls": False,
}

class EjemploForm(BaseForm):
    solucion = forms.CharField(widget=TinyMCE(mce_attrs = TINYMCE_DEFAULT_CONFIG), label='Escribe tu Solución')
    nombre = forms.CharField(max_length=50, label='Nombre')


class ProcesoMarcacionForm(BaseForm):
    archivo_usuarios = forms.FileField(
        label='Archivo de Usuarios',
        help_text='Sube un archivo CSV con los usuarios a marcar. El archivo debe contener una columna "email" con los correos electrónicos de los usuarios.',
        widget=forms.ClearableFileInput(attrs={'accept': '.dat'}),
    )
    archivo_marcaciones = forms.FileField(
        label='Archivo de Marcaciones',
        help_text='Sube un archivo CSV con las marcaciones. El archivo debe contener una columna "email" con los correos electrónicos de los usuarios y una columna "fecha" con la fecha de la marcación.',
        widget=forms.ClearableFileInput(attrs={'accept': '.dat'}),
    )
    fecha_inicio = forms.DateField(
        label='Fecha de Inicio',
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Selecciona la fecha de inicio para las marcaciones.',
    )
    fecha_fin = forms.DateField(
        label='Fecha de Fin',
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Selecciona la fecha de fin para las marcaciones.',
    )