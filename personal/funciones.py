# -*- coding: utf-8 -*-
from django.template import RequestContext, Template, Context
from django.template.loader import *
from django.http import HttpResponse
from personal.models import *
from personal.forms import *
#====================================================
from django.shortcuts import render_to_response
#===================================================

from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.template.response import TemplateResponse
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Avoid shadowing the login() and logout() views below.
from django import forms
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
#from django.utils.encoding import force_unicode
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import *
import calendar
from personal.funciones import *
from django.db.models import Q

def paginar(objlist,peticion):
    paginator = Paginator(objlist,20)
    
    try:
        page = int(peticion.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        lista = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lista = paginator.page(paginator.num_pages)
    return lista

def getTime():
    """
    Este metodo lo que hace sencillamente es devolver la fecha actual en el formato DD:MM:AAAA HH:MM:SS en formato
    """
    h = datetime.today()
    return h.strftime("%d-%m-%Y %H:%M:%S")


def formatFecha(fecha):
    """
    Este metodo sirve para convertir rapidamente una fecha en formato datetime en una cadena mas legible con el formato
    DD-MM-AAAA
    """
    return fecha.strftime("%d-%m-%Y")
    
def diffFecha(fecha1,fecha2):
    """
    Retorna la cantidad de dias entre dos fechas
    """
    return (fecha1 - fecha2).days

def diasParaFinAnio(fecha,anio):
    """
    Este metodo retorna la cantidad de dias que faltan para fin de año
    """
    return (datetime.date(anio, 12, 31) - fecha).days
    
def fechaIntervalo(fechainicio,fecha,fechafin):
    """
    Retorna si una fecha se encuentra dentro de un intervalo
    """
    return fechainicio <= fecha <= fechafin
    
def diasMes(anio,mes):
    """
    """
    return calendar.monthrange(anio,mes)[1]
#-------------------------------Registro Logs -----------------------------
#--------------------------------------------------------------------------


def modeloLista(modelo):
    """
    Convierte los datos de un modelo dado en una lista bien ordenada
    """
    #modelo=Agente.objects.filter(pk=modelo.pk).values_list()
    w = list(modelo)
    z = list()
    numero = len(w)

    for i in range(0,numero-1):
        #k = (modelo._meta.fields[i],w[i])
        k = (modelo._meta.fields[i])
        z.append(k)

    return z
    

def datosalista(datos):
    """

    """
    lista = []
    try:
        try: 
            a , b = datos.split(",",1)
        except AttributeError:
            return []
    except ValueError:
        return []
    if "'" in a:
        x ,a = a.split("'",1)
        a ,x = a.split("'",1)

    lista.append(a)
    while ',' in b:
        a , b = b.split(",",1)

        if "'" in a:
            x ,a = a.split("'",1)
            a ,x = a.split("'",1)
            lista.append(a)
    l = []
    for f in range(0, (len(lista)-1), 2):
        l.append((lista[f], lista[f+1]))


    return l


def registrar(user, ntabla, tcambio, hora, v_old, v_new):
    """
    Se encarga de cargar una nueva entrada en la tabla Cambios, lo importante en este metodo es que
    v_old es un valor que puede contener ningun valor osea que puede contener el valor None. Esto se debe a que
    en caso de tratarse de una alta en algun ABM de un modelo, no se contara con datos antiguos que registrar, por lo 
    que directamente se registra el dato nuevo. En caso de tratarse de una modificacion se registra el valor antiguo 
    v_old y el nuevo v_new para que quede constancia de que fue lo que se cambio.
    """
    val_old = list()
    val_new = list()
    if v_old != None:
    	for i in range(0,len(v_old)-1):
    	    if v_old[i] != v_new[i]:
    	        data_old = unicode(v_old[i][1])
    	        val_old.append((v_old[i][0], data_old))
    	        data_new = unicode(v_new[i][1])
    	        val_new.append((v_new[i][0],data_new))
    else:
        val_old = v_old
        for i in range(0,len(v_new)-1):
    	    try:
    	        val_new.append((v_new[i][0],str(v_new[i][1])))
    	    except:
    	        val_new.append((v_new[i][0],v_new[i][1]))  
    registro = Cambios()
    #registro.usuario = UserPerso.objects.using('default').get(pk=user.pk)
    registro.usuario = User.objects.using('default').get(pk=user.pk).username
    registro.modelo = ntabla
    registro.tipocambio = tcambio
    if tcambio == "Baja":
        registro.valorold = val_new
        registro.valornew = val_old
    else:
        registro.valorold = val_old
        registro.valornew = val_new
        registro.save()
    return


def analizaFechaRango(fechaini,fecha,fechafin):
    """
    Retorna un valor booleano referente a si se encuentra una fecha entre fechainicio y fechafin de un ausentismo.
    """
    return fechaini <= fecha <= fechafin
    
def analizaLic(agente,fecha):
    """
    Este metodo se encarga de analizar si el agente tiene licencia tomada y ademas si la fecha recibida en tal caso
    se encuentra dentro del rango de duracion de dicha licencia. Se usa en las licencias anuales en viewsforms.py
    """
    la = Licenciaanual.objects.filter(Q(idagente = agente),Q(tipo='LIC'))
    #La licencia puede estar vacia en caso de que el agente no registre pedido de licencia.
    try:
    	for l in la:
    	    fechaini = l.fechadesde #Fecha en que comienza la licencia
    	    fechafin = fechaini + timedelta(days=l.cantdias - 1) #Se calcula cuando finaliza la licencia en funcion a la cantdias
    	    if analizaFechaRango(fechaini, fecha, fechafin): #Se revisa si la fecha se encuentra entre la fecha inicio y fin
                return True
    	return False
    except IndexError:
        return False
      
def analizaLicanio(agente,fecha,anio):
    """
    Este metodo se encarga de analizar si el agente tiene licencia tomada y ademas si la fecha recibida en tal caso
    se encuentra dentro del rango de duracion de dicha licencia. Se usa en las licencias anuales en viewsforms.py
    """
    return getLicEnFecha(agente,fecha).anio == anio


def getLicEnFecha(agente,fecha):
    """
    Este metodo se encarga de retornar una licencia si la fecha dada esta incluida en su intervalo
    """
    la = Licenciaanual.objects.filter(Q(idagente = agente),Q(tipo='LIC'))
    #La licencia puede estar vacia en caso de que el agente no registre pedido de licencia.
    try:
        for l in la:
            fechaini = l.fechadesde #Fecha en que comienza la licencia
            fechafin = fechaini + timedelta(days=l.cantdias) #Se calcula cuando finaliza la licencia en funcion a la cantdias
            if analizaFechaRango(fechaini, fecha, fechafin):
                return l
        return None        
    except IndexError:
        return None
	   
	

def canttotalart(idagente,mes,anio,arti):
    """
    Este metodo cuenta el presentismo de un agente en un periodo de tiempo dado por año y mes. En caso de tomar el valor 0 en el parametro
    mes, se considera que interesa saber el presentismo de todo el año
    """
    canttotal = 0
    
    artitomados = ArtiTomados.objects.filter(idagente__exact = idagente, anio__exact = anio, idarticulo__exact = arti)
    if artitomados == []:
        return canttotal
    
    if mes == 0:
    	for a in artitomados:
    	    canttotal = canttotal + a.diastomados
    else:
        for i in range(0,mes+1):
    	    try:
        		artitomados = ArtiTomados.objects.get(idagente__exact = idagente,mes__exact = i, anio__exact = anio, idarticulo__exact = arti)
        		canttotal = canttotal + artitomados.diastomados
    	    except ArtiTomados.DoesNotExist:
                pass
    return canttotal
    
    

def superamaxausentmes(idagente, ausent, cantbase):
    arti = Articulo.objects.get(pk=ausent.idarticulo.pk)
    diastomados = 0
    try:
        artiTom = ArtiTomados.objects.get(idagente=idagente, idarticulo=ausent.idarticulo.pk, anio=ausent.fechainicio.year,mes=ausent.fechainicio.month)
        diastomados = artiTom.diastomados
    except ArtiTomados.DoesNotExist:
        diastomados = 0  
    
    return (diastomados + (ausent.cantdias - cantbase)) > arti.maxmensual

    
def superamaxausentanio(idagente, ausent, cantbase):
    arti = Articulo.objects.get(pk=ausent.idarticulo.pk)
    diastomados = 0
    artiTom = ArtiTomados.objects.filter(idagente=idagente,idarticulo=ausent.idarticulo,anio=ausent.fechainicio.year)
    if artiTom != []:
        for artit in artiTom:
            diastomados = artit.diastomados + diastomados
    else:
        diastomados = 0
    
    return (diastomados + (ausent.cantdias - cantbase)) > arti.maxanual

    
 