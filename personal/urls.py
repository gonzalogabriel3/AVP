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
    path('index/',index,name="indexPersonal"),

    path('ausReportMensual/$',ausReportMensual,name="ausReportMensual"),
    path('ausReportMensualCMO/$',ausReportMensualCMO),
    path('searchagente/(-?\d{1})/$', searchagente),
    path('partediario/',partediario,name="partediario"),
    
    path('ausReportDir$',ausReportDir,name="ausReportDir"),
    path('ausPartDiario/$',ausPartDiario,name="ausPartDiario"),
    #path('forms/traslado.html',traslado),
    path('listado/ausentismos$',ausentismos),
    path('listado/agentesIndex',agentesIndex,name='listado/agentesIndex'),
    path('listado/base_vieja/base_vieja_index$',base_vieja_index,name="listado/base_vieja/base_vieja_index"),
    path('listado/agentes_base_vieja$',agentes_base_vieja,name="listado/agentes_base_vieja"),

    path('listado/agentes$',agentes,name='listado/agentes'),

    path('listado/articulos$',articulosList,name="listado/articulos"),

    path('listado/adscriptos$',adscripList),
    
    path('listado/base_vieja/medicavieja$', medicavieja,name="listado/base_vieja/medicavieja"),
    path('listado/base_vieja/licenciaanualvieja$', licenciaanualvieja,name="listado/base_vieja/licenciaanualvieja"),
    path('listado/base_vieja/juntamedicavieja$', juntamedicavieja,name="listado/base_vieja/juntamedicavieja"),
    
    path('buscadoragenlic$',buscarAgenLic,name="buscadoragenlic"),
    path('cargaausent',buscarAgenAusent,name="cargaausent"),
    path('generarlicencia/todos$',generarLicT,name="generarlicencia/todos"),
    path('generarlicencia/individual$',generarLicI,name="generarlicencia/individual"),
    
    #path('estadisticas/ausentismoEs.html',ausentismoEs),
    path('ausent/$',ausent,name="ausent"),
    path('vacas',vacas,name="vacas"),
    path('ausRep/$',ausRep,name="ausRep"),
    path('ausRepDir/$',ausRepDir,name="ausRepDir"),
    path('ausRepMes/$',ausRepMes,name="ausRepMes"),
    path('ausRepCMO/$',ausRepCMO,name="ausRepCMO"),
    path('ausRepLicGrem/$',ausRepLicGrem,name="ausRepLicGrem"),
    path('presentRep',presentRep,name="presentRep"),
    path('presentReport/$',presentismoReport,name="presentReport"),
    path('cantclase/$',cantClases,name="cantclase"),
    path('cantagrupindex/$',cantagrupindex,name="cantagrupindex"),
    path('cantagrup/$',cantAgrupamiento,name="cantagrup"),
    path('medicasinalta/$',medicasinalta,name="medicasinalta"),
    path('licanualacum$',vacacionesAcum,name="licanualacum"),
    path('registration/logged_out.html$',logout),
    #path('accounts/login/$', django.contrib.auth.views.login, {'template_name': 'personal/registration/login.html'}),
    
    #path('site_media/(?P<path>.*)$','django.views.static.serve',
     #   {'document_root': './media'}),

    #Reportes de licencias acumuladas
    path('repLicenciasAcumuladasPDF$',repLicenciasAcumuladasPDF,name="repLicenciasAcumuladasPDF"),
    path('repLicenciasAcumuladasWord$',repLicenciasAcumuladasWord,name="repLicenciasAcumuladasWord"),
    #Fin reportes de licencias acumuladas
    
    path('forms/menuagente',menuagente,name="forms/menuagente"),
    
#---------------------------------Listado Logs------------------------------

    path('listado/cambios$',cambios,name="listado/cambios"),
    path('listado/cambiosenreg$',cambiosenreg,name="listado/cambiosenreg"),

#---------------------------------Detalles por agente-----------------------    

    
    path('detalle/detallexagente/ausentismo',detAusentismoxagente,name="detalle/detallexagente/ausentismo"),

#---------------------------------Listados por agente-----------------------

    path('listado/listadoxagente/facxagente',familiaresacxagente,name="listado/listadoxagente/facxagente"),
    re_path(r'^listado/listadoxagente/adtxagente/(\d+)/(-?\d+)/$',accdetrabajoxagente,name="listado/listadoxagente/adtxagente"),
    path('listado/listadoxagente/salidaxagente',salidaxagente,name="listado/listadoxagente/salidaxagente"),
    path('listado/listadoxagente/sancionxagente',sancionxagente,name="listado/listadoxagente/sancionxagente"),
    path('listado/listadoxagente/traslado$',trasladoxagente,name="listado/listadoxagente/traslado"),
    path('listado/listadoxagente/seguro/(\d+)/(-?\d+)/$',seguroxagente),
    path('listado/listadoxagente/servprest$',servprestxagente,name="listado/listadoxagente/servprest"),
    #path('listado/listadoxagente/vacacionesxagente/(\d+)/(-?\d+)/$',vacacionesxagente,name="listado/listadoxagente/vacacionesxagente"),
    path('listado/listadoxagente/vacacionesxagente$',vacacionesxagente,name="listado/listadoxagente/vacacionesxagente"),
    path('listado/listadoxagente/estudioscursados$',estudioscursadosxagente,name="listado/listadoxagente/estudioscursados"),
    path('listado/listadoxagente/medica',medicaxagente,name="listado/listadoxagente/medica"),

#---------------------------------Listados por acc de trabajo-----------------------

    path('listado/listadoxaccdt/certificadoxaccdt$',certificadoxaccdt,name="listado/listadoxaccdt/certificadoxaccdt"),


#---------------------------------Listados por asig familiar-----------------------

    path('listado/listadoxaf/escolaridadxaf$',escolaridadxaf,name='listado/listadoxaf/escolaridadxaf'),

#---------------------------------listado por junta medica------------------
    #path('listado/listadoxmedica/juntamedica/(\d+)/(\d+)/(-?\d+)/$',juntamedicaxagente,name="listado/listadoxmedica/juntamedica"),
     path('listado/listadoxmedica/juntamedica$',juntamedicaxagente,name='listado/listadoxmedica/juntamedica'),
#---------------------------------------------------------------------------
    path('listado/altasbajasindex$',listAltasBajasIndex, name='listado/altasbajasindex'),
    path('listado/listaltasbajas/$',listAltasBajas,name="listado/listaltasbajas"),
    #path('listado/listacctrabajo/$',listAccTrabajo),
    #path('listado/traslado/$',trasladolist),
    #path('listado/seguro/$',segurolist),

#---------------------------------Reportes excel------------------------------    
    
    
    #urlpath('export/$', 'export_to_excel', name='export_to_excel'),
    
    
    path('reportes/ausRepMensualCMO_excel/$',ausRepMensualCMO_excel,name="reportes/ausRepMensualCMO_excel"),
    path('reportes/ausRepMensualGrem_excel/$',ausRepMensualGrem_excel,name="reportes/ausRepMensualGrem_excel"),
    path('reportes/ausRepMensual_excel/$',ausRepMensual_excel),
    
    path('reportes/reportelicenciaspendientes/$',ausRepLicenciasPendientes_excel,name="reportes/reportelicenciaspendientes"),
           
    path('reportes/agentes/$',agentes_excel,name="reportes/agentes"),
    path('reportes/ingfechapartdiarioausent_excel/$',ingfechapartdiarioausent_excel,name="reportes/ingfechapartdiarioausent_excel"),
    path('reportes/partdiarioaus_excel/$',partdiarioaus_excel,name="reportes/partdiarioaus_excel"),
    path('reportes/ingopcsalidasanioagente_excel/$',ingopcsalidasanioagente_excel,name="reportes/ingopcsalidasanioagente_excel"),
    path('reportes/salidasanioagente_excel/$',salidasanioagente_excel,name="reportes/salidasanioagente_excel"),
    path('reportes/ingopcsalidasmesagentes_excel/$',ingopcsalidasmesagentes_excel,name="reportes/ingopcsalidasmesagentes_excel"),
    path('reportes/salidasmesagentes_excel/$',salidasmesagentes_excel,name="reportes/salidasmesagentes_excel"),
    
#---------------------------------Plantilla de forms-----------------------
    path('forms/agente',abmAgente,name="forms/agente"),
    path('forms/abmfamiliaresac',abmFamiliresac,name="forms/abmfamiliaresac"),
    path('forms/abmaccdetrabajo$',abmAccdetrabajo,name="forms/abmaccdetrabajo"),
    path('forms/abmsalida',abmSalida,name="forms/abmsalida"),
    path('forms/abmservprest$',abmServicioprestado,name="forms/abmservprest"),
    path('forms/abmlicencia/(\d+)/(\d+)/$',abmLicencia),
    path('forms/abmlicanualagen/(\d+)/(\d+)/$',abmLicenciaanualagente),
    path('forms/abmlicanual$',abmLicenciaanual,name="forms/abmlicanual"),
    path('forms/abmseguro/(\d+)/(\d+)/$',abmSeguro),
    path('forms/abmtraslado$',abmTraslado,name="forms/abmtraslado"),
    path('forms/abmsancion$',abmSancion,name="forms/abmsancion"),
    path('forms/abmarticulos/<int:idarticulo>/$',abmArticulos,name="forms/abmarticulos"),
    path('forms/abmausentismo',abmAusentismo,name="forms/abmausentismo"),
    #path('forms/abmausent',abmAusent),
    path('forms/abmseguro/(\d+)/(\d+)/$', abmSeguro),
    path('forms/abmcertificadoaccdt/(\d+)/(\d+)/(\d+)/$',abmCertificadoaccidente),
    path('forms/abmadscriptos/(\d+)/(\d+)/$',abmAdscriptos),
    path('forms/abmestudioscursados$',abmEstudioscursados,name="forms/abmestudioscursados"),
    path('forms/abmescolaridad/$',abmEscolaridad,name="forms/abmescolaridad"),
    path('forms/abmmedica$',abmMedica,name="forms/abmmedica"),
    path('forms/abmjuntamedica/$',abmJuntaMedica,name="forms/abmjuntamedica"),
    path('forms/abmjuntamedicavieja$', abmJuntaMedicavieja,name="forms/abmjuntamedicavieja"),
    path('forms/abmmedicavieja$', abmMedicavieja,name="forms/abmmedicavieja"),
    path('forms/abmlicenciaanualvieja$', abmLicenciaanualvieja,name="forms/abmlicenciaanualvieja"),
#---------------------------------Plantilla de error-----------------------
    path('error/',error),
#---------------------------------Plantilla de error-----------------------
    path('calif/$',califIndex),

    path('eliminarLicencia$',eliminarLicenciaTomada,name="eliminarLicencia"),

    path('eliminarAusent$',eliminarAusent,name="eliminarAusent"),


    #URL's de ABM  de Feriados
    path('listado/feriados$',feriadosListado,name='listado/feriados'),
    path('altaFeriado$',altaFeriado,name="altaFeriado"),
    path('modificarFeriado$',modificarFeriado,name="modificarFeriado"),
    path('eliminarFeriado',eliminarFeriado,name="eliminarFeriado"),

    #FIN URL's de ABM  de Feriados

    path('eliminarEscolaridad$',eliminarEscolaridad,name="eliminarEscolaridad"),

    path('eliminarSancion$',eliminarSancion,name="eliminarSancion"),

    path('eliminarTraslado$',eliminarTraslado,name="eliminarTraslado"),

    path('eliminarServPrestado$',eliminarServicioPrestado,name="eliminarServPrestado"),

    path('eliminarEstudioCursado$',eliminarEstudioCursado,name="eliminarEstudioCursado"),

    path('PDFausentismo$',PDFausentismo,name="PDFausentismo"),

    path('ausentismoExcel',ausentismoExcel,name="ausentismoExcel"),

    path('salidasAgenteAñoPDF$',salidasAgenteAñoPDF,name="salidasAgenteAñoPDF"),

    path('altasPDF$',altasPDF,name="altasPDF"),

    path('bajasPDF$',bajasPDF,name="bajasPDF"),

    path('altasExcel$',altasExcel,name="altasExcel"),

    path('bajasExcel$',bajasExcel,name="bajasExcel"),

]

