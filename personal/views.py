# -*- coding: utf-8 -*-
#from django.utils import simplejson
#from dajaxice.decorators import dajaxice_register
from django.shortcuts import render
from django.template import RequestContext, Template, Context
from django.template.loader import *
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from personal.models import *
from personal.forms import *
from django.shortcuts import get_object_or_404
#====================================================
from django.shortcuts import render_to_response
#===================================================
###
from urllib.parse import urljoin
import sys
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
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime  import *

from personal.permisos import *
import psycopg2
#import pg
from django.db.models import Q
#------------------Extenciones VIEW-------------------
from personal.viewslistados import *

from personal.viewsreportes import *

from personal.viewsforms import *

from personal.viewscalif import *
import datetime
import calendar

from pprint import pprint

'''def get_grupos(user):
    l = ""
    for g in user.groups.all():
        l = l + g.name
    return l '''

def searchagente(request,opc):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        if int(opc) == 9:
            aux = Agente.objects.all().order_by('apellido')
        else:
            aux = Agente.objects.filter(situacion=opc).order_by('apellido')
            agentes = aux.filter(nombres__icontains=q) | aux.filter(apellido__icontains=q)
            return render_to_response('personal/search_results_agentes.html',
                {'agentes': agentes, 'query': q,'opc':opc})
    else:
        return HttpResponse('Por favor ingrese un termino de busqueda.')



def logged_out(peticion):
  
    user = peticion.user
    return render_to_response('/registration/logged_out.html',{'user':user,},)
    
def logout(request, next_page=None,
           template_name='personal/registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if redirect_to:
        netloc = urlparse.urlparse(redirect_to)[1]
        # Security check -- don't allow redirection to a different host.
        if not (netloc and netloc != request.get_host()):
            return HttpResponseRedirect(redirect_to)

    if next_page is None:
        current_site = get_current_site(request)
        context = {
            'site': current_site,
            'site_name': current_site.name,
            'title': _('Logged out')
        }
        if extra_context is not None:
            context.update(extra_context)
        return TemplateResponse(request, template_name, context,
                                current_app=current_app)
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)

#--------------------------------------------------------------------------
#sudo apt-get install python-pygresql
def conexion():
    #Genero la conexion a la base de datos personal,y retorno esa conexion
    cnx = psycopg2.connect(host='172.155.0.8',dbname='personal',user='postgres',password='sistemasavp',port=5432)
    
    return cnx

def generarLicencia(idagente):
    #Obtengo una conexion a la base de datos
    base = conexion()
    fecha = datetime.datetime.now()
    #Escribo la consulta,que llama a una funcion de la base de datos
    func = 'SELECT dlicanualoptimizado('+str(idagente)+');'
    
    #Creo el cursor para ejecutar la consulta escrita anteriormente
    cursor=base.cursor()
    #Ejecuto la consulta sql
    cursor.execute(func)
    
    #Persisto los datos en la DB
    base.commit()

    #Cierro conexion 
    cursor.close()
    base.close()
    return


def generarLicenciaAgentesActivos():
    base = conexion()
    #rta = base.query("SELECT dlicanualagentes();")
    rta = base.query("SELECT dlicanualagentesnueva();")
    print(rta)
    base.close()
    return

@csrf_exempt
@login_required(login_url='login')
def ausRep(peticion):
    user = peticion.user
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')

    return render_to_response('appPersonal/ausRep.html',{'user':user,'grupos':get_grupos(user)},)
    
@login_required(login_url='/appPersonal/accounts/login')    
def generarLicT(peticion):
    user = peticion.user
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    generarLicenciaAgentesActivos()

    return render_to_response('appPersonal/licenciagenerada.html',{'user':user,'grupos':get_grupos(user)},)

def generarLicI(peticion):
    user = peticion.user
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    idagente = int(peticion.GET.get('idagente'))
    generarLicencia(int(idagente))

    return render_to_response('appPersonal/licenciagenerada.html',{'user':user,},)
    
@csrf_exempt
@login_required(login_url='login')
def ausRepDir(peticion):
    user = peticion.user
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    dire = Direccion.objects.all()
    return render_to_response('appPersonal/ausRepDir.html',{'user':user,'dire':dire,'grupos':get_grupos(user)},)

    
@csrf_exempt
@login_required(login_url='login')
def ausRepMes(peticion):
    user = peticion.user
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    return render_to_response('appPersonal/ausRepMensual.html',{'user':user,'grupos':get_grupos(user)},)


@csrf_exempt
@login_required(login_url='login')
def ausRepCMO(peticion):
    user = peticion.user
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    return render_to_response('appPersonal/ausRepMensualCMO.html',{'user':user,'grupos':get_grupos(user)},)

@csrf_exempt
@login_required(login_url='login')
def presentRep(peticion):
    user = peticion.user
    if permisoEstadistica(user):
        return HttpResponseRedirect('/personal/error/')
    return render_to_response('appPersonal/presentismo.html',{'user':user,'grupos':get_grupos(user)},)
   
@login_required(login_url='/appPersonal/accounts/login')   
def cantClases(peticion):
    user = peticion.user
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    grupos = get_grupos(user)
    cla = Clase.objects.all().order_by('idclase')
    age = Agente.objects.all().filter(situacion=2)
    lis = list()
    for c in cla:
        lis.append([c,0])
    
    for a in age:
        for i in range(0,len(lis)):
            try:
                if a.clase.pk == lis[i][0].idclase:
                    lis[i][1] = lis[i][1] + 1
            except AttributeError:
                pass
    return render_to_response('appPersonal/cantclase.html',{'lista':lis,'user':user,'grupos':grupos},)

@login_required(login_url='login')   
def cantagrupindex(peticion):
    user = peticion.user
    grupos = get_grupos(user)
    agrup = Agrupamiento.objects.all()
    return render_to_response('appPersonal/cantagrupindex.html',{'agrup':agrup,'user':user,'grupos':grupos},)
    
@login_required(login_url='login')   
def cantAgrupamiento(peticion):
    user = peticion.user
    agrup = int(peticion.GET.get('agrup'))
    agrupaux = Agrupamiento.objects.get(pk=int(agrup))
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    grupos = get_grupos(user)
    lista = []
    agent = Agente.objects.filter(agrupamiento=agrup,situacion=2).order_by('apellido')
    cantidad = agent.count()
    for a in agent:
        try:
            zona = Zona.objects.get(descripcion=a.idzona)
        except Exception as e:
            print(e)
        
        lista.append([a.apellido,a.nombres,a.nrodocumento,a.fechaalta,zona.descripcion])
    
    lista = paginar(lista,peticion)
    return render_to_response('appPersonal/cantagrup.html',{'lista':lista,'user':user,'grupos':grupos,'cantidad':cantidad,'agrup':agrup,'descrip':agrupaux.descripcion},)

@login_required(login_url='login')   
def medicasinalta(peticion):
    user = peticion.user
    if permisoEstadistica(user):
        return HttpResponseRedirect('/personal/error/')
    grupos = get_grupos(user)
    lista = []
    medic = Medica.objects.filter(Q(idausent__idarticulo__pk=102)|Q(idausent__idarticulo__pk=1021))
    for m in medic:
        if m.fechaalta == None:
            lista.append([m.agente.apellido,m.agente.nombres,m.diagnostico,m.idausent.fechainicio,m.idausent.fechafin])
    
    lista = paginar(lista,peticion)
    return render_to_response('appPersonal/medicasinalta.html',{'lista':lista,'user':user,'grupos':grupos},)


def partediario(peticion):
    user = peticion.user
    #if permisoEstadistica(user):
     #   return HttpResponseRedirect('/personal/error/')
    dire = Direccion.objects.all()
    return render_to_response('appPersonal/partediario.html',{'user':user,'dire':dire,'grupos':get_grupos(user)},)
    
    

@csrf_exempt
@login_required(login_url='login')
def ausPartDiario(peticion):
    user = peticion.user
    listaagente = list()
    dia = int(peticion.GET.get('dia'))
    mes = int(peticion.GET.get('mes'))
    anio = int(peticion.GET.get('anio'))
    fecha = datetime.date(anio,mes,dia)
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    aus = Ausent.objects.filter(Q(fechainicio__lte=fecha), Q(fechafin__gte=fecha))
    agen = Agente.objects.filter(situacion=2)
    for a in agen:
        listaagente.append(a.idagente)

    listadoAus = listadoPDAusentes(listaagente,aus)
    listadoArti = listadoArticulos(aus)
    cantDiaria = aus.count
    
    return render_to_response('appPersonal/ausParteDiario.html',{'user':user,'listadoArti':listadoArti,'listado':sorted(listadoAus, key=lambda agen: agen[0].apellido),'cant':cantDiaria,'dia':dia,'mes':mes,'anio':anio,'grupos':get_grupos(user)},)
    
    


def fechaEnRango(anio,mes,fi,ff):
    """
    Este metodo en funcion del mes arma una lista con todos los dias del mes, para luego tomar uno a uno cada uno de ellos
    y comprar si se encuentra en el intervalo dado por fechainicio (fi) y fechafin (ff). Utiliza el metodo diasMes tomado de 
    funciones.py. Luego suma la cantidad de insasitencias que ocurrieron en un mes, en caso de no existir retorna 0.
    """
    rango = list()
    cant = 0
    if mes !=0:
        for i in range(1,diasMes(anio,mes)+1):
            rango.append(datetime.date(anio, mes, i))
    #en caso de querer verificar el ausentismo de un año entero, se envia el mes en 0
    else:
        for m in range(1,12+1):
            for dia in range(1,diasMes(anio,m)+1):
                rango.append(datetime.date(anio,m,dia))
    for r in rango:
        if fi <= r <=ff:
            cant = cant+1
    return cant

def ausEnMes(anio,mes,a):
    #HAY QUE ANANALIZAR EL CASO ESPECIAL DE ENERO Y EL CAMBIO DE AÑO
    #fer = Feriado.objects.filter(Q(Fecha__year=anio,Fecha__month=mes))
    #print(a)
    #if a.idagente.idzonareal != None:
    try:
        list_f= feriadosLista(anio,mes,a.idagente.idzonareal.pk)
    #elif a.idagente.idzona != None:
    except a.idagente._meta.model.idzonareal.RelatedObjectDoesNotExist:
        list_f= feriadosLista(anio,mes,a.idagente.idzona.pk)
    #else:
    except a.idagente._meta.model.idzona.RelatedObjectDoesNotExist:
        list_f=[]
    calendar.setfirstweekday(calendar.SUNDAY)
    cal= calendar.monthcalendar(anio,mes)
    finmes= max(cal[len(cal)-1])
    cant=0
    if a.idarticulo.pk==999:
        periodo= Licenciaanual.objects.get(Q(idausent=a.pk,tipo="LIC")).anio
    else:
        periodo=anio
    #SI LOS MESES DE INICIO/FIN SON LOS MISMOS NO HACE FALTA HACER NADA
    #import pdb; pdb.set_trace()
    if (a.fechainicio.month == mes and a.fechafin.month == mes):
        return a.cantdias
    #SI EL AUSENTISMO COMIENZA EN UN MES PERO TERMINA EL MES SIGUIENTE
    elif (a.fechainicio.month == mes and a.fechafin.month > mes):
        dia = a.fechainicio#fecha inicial desde donde contar
        finmes = datetime.date(anio,mes,finmes)
        #RECORRER LAS SEMANAS DEL CALENDARIO
        for sem in cal:
            #SI EL DIA QUE COMIENZA EL AUSENT NO ESTA EN LA SEMANA SIGUE DE LARGO
            if dia.day in sem:
                while dia <= finmes:
                    #Si es L.A.R no debe sumar fines de semana ni feriados
                    if a.idarticulo.pk==999 and periodo>=2016:
                        if dia.day == sem[0]: #DOMINGO
                            pass
                        elif dia.day == sem[6]: #SABADO
                            pass
                        elif dia.day in list_f: #FERIADO
                            pass
                        elif dia.day not in sem:
                            #SI EL INCREMENTO DE LOS DIAS QUEDA FUERA DE LA SEMANA
                            #SE ROMPE EL CICLO PARA CORRERSE A LA SEMANA SIGUIENTE
                            break
                        else:
                            cant += 1
                    else:
                        cant += 1
                    dia = dia + timedelta(days=1)
        return cant
    #DIAS RESTANTES DEL MES SIGUIENTE
    cond1 = a.fechainicio.month < mes and a.fechafin.month == mes
    cond2 = a.fechainicio.month < mes and a.fechafin.month > mes
    if (cond1 or cond2):
    #elif (a.fechainicio.month < mes and a.fechafin.month == mes):
        dia = datetime.date(anio,mes,1) #fecha inicial desde donde contar
        finmes = datetime.date(anio,mes,finmes)
        for sem in cal:
            if a.idarticulo.pk==999 and periodo>=2016:
                while (dia.day <= a.fechafin.day):
                    #Si es L.A.R no debe sumar fines de semana ni feriados
                    if dia.day == sem[0]: #DOMINGO
                        pass
                    elif dia.day == sem[6]: #VIERNES
                        pass
                    elif dia.day in list_f: #FERIADO
                        pass
                    elif dia.day not in sem:
                        #SI EL INCREMENTO DE LOS DIAS QUEDA FUERA DE LA SEMANA
                        #SE ROMPE EL CICLO PARA CORRERSE A LA SEMANA SIGUIENTE
                        break
                    else:
                        cant += 1
                    dia = dia + timedelta(days=1)
            else:
                while (dia <= finmes and dia <= a.fechafin):
                    cant += 1
                    dia = dia + timedelta(days=1)
        return cant
    return 0

@login_required(login_url='login')
def ausReportMensual(peticion):
    """
    Metodo que retorna los ausentes que hubieron en un mes dado. Discriminados en la siguiente forma:
    Agente,Cantidad de faltas, Articulo
    """
    print("AUS REPORT MENSUAL")
    user = peticion.user
    grupos = get_grupos(user)
    cantMensual = 0
    mes = int(peticion.GET.get('mes'))
    anio = int(peticion.GET.get('anio'))
    listaAus = list()
    lista = list()
    agente=Agente()
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    #aus = Ausent.objects.all()
    aus = Ausent.objects.filter(Q(fechainicio__year=anio,fechainicio__month=mes)|Q(fechafin__year=anio,fechafin__month=mes)).order_by('idagente__apellido')
    for a in aus:
        #cant = fechaEnRango(anio,int(mes),a.fechainicio,a.fechafin)
        cant = ausEnMes(anio,mes,a)
        if cant !=0 :
            agente = a.idagente.apellido +' '+ a.idagente.nombres
        if a.idarticulo.pk==3:
            try:
                articulo=a.idarticulo.descripcion+" - "+a.tiempolltarde.strftime("%H:%M:%S")
            except AttributeError:
                articulo=a.idarticulo.descripcion+" "
        else:
            articulo = a.idarticulo.descripcion
        listaAus.append((agente,cant,articulo,a.fechainicio,a.fechafin))
        lista=sorted(listaAus)
    lista = paginar(lista,peticion)
    return render_to_response('appPersonal/ausReportMensual.html',{'user':user, 'grupos':grupos, 'lista':lista,'anio':anio,'mes':mes})

    
@login_required(login_url='/appPersonal/accounts/login')
def ausReportMensualCMO(peticion):
    """
    Metodo que retorna la ocurrencia de CMO en un mes dado. Discriminados en la siguiente forma:
    Agente,Cantidad de faltas, Articulo
    """
    user = peticion.user
    grupos = get_grupos(user)
    cantMensual = 0
    mes = int(peticion.GET.get('mes'))
    anio = int(peticion.GET.get('anio'))
    listaAus = list()
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    aus = Ausent.objects.filter(Q(idarticulo=1011)|Q(idarticulo=1021)|Q(idarticulo=1811))
    for a in aus:
        cant = fechaEnRango(anio,mes,a.fechainicio,a.fechafin)
        if cant !=0:
            agente = a.idagente.apellido +' '+ a.idagente.nombres
        if a.idarticulo.pk==3:
            try:
                articulo=a.idarticulo.descripcion+" - "+a.tiempolltarde.strftime("%H:%M:%S")
            except Exception as e:
                articulo = a.idarticulo.descripcion + " "
        else:
            articulo = a.idarticulo.descripcion
            listaAus.append((agente,cant,articulo,a.fechainicio,a.fechafin))
	    
    lista=sorted(listaAus, key=lambda agen: agen[0])
    lista = paginar(lista,peticion)
    return render_to_response('appPersonal/ausReportMensual.html',{'user':user, 'grupos':grupos, 'lista':lista,'anio':anio,'mes':mes})
    
def procesaPresen(listaPre):
    """
    Este metodo procesa el resultado de la lista de presentismo, en funcion a los articulos y la cantidad de ocurrencias
    de los mismos
    listaPre.append([at.idagente,at.idarticulo,at.diastomados,"",at.tiempolltarde])
    """
    listaNew = list()
    for lis in listaPre:
        agent = lis[0]
        articulo=lis[1] #Objeto articulo
        diasTom=lis[2] #Dias tomados desde principio del año hasta el mes consultado
        tiempoTarde=lis[4] #Tiempo de llegada tarde
        diasMes=lis[5] #Cantidad de dias tomados en el mes
        mesAnte= diasTom - diasMes # La cantidad de dias del mes anterior
	#--------------------------------------------------------------------------------------------------------------
        #articulo 101 -------------------------------------------------------------------------------------------------
        if articulo.idarticulo == 101:
        #if diasTom > 30:
            if mesAnte >= 30:
            #a partir de 30 dias se decuenta el 100% de haberes sumado el 50% de los diez dias anterirores
            #5 = 10/2
            #lis[3] = "Descuenta "+ str(diasTom - 5) + " dias "
                lis[3] = "Descuenta "+str(diasMes) +" dias"
        #elif diasTom > 20:
            elif mesAnte >= 20 and diasTom > 30:
                descuento100 = diasTom - 30
                descuento50 = float((diasMes - descuento100)/2)
                lis[3] = "Descuenta "+str(descuento100+descuento50) +" dias"
            else:
                if mesAnte >= 20:
        		#a partir de 20 dias se descuenta el 50% de haberes
                    lis[3] = "Descuenta "+str((float(diasMes)) / 2) +" dias"
        		#lis[3] = "Descuenta "+str((float(diasTom - 20)) / 2) +" dias"
                else:
                   if diasTom-20 > 0:
        	            lis[3] = "Descuenta "+str((float(diasTom-20)) / 2) +" dias"
    	#--------------------------------------------------------------------------------------------------------------	
    	#articulo 18 --------------------------------------------------------------------------------------------------
        elif articulo.idarticulo == 18:
            if mesAnte >= 12:
    	        lis[3] = "Descuenta "+str(diasMes)+" dias"
            elif mesAnte < 12:
                if diasTom - 12 > 0:
                    lis[3] = "Descuenta "+str(diasTom - 12)+" dias"
    	#--------------------------------------------------------------------------------------------------------------
    	#Inasistencias injustificadas ---------------------------------------------------------------------------------
        elif articulo.idarticulo == 2:
            if diasMes >= 3:
    	        lis[3] = "Descuenta "+ str(diasTom) + " dias y 100%  de presentismo"
            elif diasMes == 2:
    	        lis[3] = "Descuenta 2 dias y 66%  de presentismo"
            elif diasMes == 1:
    	        lis[3] = "Descuenta 1 dias y 33%  de presentismo"
        #-------------------------------------------------------------------------------------------------------------- 
        #LLegadas tarde ------------------------------------------------------------------------------------------------
        elif articulo.idarticulo == 3:
            if diasMes >= 5:
    	        lis[3] = "Descuenta 100% presentismo "
            elif diasMes == 4:
    	        lis[3] = "Descuenta 66% presentismo "
            elif diasMes == 3:
    	        lis[3] = "Descuenta 33% presentismo "
            ausent = Ausent.objects.filter(idagente__pk=agent.pk,fechainicio__year=lis[6],fechainicio__month=lis[7],idarticulo__pk=3)
            acum = 0
            acum2 = time(0,0,0)

            for a in ausent:
                if a.tiempolltarde >= datetime.time(0,50,0):
                    acum = acum + 1
                elif a.tiempolltarde >= datetime.time(0,30,0):
                    acum = acum + 0.5
                else:
                    acum2 = datetime.time(acum2.hour + a.tiempolltarde.hour, acum2.minute + a.tiempolltarde.minute, acum2.second + a.tiempolltarde.second)
                    if acum2 >= datetime.time(0,30,0):
                        acum = acum + 0.5
                        dif = datetime.time(0,30,0)
                        acum2 = datetime.time(acum2.hour - dif.hour, acum2.minute - dif.minute, acum2.second - dif.second)
            if acum > 0:
                #NO HABIA CODIGO!!!!!!!!!!!
                variable=0
            if acum>1:
                lis[3] = lis[3]+" Descuenta " + str(acum) + " dias"
            else:
                lis[3] = lis[3]+" Descuenta " + str(acum) + " dia"
	      
    for l in listaPre:
        if l[3]!= "" :
            listaNew.append(l)
     
    return listaNew
    


@login_required(login_url='login')
def presentismoReport(peticion):
    """
    Metodo que analiza el presentismo de los agentes
    """
    user = peticion.user
    grupos = get_grupos(user)
    month = int(peticion.GET.get('mes'))
    year = int(peticion.GET.get('anio'))
    
    try:
        excel = int(peticion.GET.get('excel'))
    except TypeError:
        excel = 0
      
    
    #agente = Agente.objects.filter(situacion=2)
    #articulo = Articulo.objects.all()
    articulos = [101,1101,18,1811,3,2]
    artitom = ArtiTomados.objects.filter(anio=year, mes__range=(0,month), idarticulo__in = articulos, diastomados__gt=0).order_by('idagente')
    listaPre = list()
    listAux = list()
    
    for at in artitom:
        #Este segmento es a los efectos de unificar los 18 y 101 que tienen doble representacion
        if at.idarticulo.pk == 1101:
            at.idarticulo = Articulo.objects.get(pk=101)
        elif at.idarticulo.pk == 1811:
            at.idarticulo = Articulo.objects.get(pk=18)
        elif at.idarticulo.pk == 3:
            at.diastomados = 0
        #----------------------------------------------------------------------------------------
        
        if (at.idagente,at.idarticulo) not in listAux:
            if at.idarticulo.pk == 3 and at.tiempolltarde == datetime.time(0,0,0):
                pass
            else:
                try:
    	    	    #artitomado = ArtiTomados.objects.filter(idagente=at.idagente,anio=year, mes=month, idarticulo = at.idarticulo)
                    artitomado = ArtiTomados.objects.get(idagente=at.idagente,anio=year, mes=month, idarticulo = at.idarticulo)
                    listaPre.append([at.idagente,at.idarticulo,at.diastomados,"",artitomado.tiempolltarde,artitomado.diastomados,year,month])
                except ArtiTomados.DoesNotExist:
                        pass
                listAux.append((at.idagente,at.idarticulo))
        else:
    	    for l in listaPre:
    	        if (at.idagente.pk == l[0].idagente) and (at.idarticulo.pk==l[1].idarticulo):    
    	            l[2] = l[2] + at.diastomados
    
    listaPre = sorted(listaPre, key=lambda pre:pre[0].apellido)
    listaPre = procesaPresen(listaPre)
    lista = paginar(listaPre,peticion)
    
    if excel == 0:
	       return render_to_response('appPersonal/presentismoReport.html',{'user':user,'grupos':grupos,'lista':lista,'anio':year,'mes':month})
    else:
    	book = xlwt.Workbook(encoding='utf8')
    	
    	sheet = book.add_sheet('Presentismo')
    	
    	default_style = xlwt.Style.default_style
    	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
    	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
    	time_style = xlwt.easyxf(num_format_str='hh:mm:ss')
    			
    	i = 0
    	sheet.write(i, 0, 'Agente', style=default_style)
    	sheet.write(i, 1, 'Artículo', style=default_style)
    	sheet.write(i, 2, 'Cantidad', style=default_style)
    	sheet.write(i, 3, 'Ll.Tarde', style=default_style)
    	sheet.write(i, 4, 'Presentismo', style=default_style)

    for le in listaPre:
        nombres = le[0].nombres
        sincodnombres = nombres#.encode('ascii','ignore')
        apellido = le[0].apellido
        sincodapellido = apellido#.encode('ascii','ignore')
        nombre = str(sincodapellido)+", "+str(sincodnombres)
        i = i + 1
        sheet.write(i, 0, nombre, style=default_style)
        sheet.write(i, 1, le[1].descripcion, style=default_style)
        sheet.write(i, 2, le[2], style=default_style)
        sheet.write(i, 3, le[4], style=time_style)
        sheet.write(i, 4, le[3], style=default_style)

    now = datetime.datetime.now()

    dia = now.day
    mes = now.month
    anio = now.year

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=presentismoReport_'+str(dia)+"-"+str(mes)+"-"+str(anio)+'_excel.xls'
    book.save(response)
    return response
    
    
#--------------------------------------------------------------------------

#@login_required
def listadoPDAusentes(aux,aus):
    listado = list()
    for a in aux:
        agente = Agente.objects.get(idagente=a)
        cantidad = aus.filter(idagente=a).count()
        if cantidad != 0:
    	    arti = aus.filter(idagente=a)[0].idarticulo
    	    listado.append((agente,arti))
    #return sorted(listado, key=lambda faltas: faltas[1], reverse=True)
    return listado

def listadoAusentes(aux,aus):
    """
    Este metodo arma una lista con el formato AGENTE CANT_FALTAS
    Recibe una lista de agentes, y ausentismos.
    El return devuelve la lista ordenada.
    """
    listado = list()
    for a in aux:
        agente = Agente.objects.get(idagente=a)
        #cantidad = aus.filter(idagente=a).count()
        cantidad = 0
        for regaus in aus.filter(idagente=a):
    	    cantidad = cantidad + regaus.cantdias
        if cantidad!=0:
            listado.append((agente,cantidad))

    return sorted(listado, key=lambda faltas: faltas[1], reverse=True)

#calcula el porcentaje de articulos
def porcentajesArti(listadoArt):
    cant = 0
    listaPorc = list()
    for l in listadoArt:
        cant=cant+l[1]
    
    for li in listadoArt:
        li=list(li)
        #n = (li[1]*100.0)/cant
        li[1] = (li[1]*100.0)/cant
        listaPorc.append(li)
    return listaPorc
    
def listadoArticulos(aus):
    """
    Forma una lista que contiene la cantidad de articulos tomados
    """
    artiList = list()
    listadoArt = list()
    arti = Articulo.objects.all()
    
    for a in arti:
        artiList.append(a.idarticulo)
    
    for al in artiList:
        cantidad = 0
        articulo = Articulo.objects.get(idarticulo=al)
        #cantidad = aus.filter(idarticulo=al).count()
        for regaus in aus.filter(idarticulo=al):
            cantidad = cantidad + regaus.cantdias
        if cantidad != 0:
            listadoArt.append((articulo,cantidad))
    
    return porcentajesArti(listadoArt)

@csrf_exempt        
@login_required(login_url='login')
def ausReportDir(peticion):
    a=peticion.GET.get('anio')
    direc=peticion.GET.get('direc')
    user = peticion.user
    grupos = get_grupos(user)
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    cantAnual=0
    try:
        direccion = Direccion.objects.get(pk=direc)
    except Exception as e:
        direccion = None
    
    listaagente = list()
    aus = Ausent.objects.all().filter(Q(fechainicio__year=a) | Q(fechafin__year=a))
    agen = Agente.objects.all().filter(iddireccion=direc)
	
	#En listaagente se guardan los agentes de la direccion
    for a in agen:
        listaagente.append(a.idagente)
	#Sobrescribo ausentismo con los ausentes de la direccion
    aus = aus.filter(idagente__in=listaagente)
    for a in aus:
        cant = fechaEnRango(datetime.date.today().year,0,a.fechainicio,a.fechafin)#el valor 0, es mes en 0 por que me interesa todo el año
        a.cantdias=cant
    listadoAus = listadoAusentes(listaagente,aus)
    listadoArti = listadoArticulos(aus)
    cantMes = ausentDias(aus)
    #cantMes = cantDias(aus)
    ene = cantMes[0][1]
    feb = cantMes[1][1]
    mar = cantMes[2][1]
    abr = cantMes[3][1]
    may = cantMes[4][1]
    jun = cantMes[5][1]
    jul = cantMes[6][1]
    ago = cantMes[7][1]
    sep = cantMes[8][1]
    oct = cantMes[9][1]
    nov = cantMes[10][1]
    dic = cantMes[11][1]
    cantAnual = ene + feb + mar + abr + may + jun + jul + ago + sep + oct + nov + dic

    return render_to_response('appPersonal/ausReportDir.html',{'user':user, 'grupos':grupos, 'listadoArti':listadoArti,'listado':listadoAus,'direccion':direccion.descripcion,'anual':cantAnual,'ene':ene,'feb':feb,'mar':mar,'abr':abr,'may':may,'jun':jun,'jul':jul,'ago':ago,'sep':sep,'oct':oct,'nov':nov,'dic':dic})

#--------------------------------------------------------------------------

#@csrf_exempt
@login_required(login_url='login')
def index(peticion):

    user = peticion.user
    grupos = get_grupos(user)
    inicio = Inicio.objects.get(idinicio=1)
    #titulo = str(i.titulo)
    #mensaje = i.mensaje
    
    return render_to_response('appPersonal/index.html',{'user':user, 'grupos':grupos,'inicio':inicio},)


@login_required(login_url='login')
def agentesIndex(peticion):

    user = peticion.user
    grupos = get_grupos(user)
  
    return render(peticion,'appPersonal/listado/agenteIndex.html',{'user':user,'grupos':grupos},)
    
@login_required(login_url='login')
def base_vieja_index(peticion):

    user = peticion.user
    grupos = get_grupos(user)
    idagente = int(peticion.GET.get('idagente'))
    agente=Agente.objects.get(idagente=idagente)
  
    return render_to_response('appPersonal/listado/base_vieja/base_vieja_index.html',{'agente':agente,'user':user,'grupos':grupos, 'idagente':idagente},)
    
#-----------------------------------------------------------------------------------

#@login_required(login_url='login')
def agentes(peticion):

    user = peticion.user
    grupos = get_grupos(user)
    opc = str(peticion.GET.get('opc'))
    busc = peticion.GET.get('busc')
    rta = permisoAgente(user)
    
    if rta == 'Central' or user.username == "admin":
        agentes = Agente.objects.all().order_by('apellido')
    else:
        agentes = Agente.objects.filter(idzonareal__descripcion=rta).order_by('apellido')
    if busc == None:
        busc = ""
    if int(opc) == 9:
        titulo_form="Todos los agentes"
        if busc == None or busc == "":
            agentes = agentes.order_by('apellido')
        else:
            agentes = agentes.filter(Q(nombres__icontains = busc) | Q(apellido__icontains = busc)| Q(nrodocumento__icontains = busc)| Q(nrolegajo__icontains = busc))
    else:
        if(user.username != "admin"):
            if busc == None or busc == "":
                agentes = agentes.filter(situacion=opc)
            else:
                agentes = agentes.filter(Q(situacion=opc), Q(nombres__icontains = busc) | Q(apellido__icontains = busc)| Q(nrodocumento__icontains = busc)| Q(nrolegajo__icontains = busc))
            
        else:
            if busc == None or busc == "":
                agentes = agentes.filter(situacion=opc).order_by('apellido')
            else:
                agentes = agentes.filter(Q(situacion=opc), Q(nombres__icontains = busc) | Q(apellido__icontains = busc)| Q(nrodocumento__icontains = busc)| Q(nrolegajo__icontains = busc))
        
        if int(opc) == 0:
            titulo_form="Agentes dados de baja"
        elif int(opc) == 1:
            titulo_form="Agentes inactivos"
        elif int(opc) == 2:
            titulo_form="Agentes activos"
        
    #**********************************************************************************
    
    #agentes = agentes.filter(situacion=opc).order_by('apellido')
    paginator = Paginator(agentes,40)
    
    try:
        page = int(peticion.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        lista = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lista = paginator.page(paginator.num_pages)
        
    
    return render(peticion,'appPersonal/listado/agentes.html',{'titulo_form':titulo_form,'lista':lista,'user':user, 'grupos':grupos, 'opc':opc, 'busc':busc},)


#-----------------------------------------------------------------------------------

@login_required(login_url='login')
def vacacionesAcum(peticion):
    idagente=int(peticion.GET.get('idagente'))
    agente=Agente.objects.get(pk=idagente)
    user = peticion.user
    grupos = get_grupos(user)
    if permisoEstadistica(user):
        return HttpResponseRedirect('/appPersonal/error/')
    licaanual = Licenciaanualagente.objects.filter(resta=True, idagente=agente).order_by('idagente')
    listaLic = list()
    for l in licaanual:
        if l.idagente.situacion==2:
            listaLic.append(l)
    
    #lista = sorted(listaLic, key=lambda vac:vac.idagente.apellido)
    lista = paginar(listaLic,peticion)

    return render_to_response('appPersonal/vacaciones.html',{'agente':agente,'user':user,'grupos':grupos,'lista':listaLic},)
    
@csrf_exempt
@login_required(login_url='login')
def vacas(peticion):
    user = peticion.user
    grupos = get_grupos(user)
    idagente = str(peticion.GET.get('idagente'))
    agente = Agente.objects.get(idagente=idagente)
    #iniciar variables
    i = 0
    nofin = True
    vacasaux = []
    #anio_lar  = [' ',' ',' ',' ',' ']
    anio_lar = []
    diastomados = [0,0,0,0,0]
    diaslicencia = [0,0,0,0,0]
    vacas = Licenciaanualagente.objects.filter(idagente__exact=idagente).order_by('anio')
    
    #fitrar vacaciones para mostrar
    vacas = vacas.reverse()
    
    for v in vacas:
        if i <= 4 and v.resta == False and nofin:
            vacasaux.append(v)
            i += 1
            nofin = False

        if i <= 4 and v.resta == True and nofin:
            vacasaux.append(v)
            i += 1
            vacas = vacasaux.reverse()
    #cargar variables
    i = 0
    for v in vacasaux:
        if i <= 4:
            #categorias[i] = str(v.anio)
            anio_lar.append(v.anio)
            diaslicencia[i] = v.cantidaddias
            diastomados[i] = v.diastomados
            i += 1
            nofin = False
	
    
    return render_to_response('appPersonal/licenciavacaciones.html',{'user':user, 'grupos':grupos, 'idagente':idagente,'agente':agente, 'vacas':vacas, 'anio_lar':anio_lar, 'diaslicencia':diaslicencia, 'diastomados':diastomados,},)
 
 
#--------------------------------------------------------------------------




@login_required(login_url='login')
def ausent(peticion):
  
    user = peticion.user
    grupos = get_grupos(user)
    #c={}
    #c.update(csrf(peticion))
    return render_to_response('appPersonal/ausentismo.html',{'user':user, 'grupos':grupos},)
    
    
    
#--------------------------------VIEW ERROR--------------------------------

@login_required(login_url='/appPersonal/accounts/login')
def error(peticion):
  
    user = peticion.user
    grupos = get_grupos(user)
    
    #c={}
    #c.update(csrf(peticion))
    return render_to_response('appPersonal/error.html',{'user':user, 'grupos':grupos},)
  



#---------------------------------------------------------------------------------    
def ausentDias(ausent):
    """
    Calcula la cantidad de inasistencias que ocurrieron en cada mes, a partir de una lista de ausentismo
    """
    print("AUSENT DIAS")
    listM = list()#vector de mes - cantidad de faltas
    for i in range(1,13):
        listM.append([i,0])#la lista interna es [mes-1,cant dias]
    #aca se recorren los ausentismos
    for a in ausent:
        aux = a.fechainicio
        m = aux.month
        anio = aux.year
        listM[m-1][1]=ausEnMes(anio,m,a)
        #if m==a.fechafin.month:
        #    listM[m-1][1]=listM[m-1][1]+a.cantdias
        #else:
        #    while(aux<=a.fechafin):
        #        if aux.month != m:
        #            m = aux.month
        #            listM[m-1][1]=listM[m-1][1]+1
        #            aux = aux + datetime.timedelta(days=1)
        #        if aux.year> anio:
        #            return listM
    return listM

@csrf_exempt
@login_required(login_url='login')
def detAusentismoxagente(peticion):
    user = peticion.user
    borrado = str(peticion.GET.get('borrado'))
    idagen = int(peticion.GET.get('idagente'))
    grupos = get_grupos(user)
    agente = Agente.objects.get(idagente = idagen)
    anio = datetime.date.today().year
    periodo = anio
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('personal/error.html',{'user':user,'error':error,'grupos':get_grupos(user)},)
    if borrado != "":
        try:
            a = Ausent.objects.get(idausent = int(borrado))
            registrar(user,"Ausentismo",'Baja',getTime(),None,modeloLista(Ausent.objects.filter(idausent__exact = int(borrado)).values_list()))
            try:
                acc = Accidentetrabajo.objects.get(idausent = a.pk)
                acc.delete()
            except Accidentetrabajo.DoesNotExist:
                print ("")

                try:
                    a.delete()
                except IntegrityError:
                    error = "Existe 10-2 o accidente de trabajo justificado, verifique antes de eliminar"
                    return render_to_response('appPersonal/error.html',{'user':user,'error':error},)
        except Ausent.DoesNotExist:
            a = None
            mes = date.today().month
            tot55 = canttotalart(idagen,0, anio, 58)
            try:
                men55 = ArtiTomados.objects.get(idagente__exact = idagen, anio__exact = anio, mes__exact = mes, idarticulo__exact=58).diastomados
            except ArtiTomados.DoesNotExist:
                men55 = 0
    tot102 = canttotalart(idagen,0, anio, 102)
    tot101 = canttotalart(idagen,0, anio, 101) + canttotalart(idagen,0, anio, 1011)
    tot18 = canttotalart(idagen,0, anio, 18) + canttotalart(idagen,0, anio, 1811) 
    cantAnual=0
    listaagente = list()
    #Todo el ausentismo en un año dado
    #fechaEnRango(anio,mes,fi,ff):
    #aus = Ausent.objects.all().filter(Q(fechainicio__year=anio, fechafin__year=anio)|Q(fechafin__year=anio))
    #aus = Ausent.objects.filter(Q(idagente__exact=idagen, fechainicio__year=anio)).order_by('-fechainicio')
    aus = Ausent.objects.filter(Q(idagente__exact=idagen,fechainicio__year=anio)|Q(idagente__exact=idagen,fechainicio__year=anio-1,fechafin__year=anio)).order_by('-fechainicio')
    #aus = aus.order_by('-fechainicio')
    agen = Agente.objects.filter(idagente__exact = idagen)
    #En listaagente se guardan los agentes de la direccion
    for a in agen:
      listaagente.append(a.idagente)
    
    #Sobrescribo ausentismo con los ausentes de la direccion
    #aus = aus.filter(idagente__in=listaagente)
    
    listadoAus = listadoAusentes(listaagente,aus)
    listadoArti = listadoArticulos(aus)
    per = []
    cantAnual = 0
    for i in range(0,12):
        per.append(0)
        #cantMes = ausentDias(aus)
    
    #per = ausentDias(aus)
    #cantAnual=10
    #import pdb; pdb.set_trace()
    for a in aus:
        indice = 0
        
        if a.idarticulo.pk ==999:
            periodo= Licenciaanual.objects.get(Q(idausent=a.pk,tipo="LIC")).anio
            
        for i in range(0,12):
            #import pdb; pdb.set_trace()
            if (a.fechainicio.year < a.fechafin.year):
                calendar.setfirstweekday(calendar.SUNDAY)
                cal = calendar.monthcalendar(anio,1)#ENERO de <anio>
                finmes = max(cal[len(cal)-1])
                ausAux = Ausent()
                #print("***caso del año anterior***")
                finOld=datetime.date(anio-1,12,31)#31 de diciembre del <anio> anterior
                c_dias = abs(finOld-a.fechainicio).days#dias corridos desde inicio a fin de <anio>
                dias_dif = cantDias(a.fechainicio,c_dias,a.idagente.pk)# dias habiles hasta fin de anio
                #******************************************************
                try:
                    list_f = feriadosLista(anio,1,a.idagente.idzonareal.pk)
                except:
                    list_f = feriadosLista(anio,1,a.idagente.idzona.pk)
                for j in range (1,5):
                    #print(cal[0][i])
                    if (cal[0][j] != 0) and (cal[0][j] not in list_f): #revisa que sea dia de semana y no sea feriado
                        #import pdb; pdb.set_trace()
                        habil=cal[0][j]#primer dia habil de <anio>
                        break
                inicio = datetime.date(anio,1,habil)#primer dia habil
                c_dias = abs(datetime.date(anio,indice+1,finmes)-inicio).days#cantidad de dias entre fechas

                if (a.idarticulo.pk ==999 and periodo >=2016):
                    #Se sobre escribe por la cantidad de dias habiles
                    c_dias = cantDias(inicio,c_dias,a.idagente.pk)
                ausAux.fechainicio = inicio
                ausAux.fechafin = a.fechafin
                ausAux.cantdias = abs(a.cantdias-dias_dif)
                ausAux.idagente= a.idagente
                ausAux.idarticulo= a.idarticulo
                ausAux.idausent= a.idausent
                per[i] = per[i] + ausEnMes(anio,indice+1,ausAux)
                break
            else:
                print("*** AUSENT CON : "+str(indice+1)+" ***")
                per[i] = per[i] + ausEnMes(anio,indice+1,a)
                #per[i] = per[i] + fechaEnRango(anio,indice+1,a.fechainicio,a.fechafin)
                indice = indice +1
                cantAnual = cantAnual + per[i]
    #cantAnual = ene + feb + mar + abr + may + jun + jul + ago + sep + oct + nov + dic

    return render_to_response('appPersonal/detalle/detallexagente/detausentismoxagente.html',{'agente':agente,'user':user, 'grupos':grupos,'listadoArti':listadoArti,'listado':listadoAus,'anual':cantAnual,'ene':per[0],'feb':per[1],'mar':per[2],'abr':per[3],'may':per[4],'jun':per[5],'jul':per[6],'ago':per[7],'sep':per[8],'oct':per[9],'nov':per[10],'dic':per[11],'aus':aus,'idagen':idagen,'grupos':grupos,'anio':anio, 'tot55':tot55, 'men55':men55, 'tot102':tot102, 'tot101':tot101, 'tot18':tot18})



#------------------------------ BUSCADOR -----------------------------
@login_required(login_url='login')
def buscarAgenAusent(peticion):
    user = peticion.user
    busc = peticion.GET.get('busc')
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    try:
        agentes = Agente.objects.filter( Q(situacion=2), Q(nombres__icontains = busc) | Q(apellido__icontains = busc)| Q(nrodocumento__icontains = busc)| Q(nrolegajo__icontains = busc)).order_by('apellido')
    except:
        agentes = Agente.objects.filter( Q(situacion=2)).order_by('apellido')
    lista = paginar(agentes,peticion)
    
    return render_to_response('appPersonal/buscadoragentes.html',{'lista':lista,'user':user,'grupos':grupos},)


    
@login_required(login_url='login')
def buscarAgenLic(peticion):
    user = peticion.user
    busc = str(peticion.GET.get('busc'))
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    agentes = Agente.objects.filter( Q(situacion=2), Q(nombres__icontains = busc) | Q(apellido__icontains = busc)| Q(nrodocumento__icontains = busc)| Q(nrolegajo__icontains = busc)).order_by('apellido')
    lista = paginar(agentes,peticion)
    return render_to_response('appPersonal/buscadoragenlic.html',{'lista':lista,'user':user,'grupos':grupos},)

    
@login_required(login_url='login')
def agentes_base_vieja(peticion):

    user = peticion.user
    grupos = get_grupos(user)
    busc = str(peticion.GET.get('busc'))
    
    agentes = Agente.objects.all().order_by('apellido')
    
    if busc == "None" or busc == "":
        agentes = agentes.order_by('apellido')
    else:
        agentes = agentes.filter(Q(nombres__icontains = busc) | Q(apellido__icontains = busc)| Q(nrodocumento__icontains = busc)| Q(nrolegajo__icontains = busc))
    
    paginator = Paginator(agentes,40)
    
    try:
        page = int(peticion.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        lista = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lista = paginator.page(paginator.num_pages)
        
    
    return render_to_response('appPersonal/listado/base_vieja/agentes_base_vieja.html',{'lista':lista,'user':user, 'grupos':grupos, 'busc':busc},)


#-----------------------------------------------------------------------------------
