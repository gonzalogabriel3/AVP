#from django.conf.urls import patterns, include, url
#from dajaxice.core import dajaxice_autodiscover
#from django.conf.urls.defaults import *
from django.urls import path,include, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from django.conf.urls import *
from personal.views import *
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
admin.autodiscover()

urlpatterns = [
    path('index/',index),

    path('ausReportMensual/$',ausReportMensual),
    path('ausReportMensualCMO/$',ausReportMensualCMO),
    path('searchagente/(-?\d{1})/$', searchagente),
    path('partediario/',partediario),
    
    path('ausReportDir/(\d{4})/(\d{1,2})/$',ausReportDir),
    path('ausPartDiario/$',ausPartDiario),
    #path('forms/traslado.html',traslado),
    path('listado/ausentismos$',ausentismos),
    path('listado/agentesIndex',agentesIndex,name='listado/agentesIndex'),
    path('listado/base_vieja/base_vieja_index$',base_vieja_index),
    path('listado/agentes_base_vieja$',agentes_base_vieja),

    path('listado/agentes$',agentes,name='listado/agentes'),
    path('listado/articulos$',articulosList),

    path('listado/adscriptos$',adscripList),
    
    path('listado/base_vieja/medicavieja$', medicavieja),
    path('listado/base_vieja/licenciaanualvieja$', licenciaanualvieja),
    path('listado/base_vieja/juntamedicavieja$', juntamedicavieja),
    
    path('buscadoragenlic$',buscarAgenLic),
    path('cargaausent$',buscarAgenAusent,name="cargaausent"),
    path('generarlicencia/todos$',generarLicT),
    path('generarlicencia/individual$',generarLicI),
    
    #path('estadisticas/ausentismoEs.html',ausentismoEs),
    path('ausent/$',ausent),
    path('vacas',vacas,name="vacas"),
    path('ausRep/$',ausRep),
    path('ausRepDir/$',ausRepDir),
    path('ausRepMes/$',ausRepMes),
    path('ausRepCMO/$',ausRepCMO),
    path('presentRep/$',presentRep),
    path('presentReport/$',presentismoReport),
    path('cantclase/$',cantClases),
    path('cantagrupindex/$',cantagrupindex),
    path('cantagrup/$',cantAgrupamiento),
    path('medicasinalta/$',medicasinalta),
    path('licanualacum$',vacacionesAcum,name="licanualacum"),
    path('registration/logged_out.html$',logout),
    #path('accounts/login/$', django.contrib.auth.views.login, {'template_name': 'personal/registration/login.html'}),
    
    #path('site_media/(?P<path>.*)$','django.views.static.serve',
     #   {'document_root': './media'}),

    path('forms/menuagente$',menuagente,name="forms/menuagente"),
    
#---------------------------------Listado Logs------------------------------

    path('listado/cambios$',cambios),
    path('listado/cambiosenreg$',cambiosenreg),

#---------------------------------Detalles por agente-----------------------    

    
    path('detalle/detallexagente/ausentismo',detAusentismoxagente,name="detalle/detallexagente/ausentismo"),

#---------------------------------Listados por agente-----------------------

    path('listado/listadoxagente/facxagente',familiaresacxagente,name="listado/listadoxagente/facxagente"),
    path('listado/listadoxagente/adtxagente$',accdetrabajoxagente,name="listado/listadoxagente/adtxagente"),
    path('listado/listadoxagente/salidaxagente',salidaxagente,name="listado/listadoxagente/salidaxagente"),
    path('listado/listadoxagente/sancionxagente$',sancionxagente,name="listado/listadoxagente/sancionxagente"),
    path('listado/listadoxagente/traslado$',trasladoxagente,name="listado/listadoxagente/traslado"),
    path('listado/listadoxagente/seguro/(\d+)/(-?\d+)/$',seguroxagente),
    path('listado/listadoxagente/servprest$',servprestxagente,name="listado/listadoxagente/servprest"),
    #path('listado/listadoxagente/vacacionesxagente/(\d+)/(-?\d+)/$',vacacionesxagente,name="listado/listadoxagente/vacacionesxagente"),
    path('listado/listadoxagente/vacacionesxagente$',vacacionesxagente),
    path('listado/listadoxagente/estudioscursados$',estudioscursadosxagente,name="listado/listadoxagente/estudioscursados"),
    path('listado/listadoxagente/medica$',medicaxagente,name="listado/listadoxagente/medica"),

#---------------------------------Listados por acc de trabajo-----------------------

    path('listado/listadoxaccdt/certificadoxaccdt$',certificadoxaccdt,name="listado/listadoxaccdt/certificadoxaccdt"),


#---------------------------------Listados por asig familiar-----------------------

    path('listado/listadoxaf/escolaridadxaf$',escolaridadxaf,name='listado/listadoxaf/escolaridadxaf'),

#---------------------------------listado por junta medica------------------
    #path('listado/listadoxmedica/juntamedica/(\d+)/(\d+)/(-?\d+)/$',juntamedicaxagente,name="listado/listadoxmedica/juntamedica"),
     path('listado/listadoxmedica/juntamedica$',juntamedicaxagente,name='listado/listadoxmedica/juntamedica'),
#---------------------------------------------------------------------------
    path('listado/altasbajasindex/$',listAltasBajasIndex),
    path('listado/listaltasbajas/(\d{4})/$',listAltasBajas),
    #path('listado/listacctrabajo/$',listAccTrabajo),
    #path('listado/traslado/$',trasladolist),
    #path('listado/seguro/$',segurolist),

#---------------------------------Reportes excel------------------------------    
    
    
    #urlpath('export/$', 'export_to_excel', name='export_to_excel'),
    
    
    path('reportes/ausRepMensualCMO_excel/$',ausRepMensualCMO_excel),
    path('reportes/ausRepMensual_excel/$',ausRepMensual_excel),
    
    path('reportes/reportelicenciaspendientes/$',ausRepLicenciasPendientes_excel),
           
    path('reportes/agentes/$',agentes_excel),
    path('reportes/ingfechapartdiarioausent_excel/$',ingfechapartdiarioausent_excel),
    path('reportes/partdiarioaus_excel/$',partdiarioaus_excel),
    path('reportes/ingopcsalidasanioagente_excel/$',ingopcsalidasanioagente_excel),
    path('reportes/salidasanioagente_excel/$',salidasanioagente_excel),
    path('reportes/ingopcsalidasmesagentes_excel/$',ingopcsalidasmesagentes_excel),
    path('reportes/salidasmesagentes_excel/$',salidasmesagentes_excel),
    
#---------------------------------Plantilla de forms-----------------------
    path('forms/agente',abmAgente,name="forms/agente"),
    path('forms/abmfamiliaresac',abmFamiliresac),
    path('forms/abmaccdetrabajo$',abmAccdetrabajo,name="forms/abmaccdetrabajo"),
    path('forms/abmsalida',abmSalida),
    path('forms/abmservprest$',abmServicioprestado,name="forms/abmservprest"),
    path('forms/abmlicencia/(\d+)/(\d+)/$',abmLicencia),
    path('forms/abmlicanualagen/(\d+)/(\d+)/$',abmLicenciaanualagente),
    path('forms/abmlicanual$',abmLicenciaanual,name="forms/abmlicanual"),
    path('forms/abmseguro/(\d+)/(\d+)/$',abmSeguro),
    path('forms/abmtraslado$',abmTraslado,name="forms/abmtraslado"),
    path('forms/abmsancion$',abmSancion,name="forms/abmsancion"),
    path('forms/abmarticulos/(\d+)/$',abmArticulos),
    path('forms/abmausentismo',abmAusentismo,name="forms/abmausentismo"),
    #path('forms/abmausent',abmAusent),
    path('forms/abmsancion/(\d+)/(\d+)/$',abmSancion),
    path('forms/abmseguro/(\d+)/(\d+)/$', abmSeguro),
    path('forms/abmcertificadoaccdt/(\d+)/(\d+)/(\d+)/$',abmCertificadoaccidente),
    path('forms/abmadscriptos/(\d+)/(\d+)/$',abmAdscriptos),
    path('forms/abmestudioscursados$',abmEstudioscursados,name="forms/abmestudioscursados"),
    path('forms/abmescolaridad/(\d+)/(\d+)/$',abmEscolaridad),
    path('forms/abmmedica$',abmMedica,name="forms/abmmedica"),
    path('forms/abmjuntamedica/(\d+)/(\d+)/(\d+)/$',abmJuntaMedica),
    path('forms/abmjuntamedicavieja$', abmJuntaMedicavieja),
    path('forms/abmmedicavieja$', abmMedicavieja),
    path('forms/abmlicenciaanualvieja$', abmLicenciaanualvieja),
#---------------------------------Plantilla de error-----------------------
    path('error/',error),
#---------------------------------Plantilla de error-----------------------
    path('calif/$',califIndex),
]

