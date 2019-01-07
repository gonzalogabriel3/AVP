from django.urls import path

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #################INDEX de todo el proyecto#####################
    path('', views.index, name=''),

]

urlpatterns+= staticfiles_urlpatterns()