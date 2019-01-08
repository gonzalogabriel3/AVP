# -*- coding: utf-8 -*-
from personal.models import *
from django.db.models import base
from django.contrib import admin



class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'personal'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)



class AgenteAdmin(admin.ModelAdmin):
     search_fields = ['nombres']
     

class AusentismoAdmin(admin.ModelAdmin):
	list_display=['fecha','idagente','fecha','tiempolltarde','observaciones']
	ordering = ['-fecha']
	
class AusentAdmin(admin.ModelAdmin):
	list_display=['idagente','fechainicio','cantdias','fechafin','tiempolltarde','observaciones']
	ordering = ['-fechainicio']
	
class LogAdmin(admin.ModelAdmin):
	list_display=['user','change_message','action_time','content_type','object_id','object_repr','action_flag']
	ordering = ['-action_time']
	
class cambiosAdmin(admin.ModelAdmin):
	list_display=['usuario','modelo','tipocambio','horario','valorold','valornew']
	
class ArtiTomadosAdmin(admin.ModelAdmin):
	list_display=['idagente','anio','mes','idarticulo','diastomados']
	
admin.site.register(Agente,AgenteAdmin)
admin.site.register(Inicio)
admin.site.register(Nacionalidad)
admin.site.register(Funcion)
admin.site.register(Clase)
admin.site.register(Direccion)
admin.site.register(Zona)
admin.site.register(Codigopostal)
admin.site.register(Articulo)
admin.site.register(Agrupamiento)
admin.site.register(Tipolesion)
admin.site.register(Accidentetrabajo)
admin.site.register(Certificadoaccidente)
admin.site.register(Adscripcion)
admin.site.register(Vinculo)
admin.site.register(Asignacionfamiliar)
admin.site.register(Traslado)
admin.site.register(Licenciaanualagente)
admin.site.register(Sancion)
admin.site.register(Licenciaanual)
admin.site.register(Ausentismo,AusentismoAdmin)
admin.site.register(Ausent,AusentAdmin)
admin.site.register(Licenciamedica)
admin.site.register(Juntamedica)
admin.site.register(Estudiocursado)
admin.site.register(Servicioprestado)
admin.site.register(Licencia)
admin.site.register(Seguro)
admin.site.register(Salida)
admin.site.register(Medica)
admin.site.register(UserPerso)
admin.site.register(Cambios,cambiosAdmin)
admin.site.register(Log,LogAdmin)
admin.site.register(ArtiTomados,ArtiTomadosAdmin)
admin.site.register(Evaluador)
admin.site.register(Calificacion)
admin.site.register(CargoFuncion)

#othersite = admin.AdminSite('PersonaLO')
#othersite.register(Ausentismo, MultiDBModelAdmin)
