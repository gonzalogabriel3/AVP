# -*- coding: utf-8 -*-
from django.template import RequestContext, Template, Context
from django.template.loader import *
from django.http import HttpResponse
from personal.models import *
from personal.forms import *
from personal.viewsforms import *
from personal.permisos import *

from django.shortcuts import render_to_response

from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse
from django.contrib import auth

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import datetime

@login_required(login_url='/personal/accounts/login')   
def califIndex(peticion):
    user = peticion.user
    return render_to_response('calif/index.html',{'user':user},)
    
def cantSancion(agente):
    return Sancion.objects.filter(idagente=agente).count()

def cantSancionPeriodo(agente,periodo):
    return Sancion.objects.filter(idagente=agente, fecha__year=periodo).count()
    
def cantSancionTipo(agente,periodo,tipo):
    return Sancion.objects.filter(idagente=agente, fecha__year=periodo, tiposancion=tipo).count()