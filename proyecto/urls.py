from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.shortcuts import render

#import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('proyectoApp.urls')),
    path('pasajes/', include('pasajes.urls')),
    path('deposito/', include('depoapp.urls')),
    path('personal/', include('personal.urls')),
    path(r'^select2/', include('django_select2.urls')),
    #Agrego autenticacion de usuarios provista por Django a la app "pasajes"
    path('pasajes/', include('django.contrib.auth.urls')),
    path('', include('django.contrib.auth.urls')),
    
    

]
