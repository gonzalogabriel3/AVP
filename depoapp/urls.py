from django.conf.urls import patterns, include, url
#
from django.conf.urls import *
from django.contrib.auth.views import login, logout
#
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from depoapp.views import *

urlpatterns = patterns('',
    (r'^listado/(\w{3,25})$',listado),
    (r'^listado/pdf/(\w{3,25})$',listPdf),
    (r'^lista/Compra/',listaCompra),
    (r'^lista/Salida/',listaSalida),
    (r'^lista/Transf/',listaTransf),
    
      
    (r'^listado/stockactual/$',stockactual),
    (r'^listado/stockactualdepo/$',stockactualdepo),
    (r'^listado/ingstockactual/$',ingopcliststockactual),
    (r'^listado/stockcero/',stockcero),
    
    (r'^listado/graficocombustibles/$',graficocombustibles),
    
    (r'^listado/ingopclistegresos/$',ingopclistegresos),
    (r'^listado/listegresos/$',listegresos),
    
    (r'^listado/ingopclistingresos/$',ingopclistingresos),
    (r'^listado/listingresos/$',listingresos),
    
    
    (r'^listado/ingopccombustibles/$',ingopccombustibles),
    (r'^listado/listcombustibles/$',listcombustibles),
    (r'^combustockindex/$',combustockindex),
    (r'^listado/combustock/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)$',combustock),
    
    
    #(r'^depos/',depos),
    #(r'^$',index),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^site_media/(?P<path>.*)$','django.views.static.serve',
        {'document_root': '/var/www/avp/media'}),
    (r'^static/(?P<path>.*)$','django.views.static.serve',
        {'document_root': '/var/www/avp/media'}),

    #GENERAR PDF ->
    (r'^pdfcompra/(\d+)/$',pdfcompra),
    (r'^pdfarticulo/(\d+)/$',pdfarticulo),
    (r'^pdftransferencia/(\d+)/$',pdftransferencia),
    (r'^pdftransferenciaent/(\d+)/(\d+)/$',pdftransferenciaent),
    (r'^pdftransferenciasal/(\d+)/(\d+)/$',pdftransferenciasal),
    (r'^pdfarticulodeposito/(\d+)/(\d+)/$',pdfarticulodeposito),
    (r'^pdfarticulodepositoad/(\d+)/$',pdfarticulodepositoad),
    (r'^pdfdevolucionesdepo/(\d+)/(\d+)/$',pdfdevolucionesdepo),
    (r'^pdfdevoluciones/(\d+)/$',pdfdevoluciones),
    (r'^pdfarticulomovdepo/(\d+)/(\d+)/$',pdfarticulomovdepo),
    (r'^pdfarticulomov/(\d+)/$',pdfarticulomov),
    (r'^pdfsalida/(\d+)/$',pdfsalida),
    (r'^pdfsalidadepo/(\d+)/(\d+)/$',pdfsalidadepo),
)
