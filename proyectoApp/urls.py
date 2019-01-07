from django.urls import path

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    
    #################INDEX'S#####################
    path('', views.index, name='inicio'),

]

urlpatterns+= staticfiles_urlpatterns()