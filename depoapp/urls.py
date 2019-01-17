from django.urls import path,include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from depoapp.views import *

urlpatterns = [
    path('index/',index),
    path('listado/(\w{3,25})',listado),
    path('listado/pdf/(\w{3,25})',listPdf),
    path('lista/Compra/',listaCompra),
    path('lista/Salida/',listaSalida),
    path('lista/Transf/',listaTransf),
    #path('listado/stockactual/$',stockactual),
    #path('listado/stockactualdepo/$',stockactualdepo),
    path('listado/ingstockactual/',ingopcliststockactual),
    path('listado/stockcero/',stockcero),
    path('listado/graficocombustibles/',graficocombustibles),
    path('listado/ingopclistegresos/',ingopclistegresos),
    path('listado/listegresos/',listegresos),
    path('listado/ingopclistingresos/',ingopclistingresos),
    path('listado/listingresos/',listingresos),
    path('listado/ingopccombustibles/',ingopccombustibles),
    path('listado/listcombustibles/',listcombustibles),
    path('combustockindex/',combustockindex),
    path('listado/combustock/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)',combustock),
    #('depos/',depos),
    #('',index),
    #path('accounts/login/$', include('django.contrib.auth.views.login')),
    #path('assets/(?P<path>.*)$','django.views.static.serve',
    #    {'document_root': '/var/www/avp/media'}),
    #path('static/(?P<path>.*)$','django.views.static.serve',
    #    {'document_root': '/var/www/avp/media'}),
    #GENERAR PDF ->
    path('pdfcompra/(\d+)/',pdfcompra),
    path('pdfarticulo/(\d+)/',pdfarticulo),
    path('pdftransferencia/(\d+)/',pdftransferencia),
    path('pdftransferenciaent/(\d+)/(\d+)/',pdftransferenciaent),
    path('pdftransferenciasal/(\d+)/(\d+)/',pdftransferenciasal),
    path('pdfarticulodeposito/(\d+)/(\d+)/',pdfarticulodeposito),
    path('pdfarticulodepositoad/(\d+)/',pdfarticulodepositoad),
    path('pdfdevolucionesdepo/(\d+)/(\d+)/',pdfdevolucionesdepo),
    path('pdfdevoluciones/(\d+)/',pdfdevoluciones),
    path('pdfarticulomovdepo/(\d+)/(\d+)/',pdfarticulomovdepo),
    path('pdfarticulomov/(\d+)/',pdfarticulomov),
    path('pdfsalida/(\d+)/',pdfsalida),
    path('pdfsalidadepo/(\d+)/(\d+)/',pdfsalidadepo),
]
