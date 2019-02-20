# -*- coding: utf-8 -*-
from django.template import RequestContext, Template, Context
from django.template.loader import *
from django.http import HttpResponse
from personal.models import *
from personal.forms import *
from personal.viewsforms import *
from personal.permisos import *
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
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseRedirect

import datetime



#--------------------------------LISTADO POR AGENTE--------------------------------

@login_required(login_url='login')   
def familiaresacxagente(peticion):
    user = peticion.user

    grupos = get_grupos(user)
    idagente = int(peticion.GET.get('idagente'))
    borrado = int(peticion.GET.get('borrado'))
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
        
    agente = Agente.objects.get(idagente=idagente)
    
    if borrado != "":
        try:
            a = Asignacionfamiliar.objects.get(idasigfam=int(borrado))
            registrar(user,"Asignacion Familiar",'Baja',getTime(),None,modeloLista(Asignacionfamiliar.objects.filter(idasigfam=int(borrado)).values_list()))
            a.delete()
        except Asignacionfamiliar.DoesNotExist:
            a = None
    
    familiares = Asignacionfamiliar.objects.filter(idagente__exact=idagente).order_by('apellidoynombre')
    
    lista = paginar(familiares,peticion)
    
    return render_to_response('appPersonal/listado/listadoxagente/familiaresacxagente.html',{'lista':lista,'user':user,'idagente':idagente,'agente':agente,'grupos':grupos},)

@login_required(login_url='login')   
def accdetrabajoxagente(peticion):
    
    idagente=int(peticion.GET.get('idagente'))
    borrado=int(peticion.GET.get('borrado'))
    user = peticion.user
    
    grupos = get_grupos(user)
    
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error},)
        
    if borrado != "":
        try:
            a = Accidentetrabajo.objects.get(idaccidente=borrado)
            try:
                ausent = Ausent.objects.get(pk = a.idausent_id)
                registrar(user,"Accidente de trabajo",'Baja',getTime(),modeloLista(Accidentetrabajo.objects.get(idaccidente=int(borrado)).values_list()), None)
                a.delete()
                ausent.delete()
            except Ausent.DoesNotExist:
                print ("")
        except Accidentetrabajo.DoesNotExist:
            a = None
    agente = Agente.objects.get(idagente=idagente)
    accidentes = Accidentetrabajo.objects.filter(idagente=idagente).order_by('-fecha')
    
    lista = paginar(accidentes,peticion)
    return render_to_response('appPersonal/listado/listadoxagente/accdetrabajoxagente.html',{'lista':lista,'user':user,'idagente':idagente,'agente':agente,'grupos':grupos},)



@login_required(login_url='login')   
def salidaxagente(peticion):

    user = peticion.user
    idagente = int(peticion.GET.get('idagente'))
    borrado = int(peticion.GET.get('borrado'))
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error},)

    if borrado != "":
        try:
    	    s = Salida.objects.get(idsalida=int(borrado))
    	    registrar(user,"Salida",'Baja',getTime(),modeloLista(Salida.objects.filter(idsalida=int(borrado)).values_list()),None)
    	    s.delete()
        except Salida.DoesNotExist:
            s = None
    agente = Agente.objects.get(idagente=idagente)
    salidas = Salida.objects.filter(idagente__exact=idagente).order_by('-fecha')
        
    lista = paginar(salidas,peticion)
    return render_to_response('appPersonal/listado/listadoxagente/salidaxagente.html',{'lista':lista,'user':user,'idagente':idagente,'agente':agente,'grupos':grupos},)
  

@login_required(login_url='login')
def sancionxagente(peticion):
    idagente=int(peticion.GET.get('idagente'))
    borrado=int(peticion.GET.get('borrado'))
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error},)
    agente = Agente.objects.get(idagente=idagente)
    if borrado != "":
        try:
            s = Sancion.objects.get(idsancion = int(borrado))
            registrar(user,"Sanción",'Baja',getTime(),modeloLista(Sancion.objects.filter(idsancion__exact = int(borrado)).values_list()),None)
            s.delete()
        except Sancion.DoesNotExist:
            s = None
    
    Sancion.objects.filter(fecha=None).delete()
    sanciones = Sancion.objects.filter(idagente=idagente).order_by('fecha')

    lista = paginar(sanciones,peticion)
    return render_to_response('appPersonal/listado/listadoxagente/sancionxagente.html',{'lista':lista,'user':user, 'grupos':grupos, 'idagente':idagente,'agente':agente,},)
    
    
    
#--------------------------------LISTADO POR CERTIFICADO--------------------------------
    
@login_required(login_url='login')   
def certificadoxaccdt(peticion):
    idacc=peticion.GET.get('idacc')
    idagen=peticion.GET.get('idagen')
    borrado=peticion.GET.get('borrado')
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error},)
    if borrado != "":
        try:
            s = Certificadoaccidente.objects.get(idcertif__exact = int(borrado))
            registrar(user,"Certificado de Acc",'Baja',getTime(),modeloLista(Certificadoaccidente.objects.filter(idcertif__exact = int(borrado)).values_list()),None)
            s.delete()
        except Certificadoaccidente.DoesNotExist:
            s = None
            certificados = Certificadoaccidente.objects.filter(idaccidentetrabajo=idacc).order_by('fechadesde')
    lista = paginar(certificados,peticion)
    
    return render_to_response('appPersonal/listado/listadoxaccdt/certificadoxaccdt.html',{'lista':lista,'user':user, 'grupos':grupos, 'idacc':idacc,'idagen':idagen},)
    
#--------------------------------LISTADO POR CERTIFICADO--------------------------------
    
@login_required(login_url='login')   
def escolaridadxaf(peticion):
    user = peticion.user
    idaf = int(peticion.GET.get('idfac'))
    borrado = int(peticion.GET.get('borrado'))
    persona = Asignacionfamiliar.objects.get(idasigfam=idaf)
    idagente = persona.idagente_id
    grupos = get_grupos(user)

    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error},)
    if borrado != "":
        try:
            e = Escolaridad.objects.get(idescolaridad=int(borrado))
            registrar(user,"Escolaridad",'Baja',getTime(),modeloLista(Escolaridad.objects.filter(idescolaridad=int(borrado)).values_list()),None)
            e.delete()
        except Escolaridad.DoesNotExist:
            e = None
        
    escolaridad = Escolaridad.objects.filter(idasigfam__exact=idaf).order_by('anio')

    lista = paginar(escolaridad,peticion)        
        
    return render_to_response('appPersonal/listado/listadoxaf/escolaridadxaf.html',{'lista':lista,'user':user,'idaf':idaf,'persona':persona,'grupos':grupos,'idagente':idagente},)




#---------------------------------------------LISTADO ALTAS BAJAS AGENTES----------------------
@login_required(login_url='login')
def listAltasBajasIndex(peticion):
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = ": No posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
    return render_to_response('appPersonal/listado/altasBajasIndex.html',{'user':user,'grupos':grupos},)

@login_required(login_url='login')
def listAltasBajas(peticion,periodo):
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = ": No posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    agen = Agente.objects.all()
    alta = Agente.objects.filter(fechaalta__year=periodo)
    alta = alta.order_by('apellido')
    baja = Agente.objects.filter(fechabaja__year=periodo)
    baja = baja.order_by('apellido')
    cantAlta = alta.count()
    cantBaja = baja.count()
    cantAgen = agen.filter(situacion=2).count()
    return render_to_response('appPersonal/listado/altasBajas.html',{'alta':alta,'baja':baja,'cantAlta':cantAlta,'cantBaja':cantBaja,'cantAgen':cantAgen,'periodo':periodo,'user':user,'grupos':grupos},)

@login_required(login_url='login')
def listAccTrabajo(peticion):
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error},)
    accidentes = Accidentetrabajo.objects.all().order_by('-fecha')
    lista = paginar(accidentes,peticion)
    
    return render_to_response('appPersonal/listado/acctrabajo.html',{'lista':lista, 'user':user,'grupos':grupos},)

#------------------------------------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def articulosList(peticion):
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error},)
    articulos = Articulo.objects.all()
    
    return render_to_response('appPersonal/listado/articulos.html',{'user':user,'articulos':articulos,'grupos':grupos},)

@login_required(login_url='login')
def adscripList(peticion):
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error},)
    adscriptos = Adscripcion.objects.all()
    
    return render_to_response('appPersonal/listado/adscriptos.html',{'user':user,'adscriptos':adscriptos,'grupos':grupos},)
    
@login_required(login_url='login')
def ausentismos(peticion):
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error},)
    agentes = Agente.objects.order_by('idagente')

    return render_to_response('appPersonal/listado/ausentismo.html',{'user':user, 'grupos':grupos, 'agentes':agentes},)
    
@login_required(login_url='login')
def menuagente(peticion):
  
    user = peticion.user
    idagente = int(peticion.GET.get('idagente'))
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
        
    agente = Agente.objects.get(idagente=idagente)
    
    return render_to_response('appPersonal/menu_agente.html',{'user':user,'idagente':idagente,'agente':agente,'grupos':grupos},)

    
@login_required(login_url='login')   
def agentesIndex(peticion):
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    return render_to_response('appPersonal/listado/agenteIndex.html',{'user':user,'grupos':grupos},)
    
@login_required(login_url='login')   
def agentes(peticion,opc):
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    agentes = Agente.objects.all()
    if int(opc) == 9:
        agentes = agentes.order_by('apellido')
    else:
        agentes = agentes.filter(situacion=opc).order_by('apellido')
    lista = paginar(agentes,peticion)
    return render_to_response('appPersonal/listado/agentes.html',{'lista':lista,'user':user,'opc':opc,'grupos':grupos},)

#-------------------------------------------------------------------------------------------------------------------    

@login_required(login_url='login')
def trasladoxagente(peticion):
    idagente=int(peticion.GET.get('idagente'))
    borrado=int(peticion.GET.get('borrado'))
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos},)

    if borrado != "":
        try:
            t = Traslado.objects.get(idtraslado=int(borrado))
            registrar(user,"Traslado",'Baja',getTime(), None, modeloLista(Traslado.objects.filter(idtraslado=int(borrado)).values_list()))
            t.delete()
        except Traslado.DoesNotExist:
            t = None
    agente = Agente.objects.get(idagente=idagente)
    traslado = Traslado.objects.filter(idagente__exact=idagente).order_by('-fechad')
    lista = paginar(traslado,peticion)
    flag= True
    return render_to_response('appPersonal/listado/traslado.html',{'lista':lista,'user':user,'grupos':grupos,'flag':flag,'idagente':idagente,'agente':agente},)

#-------------------------------------------------------------------------------------------------------------------    

@login_required(login_url='login')
def seguroxagente(peticion,idagente,borrado):
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    if borrado != "":
        try:
            s = Seguro.objects.get(idseguro=int(borrado))
            registrar(user,"Seguro",'Baja',getTime(),modeloLista(s = Seguro.objects.filter(idseguro=int(borrado)).values_list()),None)
            s.delete()
        except Seguro.DoesNotExist:
            s = None
    agente = Agente.objects.get(idagente=idagente)
    seguro = Seguro.objects.filter(idagente__exact=idagente).order_by('idseguro')
    lista = paginar(seguro,peticion)
    flag= True
    return render_to_response('appPersonal/listado/listadoxagente/seguroxagente.html',{'lista':lista,'user':user,'grupos':grupos,'flag':flag,'idagente':idagente,'agente':agente},)

#-------------------------------------------------------------------------------------------------------------------    
@login_required(login_url='login')
def servprestxagente(peticion):
    idagente=int(peticion.GET.get('idagente'))
    borrado=int(peticion.GET.get('borrado'))
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos},)
    if borrado != "":
        try:
            s = Servicioprestado.objects.get(idservprest=int(borrado))
            registrar(user,"Servicio prestado",'Baja',getTime(),modeloLista(Servicioprestado.objects.filter(idservprest=int(borrado)).values_list()),None)
            s.delete()
        except Servicioprestado.DoesNotExist:
            s = None
    agente = Agente.objects.get(idagente=idagente)
    servprest = Servicioprestado.objects.filter(idagente__exact=idagente).order_by('idservprest')
    lista = paginar(servprest,peticion)
    flag= True
    return render_to_response('appPersonal/listado/listadoxagente/servprestxagente.html',{'lista':lista,'user':user,'grupos':grupos,'flag':flag,'idagente':idagente,'agente':agente},)
    
    
#--------------------------------LISTADO DE VACACIONES POR AGENTE--------------------------------
    
@login_required(login_url='login')
@csrf_exempt   
def vacacionesxagente(peticion):
    user = peticion.user
    idagen = int(peticion.GET.get('idagen'))
    borrado = int(peticion.GET.get('borrado'))
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos},)
    if borrado != "":
        try:
          l = Licenciaanual.objects.get(idlicanual__exact = int(borrado))
          registrar(user,"Licencia Vacaciones",'Baja',getTime(),None,modeloLista(Licenciaanual.objects.filter(idlicanual__exact = int(borrado)).values_list()))
          if l.tipo == "INT":
            ausent = Ausent.objects.get(pk=l.idausent.pk)
            la = Licenciaanual.objects.get(idausent=l.idausent,tipo='LIC')
            l.delete()
            ausent.cantdias = la.cantdias
            ausent.save()
          elif l.tipo == "LIC":
            ausent = Ausent.objects.get(pk=l.idausent.pk)
            l.delete()
            ausent.delete()
        except Licenciaanual.DoesNotExist:
            l = None
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos},)
    licencia = Licenciaanual.objects.filter(idagente=idagen).order_by('anio')
    
    lista = paginar(licencia,peticion)
    
    return render_to_response('appPersonal/listado/listadoxagente/vacacionesxagente.html',{'lista':lista,'user':user,'idagente':idagen, 'grupos':grupos},)
    
@login_required(login_url='login')   
def estudioscursadosxagente(peticion):
    idagente=int(peticion.GET.get('idagente'))
    borrado=int(peticion.GET.get('borrado'))
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos},)

    if borrado != "":
        try:
            e = Estudiocursado.objects.get(idestcur=int(borrado))
            registrar(user,"Estudios cursados",'Baja',getTime(),modeloLista(Estudiocursado.objects.filter(idestcur=int(borrado)).values_list()),None)
            e.delete()
        except Estudiocursado.DoesNotExist:
            e = None
    agente = Agente.objects.get(idagente=idagente)
    estudioscursados = Estudiocursado.objects.filter(idagente__exact=idagente)
        
    lista = paginar(estudioscursados,peticion)
    return render_to_response('appPersonal/listado/listadoxagente/estudioscursadosxagente.html',{'lista':lista,'user':user,'idagente':idagente,'agente':agente,'grupos':grupos},)

    
@login_required(login_url='login')   
def medicaxagente(peticion):
    user = peticion.user
    
    idagente = int(peticion.GET.get('idagente'))
    borrado = int(peticion.GET.get('borrado'))
    try:
        idausent = int(peticion.GET.get('idausent'))
    except TypeError:
        idausent = 0
    
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos},)

    if borrado != "":
        try:
            m = Medica.objects.get(id_medica=int(borrado))
            registrar(user,"Medica",'Baja',getTime(),None,modeloLista(Medica.objects.filter(id_medica=int(borrado)).values_list()))
            m.delete()
        except Medica.DoesNotExist:
            m = None
	    
    agente = Agente.objects.get(idagente=idagente)  
    if idausent == 0:
        medica = Medica.objects.filter(agente__exact=idagente)
    else:
        medica = Medica.objects.filter(agente__exact=idagente, idausent__exact = idausent)
        #medica = Medica.objects.filter(agente__exact=idagente,Q(idausent__idarticulo__pk=102)|Q(idausent__idarticulo__pk=1021))
    
    lista = paginar(medica,peticion)
    return render_to_response('appPersonal/listado/listadoxagente/medicaxagente.html',{'lista':lista,'user':user,'idagente':idagente,'agente':agente,'grupos':grupos, 'idausent':idausent},)



@login_required(login_url='login')   
def juntamedicaxagente(peticion):
    idagente=int(peticion.GET.get('idagente'))
    idmedica=int(peticion.GET.get('idmedica'))
    borrado=int(peticion.GET.get('borrado'))
    try:
        idausent = int(peticion.GET.get('idausent'))
    except TypeError:
        idausent = ""
    user = peticion.user
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('personal/error.html',{'user':user,'error':error, 'grupos':grupos},)

    if borrado != "":
        try:
            m = Juntamedica.objects.get(idjuntamedica=int(borrado))
            registrar(user,"Junta Medica",'Baja',getTime(),None,modeloLista(Juntamedica.objects.filter(idjuntamedica=int(borrado)).values_list()))
            m.delete()
        except Juntamedica.DoesNotExist:
            m = None
    juntamedicas = Juntamedica.objects.filter(medica=idmedica)
    agente = Agente.objects.get(idagente=idagente)    
    lista = paginar(juntamedicas,peticion)

    return render_to_response('appPersonal/listado/listadoxmedica/juntamedicaxmedica.html',{'lista':lista,'user':user,'idmedica':idmedica, 'idagente':idagente,'agente':agente,'grupos':grupos, 'idausent':idausent},)

#-------------------------------------------------------------------------------------------------------------------------------------------    

@login_required(login_url='login')   
def cambios(peticion):
    user = peticion.user

    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
        
    cambios = Cambios.objects.all().order_by('-horario')
    
    lista = paginar(cambios,peticion)
    
    return render_to_response('appPersonal/listado/cambios.html',{'lista':lista,'user':user,'grupos':grupos},)
    
def cambiosenreg(peticion):
    user = peticion.user
    camb = int(peticion.GET.get('camb'))
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
        
    cambios = Cambios.objects.get(pk=camb)
    lista = []
    listaold = datosalista(cambios.valorold)
    listanew = datosalista(cambios.valornew)
    if listaold == []:
        for i in range(0,len(listanew)):
            lista.append((listanew[i] , ("","Vacio")))
    elif listanew == []:
        for i in range(0,len(listaold)):
            lista.append((("","Vacio"), listaold[i]))
    else:
        for i in range(0,len(listanew)):
            lista.append((listanew[i] , listaold[i]))
        
    return render_to_response('appPersonal/listado/cambiosenregistros.html',{'lista':lista,'user':user,'grupos':grupos},)



@login_required(login_url='login')   
def medicavieja(peticion):

    user = peticion.user
    idagente = int(peticion.GET.get('idagente'))
    agente = Agente.objects.get(idagente = idagente)
    
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos},)
    
    medicav = Medicavieja.objects.filter(agente__exact = idagente)

    lista = paginar(medicav,peticion)
    return render_to_response('appPersonal/listado/base_vieja/medicavieja.html',{'lista':lista,'user':user,'grupos':grupos, 'idagente':idagente, 'agente':agente},)
    
    
@login_required(login_url='login')   
def licenciaanualvieja(peticion):

    user = peticion.user
    idagente = int(peticion.GET.get('idagente'))
    agente = Agente.objects.get(idagente = idagente)
    
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos},)
    
    licav = Licenciaanualvieja.objects.filter(id_agente__exact = idagente)

    lista = paginar(licav,peticion)
    return render_to_response('appPersonal/listado/base_vieja/licenciaanualvieja.html',{'lista':lista,'user':user,'grupos':grupos,'licav':licav, 'idagente':idagente, 'agente':agente},)
    
    
@login_required(login_url='login')   
def juntamedicavieja(peticion):

    user = peticion.user
    idagente = int(peticion.GET.get('idagente'))
    agente = Agente.objects.get(idagente = idagente)
    
    grupos = get_grupos(user)
    if permisoListado(user):
        error = "no posee permiso para listar"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos},)
    
    juntamedicas = Juntamedicavieja.objects.filter(idagente__exact = idagente)

    lista = paginar(juntamedicas,peticion)
    return render_to_response('appPersonal/listado/base_vieja/juntamedicavieja.html',{'lista':lista,'user':user,'grupos':grupos, 'idagente':idagente, 'agente':agente},)

