from django.conf.urls import patterns, include, url
#from dajaxice.core import dajaxice_autodiscover
from personal.views import *
#from django.conf.urls.defaults import *
from django.conf.urls import *

#dajaxice_autodiscover()

urlpatterns = patterns('',

    #(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    (r'^index/',index),
    #(r'^ausReport/(\d{4})/$',ausReport),

    (r'^ausReportMensual/$',ausReportMensual),
    (r'^ausReportMensualCMO/$',ausReportMensualCMO),
    (r'^searchagente/(-?\d{1})/$', searchagente),
    (r'^partediario/$',partediario),
    
    (r'^ausReportDir/(\d{4})/(\d{1,2})/$',ausReportDir),
    (r'^ausPartDiario/$',ausPartDiario),
    #(r'^forms/traslado.html',traslado),
    (r'^listado/ausentismos$',ausentismos),
    (r'^listado/agentesIndex$',agentesIndex),
    (r'^listado/base_vieja/base_vieja_index$',base_vieja_index),
    (r'^listado/agentes_base_vieja$',agentes_base_vieja),

    (r'^listado/agentes$',agentes),
    (r'^listado/articulos$',articulosList),

    (r'^listado/adscriptos$',adscripList),
    
    (r'^listado/base_vieja/medicavieja$', medicavieja),
    (r'^listado/base_vieja/licenciaanualvieja$', licenciaanualvieja),
    (r'^listado/base_vieja/juntamedicavieja$', juntamedicavieja),
    
    (r'^buscadoragenlic$',buscarAgenLic),
    (r'^cargaausent$',buscarAgenAusent),
    (r'^generarlicencia/todos$',generarLicT),
    (r'^generarlicencia/individual$',generarLicI),
    
    #(r'^estadisticas/ausentismoEs.html',ausentismoEs),
    (r'^ausent/$',ausent),
    (r'^vacas$',vacas),
    (r'^ausRep/$',ausRep),
    (r'^ausRepDir/$',ausRepDir),
    (r'^ausRepMes/$',ausRepMes),
    (r'^ausRepCMO/$',ausRepCMO),
    (r'^presentRep/$',presentRep),
    (r'^presentReport/$',presentismoReport),
    (r'^cantclase/$',cantClases),
    (r'^cantagrupindex/$',cantagrupindex),
    (r'^cantagrup/$',cantAgrupamiento),
    (r'^medicasinalta/$',medicasinalta),
    (r'^licanualacum/(\d{1,5})/$',vacacionesAcum),
    (r'^registration/logged_out.html$',logout),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'personal/registration/login.html'}),
    
    (r'^site_media/(?P<path>.*)$','django.views.static.serve',
        {'document_root': './media'}),

    (r'^forms/menuagente$',menuagente),
    
#---------------------------------Listado Logs------------------------------

    (r'^listado/cambios$',cambios),
    (r'^listado/cambiosenreg$',cambiosenreg),

#---------------------------------Detalles por agente-----------------------    

    (r'^detalle/detallexagente/ausentismo',detAusentismoxagente),

#---------------------------------Listados por agente-----------------------

    (r'^listado/listadoxagente/facxagente',familiaresacxagente),
    (r'^listado/listadoxagente/adtxagente/(\d+)/(-?\d+)/$',accdetrabajoxagente),
    (r'^listado/listadoxagente/salidaxagente',salidaxagente),
    (r'^listado/listadoxagente/sancionxagente/(\d+)/(-?\d+)/$',sancionxagente),
    (r'^listado/listadoxagente/traslado/(\d+)/(-?\d+)/$',trasladoxagente),
    (r'^listado/listadoxagente/seguro/(\d+)/(-?\d+)/$',seguroxagente),
    (r'^listado/listadoxagente/servprest/(\d+)/(-?\d+)/$',servprestxagente),
    (r'^listado/listadoxagente/vacacionesxagente/(\d+)/(-?\d+)/$',vacacionesxagente),
    (r'^listado/listadoxagente/estudioscursados/(\d+)/(-?\d+)/$',estudioscursadosxagente),
    (r'^listado/listadoxagente/medica$',medicaxagente),

#---------------------------------Listados por acc de trabajo-----------------------

    (r'^listado/listadoxaccdt/certificadoxaccdt/(\d+)/(\d+)/(-?\d+)/$',certificadoxaccdt),


#---------------------------------Listados por asig familiar-----------------------

    (r'^listado/listadoxaf/escolaridadxaf$',escolaridadxaf),

#---------------------------------listado por jutna medica------------------
    (r'^listado/listadoxmedica/juntamedica/(\d+)/(\d+)/(-?\d+)/$',juntamedicaxagente),

#---------------------------------------------------------------------------
    (r'^listado/altasbajasindex/$',listAltasBajasIndex),
    (r'^listado/listaltasbajas/(\d{4})/$',listAltasBajas),
    #(r'^listado/listacctrabajo/$',listAccTrabajo),
    #(r'^listado/traslado/$',trasladolist),
    #(r'^listado/seguro/$',segurolist),

#---------------------------------Reportes excel------------------------------    
    
    
    #url(r'^export/$', 'export_to_excel', name='export_to_excel'),
    
    
    (r'^reportes/ausRepMensualCMO_excel/$',ausRepMensualCMO_excel),
    (r'^reportes/ausRepMensual_excel/$',ausRepMensual_excel),
    
    (r'^reportes/reportelicenciaspendientes/$',ausRepLicenciasPendientes_excel),
           
    (r'^reportes/agentes/$',agentes_excel),
    (r'^reportes/ingfechapartdiarioausent_excel/$',ingfechapartdiarioausent_excel),
    (r'^reportes/partdiarioaus_excel/$',partdiarioaus_excel),
    (r'^reportes/ingopcsalidasanioagente_excel/$',ingopcsalidasanioagente_excel),
    (r'^reportes/salidasanioagente_excel/$',salidasanioagente_excel),
    (r'^reportes/ingopcsalidasmesagentes_excel/$',ingopcsalidasmesagentes_excel),
    (r'^reportes/salidasmesagentes_excel/$',salidasmesagentes_excel),
    
#---------------------------------Plantilla de forms-----------------------
    (r'^forms/agente',abmAgente),
    (r'^forms/abmfamiliaresac',abmFamiliresac),
    (r'^forms/abmaccdetrabajo/(\d+)/(\d+)/$',abmAccdetrabajo),
    (r'^forms/abmsalida',abmSalida),
    (r'^forms/abmservprest/(\d+)/(\d+)/$',abmServicioprestado),
    (r'^forms/abmlicencia/(\d+)/(\d+)/$',abmLicencia),
    (r'^forms/abmlicanualagen/(\d+)/(\d+)/$',abmLicenciaanualagente),
    (r'^forms/abmlicanual/(\d+)/(\d+)/(\d*)$',abmLicenciaanual),
    (r'^forms/abmseguro/(\d+)/(\d+)/$',abmSeguro),
    (r'^forms/abmtraslado/(\d+)/(\d+)/$',abmTraslado),
    (r'^forms/abmsancion/(\d+)/(\d+)/$',abmSancion),
    (r'^forms/abmarticulos/(\d+)/$',abmArticulos),
    #(r'^forms/abmausentismo',abmAusentismo),
    (r'^forms/abmausent',abmAusent),
    (r'^forms/abmsancion/(\d+)/(\d+)/$',abmSancion),
    (r'^forms/abmseguro/(\d+)/(\d+)/$', abmSeguro),
    (r'^forms/abmcertificadoaccdt/(\d+)/(\d+)/(\d+)/$',abmCertificadoaccidente),
    (r'^forms/abmadscriptos/(\d+)/(\d+)/$',abmAdscriptos),
    (r'^forms/abmestudioscursados/(\d+)/(\d+)/$',abmEstudioscursados),
    (r'^forms/abmescolaridad/(\d+)/(\d+)/$',abmEscolaridad),
    (r'^forms/abmmedica$',abmMedica),
    (r'^forms/abmjuntamedica/(\d+)/(\d+)/(\d+)/$',abmJuntaMedica),
    (r'^forms/abmjuntamedicavieja$', abmJuntaMedicavieja),
    (r'^forms/abmmedicavieja$', abmMedicavieja),
    (r'^forms/abmlicenciaanualvieja$', abmLicenciaanualvieja),
#---------------------------------Plantilla de error-----------------------
    (r'^error/',error),
#---------------------------------Plantilla de error-----------------------
    (r'^calif/$',califIndex),
)

