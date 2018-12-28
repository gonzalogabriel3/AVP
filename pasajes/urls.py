from django.urls import path

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    
    #################INDEX'S#####################
    path('', views.index, name='index'),
    path('agente', views.indexAgenteView, name='agente'),
    path('localidad', views.indexLocalidadView, name='localidad'),
    path('familiar', views.indexFamiliarView, name='familiar'),
    path('empresa', views.indexEmpresaView, name='empresa'),
    path('pasaje', views.indexPasajeView, name='pasaje'),
    path('pasajero', views.indexPasajeroView, name='pasajero'),

    #################ABM'S#####################

    #**ABM Agente**#
    path('altaAgente', views.altaAgente, name='altaAgente'),
    path('modificacionAgente/<int:idAgente>/', views.modificacionAgente, name='modificacionAgente'),
    path('bajaAgente/<int:idAgente>/', views.bajaAgente, name='bajaAgente'),

    #**ABM Localidad**#
    path('altaLocalidad', views.altaLocalidad, name='altaLocalidad'),
    path('bajaLocalidad/<int:idLocalidad>/', views.bajaLocalidad, name='bajaLocalidad'),
    path('modificacionLocalidad/<int:idLocalidad>/', views.modificacionLocalidad, name='modificacionLocalidad'),

    #**ABM Familiar**#
    path('altaFamiliar', views.altaFamiliar, name='altaFamiliar'),
    path('bajaFamiliar/<int:idFamiliar>/', views.bajaFamiliar, name='bajaFamiliar'),
    path('modificacionFamiliar/<int:idFamiliar>/', views.modificacionFamiliar, name='modificacionFamiliar'),

    #**ABM Empresa**#
    path('altaEmpresa', views.altaEmpresa, name='altaEmpresa'),
    path('bajaEmpresa/<int:idEmpresa>/', views.bajaEmpresa, name='bajaEmpresa'),
    path('modificacionEmpresa/<int:idEmpresa>/', views.modificacionEmpresa, name='modificacionEmpresa'),

    #**ABM Pasaje**#
    path('altaPasaje', views.altaPasaje, name='altaPasaje'),
    path('bajaPasaje/<int:idPasaje>/', views.bajaPasaje, name='bajaPasaje'),
    path('modificacionPasaje/<int:idPasaje>/', views.modificacionPasaje, name='modificacionPasaje'),

    #Url para formulario de un nuevo pasaje
    path('altaPasaje/<int:idPasajero>', views.altaPasaje, name='altaPasaje'),
    #Url para generar el reporte en pdf de un pasaje
    path('reportePasaje/<int:idPasaje>/', views.reportePasaje, name='reportePasaje'),

    #Login
   # path('login',views.loginView,name='login'),

]

urlpatterns+= staticfiles_urlpatterns()