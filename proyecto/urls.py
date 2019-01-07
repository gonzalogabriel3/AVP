from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pasajes/', include('pasajes.urls')),
    path('deposito/', include('depoapp.urls')),
    path(r'^select2/', include('django_select2.urls')),
    #Agrego autenticacion de usuarios provista por Django a la app "pasajes"
    path('pasajes/', include('django.contrib.auth.urls')),

    #Url a index del proyecto
    path('inicio/', TemplateView.as_view(template_name='templates/indexProyecto.html'),name='inicio'),

]
