from django.contrib import admin

# Register your models here.

from .models import Localidad,Agente,Familiar,Empresa,Pasaje

admin.site.register(Localidad),
admin.site.register(Agente),
admin.site.register(Familiar),
admin.site.register(Empresa),
admin.site.register(Pasaje),
