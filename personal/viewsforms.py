# -*- coding: utf-8 -*-
from django.template import RequestContext, Template, Context
from django.template.loader import *
from django.http import HttpResponse
from personal.models import *
from personal.forms import *
from django.shortcuts import render
#====================================================
from django.shortcuts import render_to_response
#===================================================

import math
from urllib.parse import urljoin
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.template.response import TemplateResponse
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.core.cache import cache
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
#from django.debug.toolbar import force_unicode
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import *
from personal.permisos import *
from personal.funciones import *
from personal.viewslistados import *
from pprint import pprint
from django.shortcuts import redirect
from personal.viewslistados import *
from django.core.cache import cache
import json
from django.core import serializers
from django.contrib import messages
#--------------------------------------------------------------------------
#---------------------------------VIEW FORM--------------------------------

def borrarCache():
  cache.delete('forms/abmlicanual')




@csrf_exempt
@login_required(login_url='login')
######NO SE USA,SE UTILIZA EL METODO 'abmAusentismo'##########
def abmAusent(peticion):

    user = peticion.user
    name = 'Ausentismo'
    accion = ''
    form_old = ''
    cantbaseFI = 0
    cantbaseFF = 0
    grupos = get_grupos(user)
    if permisoZona(user) and permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html', {'user': user, 'error': error, 'grupos': grupos},)

    idagen = int(peticion.GET.get('idagente'))
    idausent = int(peticion.GET.get('idausent'))

    code = peticion.GET.get('code')
    if code != None:
    	code = int(peticion.GET.get('code'))
    else:
        code = 0

    if peticion.POST:
      if int(idausent) > 0:
        a = Ausent.objects.get(pk=idausent)
        form_old = formAusent(instance=a)
        # form_old = modeloLista(form_old.instance)
        form_old = modeloLista(form_old.Meta.model.objects.filter(
            pk=form_old.instance.pk).values_list())
        form = formAusent(peticion.POST, instance=a)
        accion = 'Modificacion'
      else:
      	accion = 'Alta'
      	form = formAusent(peticion.POST)

    if form.is_valid():
    # Control cantidad de articulos permitidos
    	fechainicio = form.instance.fechainicio
    	dias = form.instance.cantdias - 1
    	fechafin = fechainicio + timedelta(days=dias)
    if fechainicio.month != fechafin.month:
    	try:
    		ausentenbase = Ausent.objects.get(pk=form.instance.pk)
    		if ausentenbase.fechainicio.month != ausentenbase.fechafin.month:
    			cantbaseFI = ausentenbase.cantdias - ausentenbase.fechafin.day
    			cantbaseFF = ausentenbase.fechafin.day
    		else:
    			cantbaseFI = ausentenbase.cantdias
    	except Ausent.DoesNotExist:
    		cantbaseFI = 0
    		cantbaseFF = 0

    	ausentFI = Ausent()
    	ausentFI.idagente = Agente.objects.get(pk=idagen)
    	ausentFI.idarticulo = form.instance.idarticulo
    	ausentFI.fechainicio = form.instance.fechainicio
    	ausentFI.cantdias = form.instance.cantdias - fechafin.day
    	if superamaxausentmes(idagen, ausentFI, cantbaseFI):
    		# error
    		url = '/personal/detalle/detallexagente/ausentismo?idagente=' + \
    		    str(idagen) + '&borrado=-1'
    		error = ": Supera cantidad de artículos en el mes"
    		return render_to_response('personal/error.html', {'user': user, 'error': error, 'grupos': grupos, 'url': url},)
    		ausentFF = Ausent()
    		ausentFF.idagente = Agente.objects.get(pk=idagen)
    		ausentFF.idarticulo = form.instance.idarticulo
    		ausentFF.cantdias = fechafin.day
    		ausentFF.fechainicio = fechafin

    	if superamaxausentmes(idagen, ausentFF, cantbaseFF):
    		url = '/personal/detalle/detallexagente/ausentismo?idagente=' + \
    		    str(idagen) + '&borrado=-1'
    		error = ": Supera cantidad de artículos en el mes"
    		return render_to_response('personal/error.html', {'user': user, 'error': error, 'grupos': grupos, 'url': url},)
    else:
	    try:
	       ausentenbase = Ausent.objects.get(pk=form.instance.pk)
	       cantbase = ausentenbase.cantdias
	    except Ausent.DoesNotExist:
	       cantbase = 0
	    if superamaxausentmes(idagen, form.instance, cantbase):
	    	# error
	    	url = '/personal/detalle/detallexagente/ausentismo?idagente=' + \
	    	    str(idagen) + '&borrado=-1'
	    	error = ": Supera cantidad de artículos en el mes"
	    	return render_to_response('personal/error.html', {'user': user, 'error': error, 'grupos': grupos, 'url': url},)
	    	try:
	    		ausentenbase = Ausent.objects.get(pk=form.instance.pk)
	    		cantbase = ausentenbase.cantdias
	    	except Ausent.DoesNotExist:
	    		cantbase = 0

	    if superamaxausentanio(idagen, form.instance, cantbase):
	    	url = '/personal/detalle/detallexagente/ausentismo?idagente=' + \
	    	    str(idagen) + '&borrado=-1'
	    	error = ": Supera cantidad de artículos en el año"
	    	return render_to_response('personal/error.html', {'user': user, 'error': error, 'grupos': grupos, 'url': url},)

	    ausen = Ausent.objects.order_by(
	        '-fechainicio').filter(idagente__exact=idagen)
    try:
      for au in ausen:
        if au.idausent != form.instance.idausent:
          if len(ausen) > 0:
            cd = form.instance.cantdias  # Datos del Formulario
            f = form.instance.fechainicio  # Datos del Formulario
            cd1 = au.cantdias  # Datos en la Base
            f1 = au.fechainicio  # Datos en la Base
            if f == f1:
              url = '/personal/detalle/detallexagente/ausentismo?idagente=' +str(idagen) + '&borrado=-1'
              error = ": Redundancia en ausentismo"
              return render_to_response('personal/error.html',{'user':user,'error':error, 'grupos':grupos, 'url':url})
      for i in range(1,cd+1):
        for j in range(1,cd1+1):
          f = form.instance.fechainicio + timedelta(days=i)
          f1 = au.fechainicio + timedelta(days=j)
          if f == f1:
            url = '/personal/detalle/detallexagente/ausentismo?idagente='+str(idagen)+'&borrado=-1'
            error = ": Redundancia en ausentismo"
            return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos,'url':url},)
    except IndexError:
      print ("")

    form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
    form.fields['direccion'].widget.attrs['enabled'] = 'enabled'
    agente = Agente.objects.get(pk = idagen)
    form.instance.idagente = agente
    form.instance.direccion = agente.iddireccion
    form.save()
	
	#------------------------------------------------
        
        # Cargar accidente de trabajo
    if form.instance.idarticulo_id == 111 :
      try:
        acc = Accidentetrabajo.objects.get(idausent = form.instance)
      except Accidentetrabajo.DoesNotExist:
        acc = Accidentetrabajo()
        acc.idagente = agente
        acc.fecha = form.instance.fechainicio
        acc.fechaalta = form.instance.fechainicio + timedelta(days=form.instance.cantdias)
        acc.idausent = form.instance
        acc.save()
	#-----------------------------------------------
    if accion == 'Alta':
      registrar(user,name,'Alta',getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
    elif accion == 'Modificacion':
      registrar(user, name, "Modificacion", getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))

      if code == 2 :
        url = '/personal/cargaausent'
      else:
        url = '/personal/detalle/detallexagente/ausentismo?idagente='+str(idagen)+'&borrado=-1'
        return HttpResponseRedirect(url)
    else:
      if int(idausent) >0 and int(idagen)> 0:
        a = Ausent.objects.get(pk=idausent)
        form = formAusent(instance=a)
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Ausent()
          b.idagente = a
          b.direccion = a.iddireccion	
          form = formAusent(instance=b)
          
      else:
        form = formAusent()
    pag_ausentismo=True
    cache.clear()
    return render_to_response('appPersonal/forms/abm.html',{'pag_ausentismo':pag_ausentismo,'user':user,'form': form, 'name':name, 'grupos':grupos}, )

@csrf_exempt
@login_required(login_url='login')
def abmAusentismo(peticion):
    user = peticion.user
    name = 'Ausentismo'
    grupos = get_grupos(user)
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('personal/error.html',{'user':user,'error':error,'grupos':grupos},)

    idagen = int(peticion.GET.get('idagente'))
    idausent = int(peticion.GET.get('idausent'))
    agente = Agente.objects.get(pk=idagen)
    if peticion.POST:
      if int(idausent) >0:
        a = Ausent.objects.get(pk=idausent)
        form = formAusent(peticion.POST, instance=a)
      else:
        form = formAusent(peticion.POST)
      if form.is_valid():
        cd = form.cleaned_data['cantdias']
        #------------------------------------------------
        
        licencia = Licenciaanual.objects.order_by('-fechadesde').filter(idagente__exact = idagen)
        if len(licencia) > 0:
          cdl = licencia[0].cantdias
          fd = licencia[0].fechadesde
          f = form.instance.fechainicio
          if f == fd:
            error = ": El agente se encuentra de vacaciones"
            return render_to_response('error.html',{'user':user,'error':error, 'grupos':grupos},)
          for i in range(1,cd):
            for j in range(1,cdl):
              f = form.instance.fechainicio + timedelta(days=i)
              fd = licencia[0].fechadesde + timedelta(days=j)
              if f == fd:
                error = ": El agente se encuentra de vacaciones"
                return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos},)
        #------------------------------------------------
        form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
        form.fields['direccion'].widget.attrs['enabled'] = 'enabled'
        agente = Agente.objects.get(pk = idagen)
        form.instance.idagente = agente
        form.instance.direccion = agente.iddireccion
        #form.save()
        
        #for i in range(1,cd):
        a = Ausent()
        a.fechainicio=form.instance.fechainicio
        #a.fechafin = form.instance.fechafin + timedelta(days=form.instance.cantdias)
        #pprint(a.fechafin)
        a.cantdias = form.instance.cantdias
        a.observaciones = form.instance.observaciones
        a.idagente = form.instance.idagente
        a.idarticulo = form.instance.idarticulo
        a.tiempolltarde = form.instance.tiempolltarde
        a.direccion = form.instance.direccion
        a.save()

        url = '/personal/detalle/detallexagente/ausentismo?idagente='+str(idagen)+'&borrado=-1'
        return HttpResponseRedirect(url)
    else:
      if int(idausent) >0 and int(idagen)> 0:
        a = Ausent.objects.get(pk=idausent)
        form = formAusent(instance=a)
        titulo_form="/ Modificar ausentismo"
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Ausent()
          b.idagente = a
          b.direccion = a.iddireccion 
          form = formAusent(instance=b)
          titulo_form=" Cargar ausentismo"
      else:
        form = formAusent()
        titulo_form=" Cargar ausentismo"
    '''
      ###Variable para la paginacion en un formulario,debido a que todos los formularios de la aplicacion comparten
      el mismo template .html
    '''
    if titulo_form==False:
      titulo_form=" Cargar ausentismo"
    
    pag_ausentismo=True   
    return render_to_response('appPersonal/forms/abm.html',{'user':user,'pag_ausentismo':pag_ausentismo,'titulo_form':titulo_form,'form': form, 'name':name, 'grupos':grupos,'agente':agente})

def eliminarAusent(peticion):
  idausent=peticion.GET.get('idausent')
  idagente=peticion.GET.get('idagente')
  user = peticion.user
  agente=Agente.objects.get(idagente=idagente)
  ausent=Ausent.objects.get(idausent=idausent)
  ausent.delete()

  url="detalle/detallexagente/ausentismo?idagente="+str(idagente)+"&borrado=-1"
  return render_to_response('appPersonal/mensaje.html',{'url':url,'user':user,'mensaje':'Se ha eliminado ausentismo de '+agente.apellido+' '+agente.nombres})

@login_required(login_url='login')
def abmAgente(peticion):
    
    pag_agentes=True

    user = peticion.user
    grupos = get_grupos(user)
    if permisoZona(user) and permisoABM(user) and permisoDatosAgente(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    idagente = int(peticion.GET.get('idagente'))
    name = 'Agente'
    accion = ''
    form_old=''
    if peticion.POST:
      a= Agente()
      if int(idagente) >0:
	      a = Agente.objects.get(pk=idagente)
	      form_old = formAgente(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formAgente(peticion.POST, instance=a)
	      
      else:
        form = formAgente(peticion.POST)

        if form.is_valid():
          try:
            aux = Agente.objects.get(nrodocumento=form.instance.nrodocumento)
            accion = "Modificacion"
          except Agente.DoesNotExist:
            accion = "Alta"

          if ("Datos Agente" not in get_grupos(user)):
  	          form.save()
        if accion == "Alta":
              registrar(user, name, "Alta", getTime(), None, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
        elif accion == "Modificacion":
            registrar(user, name, "Modificacion", getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
            if int(idagente) != 0:
              url = '/personal/forms/menuagente?idagente='+str(idagente)
            else:
              url = 'listado/agentes?opc=2'
              return HttpResponseRedirect(url)
    else:
      if int(idagente) >0:
        #MODIFICACION
        a = Agente.objects.get(pk=idagente)
        titulo_form=" Modificar datos personales "
        form = formAgente(instance=a)
        return render(peticion,'appPersonal/forms/abm.html',{'agente':a,'user':user,'pag_agentes':pag_agentes,'form': form,'accion':accion, 'name':name,'grupos':grupos,'titulo_form':titulo_form}) 
      
      else:
        # ALTA
        form = formAgente()
        titulo_form=" Nuevo agente "
   
    return render(peticion,'appPersonal/forms/abm.html',{'user':user,'pag_agentes':pag_agentes,'form': form,'accion':accion, 'name':name,'grupos':grupos,'titulo_form':titulo_form}) 
    


    
@login_required(login_url='login')
def abmFamiliresac(peticion):
  
    user = peticion.user
    grupos = get_grupos(user)
    name = 'Familiar a Cargo'
    form_old = ''
    accion = ''
    
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
    idfac = int(peticion.GET.get('idfac'))
    idagen = int(peticion.GET.get('idagente'))

    agente=Agente.objects.get(pk=idagen)
    
    if peticion.POST:
      if int(idfac) >0:
	      a = Asignacionfamiliar.objects.get(pk=idfac)
	      form_old = formFamiliaresac(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formFamiliaresac(peticion.POST, instance=a)   
	      accion = 'Modificacion'
      else:
	      accion = 'Alta'
	      form = formFamiliaresac(peticion.POST)
    
      if form.is_valid():
	      form.instance.idagente_id = idagen
	      form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name, accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      url = '/personal/listado/listadoxagente/facxagente?idagente='+str(idagen)+'&borrado=-1'
	      return HttpResponseRedirect(url)
    else:
      if int(idfac) > 0 and int(idagen)> 0:
        a = Asignacionfamiliar.objects.get(pk=idfac)
        form = formFamiliaresac(instance=a)
        titulo_form="Familiar a cargo"
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Asignacionfamiliar()
          b.idagente = a
          form = formFamiliaresac(instance=b)
          titulo_form="Familiar a cargo"
      else:
        form = formFamiliaresac()
        titulo_form="Nuevo familiar a cargo"
    
    pag_agentes=True
    return render_to_response('appPersonal/forms/abm.html',{'user':user,'pag_agentes':pag_agentes,'form': form, 'name':name,'grupos':grupos,'titulo_form':titulo_form,'agente':agente})

    
    
@login_required(login_url='login')
def abmAccdetrabajo(peticion):
   
   idadt=int(peticion.GET.get('idadt'))
   idagen=int(peticion.GET.get('idagen'))
   user = peticion.user
   name = 'Accidente de Trabajo'
   form_old = ''
   accion = ''
   grupos = get_grupos(user)
   
   if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
   if peticion.POST:
      if int(idadt) >0:
	      a = Accidentetrabajo.objects.get(pk=idadt)
	      form_old = formAccdetrabajo(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formAccdetrabajo(peticion.POST, instance=a)   
	      accion = 'Modificacion'
      else:
	      accion = 'Alta'
	      form = formAccdetrabajo(peticion.POST)
    
      if form.is_valid():
	      form.instance.idagente_id = idagen
	      form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name,accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	          
	      url = '/personal/listado/listadoxagente/adtxagente/'+str(form.instance.idagente_id)+'/-1/'
	      return HttpResponseRedirect(url)
   else:
    if int(idadt) > 0 and int(idagen)> 0:
      a = Accidentetrabajo.objects.get(pk=idadt)
      form = formAccdetrabajo(instance=a)
    elif int(idagen) > 0:          
      a = Agente.objects.get(pk=idagen)
      b = Accidentetrabajo()
      b.idagente = a
      form = formAccdetrabajo(instance=b)
    else:
      form = formAccdetrabajo()
      
   return render_to_response('appPersonal/forms/abm.html',{'user':user,'form': form, 'name': name, 'grupos':grupos},)


@login_required(login_url='login')
def abmSalida(peticion):
  
    user = peticion.user
    name = 'Salida'
    form_old = ''
    accion = ''
    grupos = get_grupos(user)
    
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    idsalida = int(peticion.GET.get('idsalida'))
    idagen = int(peticion.GET.get('idagente'))
    agente = Agente.objects.get(idagente=idagen)
    if peticion.POST:
      if int(idsalida) >0:
	      a = Salida.objects.get(pk=idsalida)
	      form_old = formSalida(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formSalida(peticion.POST, instance=a)   
	      accion = 'Modificacion'
      else:
	      form = formSalida(peticion.POST)
	      accion = 'Alta'
    
      if form.is_valid():
	      form.instance.idagente_id = idagen
	      form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name,accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	          
	      url = '/personal/listado/listadoxagente/salidaxagente?idagente='+str(form.instance.idagente_id)+'&borrado=-1'
	      return HttpResponseRedirect(url)
    else:
      if int(idsalida) > 0 and int(idagen)> 0:
        a = Salida.objects.get(pk=idsalida)
        form = formSalida(instance=a)
        #Variable para paginar
        titulo_form=" Salidas / "+str(a.fecha)
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Salida()
          b.idagente = a
          form = formSalida(instance=b)
          titulo_form=" Salidas / Cargar salida"
      else:
        form = formSalida()
        titulo_form=" Salidas / Cargar salida"
    pag_agentes=True
    return render_to_response('appPersonal/forms/abm.html',{'user':user,'pag_agentes':pag_agentes,'titulo_form':titulo_form,'agente':agente,'form': form, 'name':name, 'grupos':grupos})

    
@login_required(login_url='login')
def abmTraslado(peticion):
    
    idtraslado=int(peticion.GET.get('idtraslado'))
    idagen=int(peticion.GET.get('idagen'))
    user = peticion.user
    name = 'Traslado'
    form_old = ''
    accion = ''
    agente=Agente.objects.get(idagente=idagen)
    grupos = get_grupos(user)
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    if peticion.POST:
      if int(idtraslado) >0:
	      a = Traslado.objects.get(pk=idtraslado)
	      form_old = formTraslado(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formTraslado(peticion.POST, instance=a)   
	      accion = 'Modificacion'
	      
      else:
	      form = formTraslado(peticion.POST)
	      accion = 'Alta'
    
      if form.is_valid():
	      form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
	      form.instance.idagente_id = idagen
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name,accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	          
	      url = '/personal/listado/listadoxagente/traslado/'+ idagen + '/0/'
	      return HttpResponseRedirect(url)
    else:
      if int(idtraslado) > 0 and int(idagen)> 0:
        a = Traslado.objects.get(pk=idtraslado)
        form = formTraslado(instance=a)
        titulo_form=" Traslados / Modificar traslado"
          
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Traslado()
          b.idagente = a
          form = formTraslado(instance=b)
          titulo_form=" Traslados / Cargar traslado"
          
      else:
        form = formTraslado()
        titulo_form=" Traslados / Cargar traslado"
    pag_agentes=True  
    return render_to_response('appPersonal/forms/abm.html',{'pag_agentes':pag_agentes,'titulo_form':titulo_form,'agente':agente,'form': form, 'name':name, 'grupos':grupos, 'user':user},)

    
@login_required(login_url='login')
def abmSeguro(peticion,idseguro,idagen):

    user = peticion.user
    grupos = get_grupos(user)
    name = 'Seguro'
    form_old = ''
    accion = ''
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)

    
    if peticion.POST:

      if int(idseguro) >0:
	      a = Seguro.objects.get(pk=idseguro)
	      form_old = formSeguro(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formSeguro(peticion.POST, instance=a)   
	      accion = 'Modificacion'
	      
      else:
	      form = formSeguro(peticion.POST)
	      accion = 'Alta'
    
      if form.is_valid():
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name,accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	          
	      url = '/personal/listado/listadoxagente/seguro/'+idagen+'/-1/'
	      return HttpResponseRedirect(url)
    else:
      if int(idseguro) > 0 and int(idagen)> 0:
        a = Seguro.objects.get(pk=idseguro)
        form = formSeguro(instance=a)
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Seguro()
          b.idagente = a
          form = formSeguro(instance=b)
      else:
        form = formSeguro()
      
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'grupos':grupos, 'user':user}, )


@login_required(login_url='login')
def abmServicioprestado(peticion):
    idservprest=int(peticion.GET.get('idservprest'))
    idagen=int(peticion.GET.get('idagen'))
    user = peticion.user
    grupos = get_grupos(user)
    name = 'Servicio Prestado'
    form_old = ''
    accion = ''
    agente=Agente.objects.get(idagente=idagen)
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
    
    if peticion.POST:
      if int(idservprest) >0:
	      a = Servicioprestado.objects.get(pk=idservprest)
	      form_old = formServicioprestado(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formServicioprestado(peticion.POST, instance=a)   
	      accion = 'Modificacion'
      else:
	      form = formServicioprestado(peticion.POST)
	      accion = 'Alta'
    
      if form.is_valid():
	      form.instance.idagente = Agente.objects.get(pk=idagen)
	      form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name,accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	          
	      url = '/personal/listado/listadoxagente/servprest/'+idagen+'/-1/'
	      return HttpResponseRedirect(url)
    else:
      if int(idservprest) > 0 and int(idagen)> 0:
        a = Servicioprestado.objects.get(pk=idservprest)
        form = formServicioprestado(instance=a)
        titulo_form=" Servicios prestados / Cargar servicio prestado"
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Servicioprestado()
          b.idagente = a
          form = formServicioprestado(instance=b)
          titulo_form=" Servicios prestados / Cargar servicio prestado"
          
      else:
        form = formSeguro()
        titulo_form=" Servicios prestados / Cargar servicio prestado"
    pag_agentes=True  
    return render_to_response('appPersonal/forms/abm.html',{'pag_agentes':pag_agentes,'titulo_form':titulo_form,'agente':agente,'form': form, 'name':name, 'user':user, 'grupos':grupos}, )
        


@login_required(login_url='login')
def abmLicenciaanualagente(peticion,idlicanualagen,idagen):
  
    user = peticion.user
    grupos = get_grupos(user)
    name = 'Licencia Anual Agente'
    form_old = ''
    accion = ''
    
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
        

    if peticion.POST:
      if int(idlicanualagen) >0:
	      a = Licenciaanualagente.objects.get(pk=idlicanualagen)
	      form_old = formLicenciaanualagente(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formLicenciaanualagente(peticion.POST, instance=a)   
	      accion = 'Modificacion'
	      
      else:
        form = formLicenciaanualagente(peticion.POST)
        accion = 'Alta'
              
      if form.is_valid():
	      form.instance.idagente_id = idagen
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name,accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	          
	      url = '/personal/listado/listadoxagente/sancionxagente/'+str(idagen)+'/'
	      return HttpResponseRedirect(url)
    else:
      if int(idlicanualagen) > 0 and int(idagen)> 0:
        a = Licenciaanualagente.objects.get(pk=idlicanualagen)
        form = formLicenciaanualagente(instance=a)
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Licenciaanualagente()
          b.idagente = a
          form = formLicenciaanualagente(instance=b)
          
      else:
        form = formLicenciaanualagente()
      
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'user':user, 'grupos':grupos}, )

@csrf_exempt
#@login_required(login_url='login')
def abmLicenciaanual(peticion):
    idlicanual=int(peticion.GET.get('idlicanual'))
    idagen=int(peticion.GET.get('idagen'))
    anio=int(peticion.GET.get('anio'))
    user = peticion.user
    grupos = get_grupos(user)
    form_old = ''
    accion = ''
    titulo_form=''
    agente=Agente.objects.get(idagente=idagen)
    #Calculo los dias que le quedan en la licenciaAnualaGENTE para poner un 'max' en cantidad de dias en el formulario
    lic_anual_agente=Licenciaanualagente.objects.get(idagente=idagen,anio=anio)
    diasRestantes=(lic_anual_agente.cantidaddias-lic_anual_agente.diastomados)
    
    if permisoZona(user) and permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    name = 'Licencia Anual'
    
    if peticion.POST:
      if int(idlicanual) >0:
        a = Licenciaanual.objects.get(pk=idlicanual)
        form_old = formLicenciaanual(instance=a)
        modelo=Licenciaanual.objects.filter(pk=form_old.instance.pk).values_list()
        form_old=modelo
        form = formLicenciaanual(peticion.POST, instance=a)
        accion = 'Modificacion'
      else:
        form = formLicenciaanual(peticion.POST)
        accion = 'Alta'

      if form.is_valid():
      #superposicion de licencias
        jump = False
        modaus = False
        
        '''Anteriormente no se podia modificar una interrupcion
        if accion == "Modificacion" and form.instance.tipo == 'INT':
          url = "{% url 'vacas' %}?idagente="+str(idagen)
          error = ": No se puede modificar interrupcion, elimine y vuelve a cargar"
          return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos, 'url':url},)'''

        lica = Licenciaanual.objects.filter(idagente__exact=idagen).order_by('fechadesde')
        ausent = Ausent()
        try:
          if form.instance.tipo == 'LIC':
            for l in lica:
              cd = form.instance.cantdias # Datos del Formulario
              f = form.instance.fechadesde # Datos del Formulario
              cd1 = l.cantdias # Datos en la Base
              f1 = l.fechadesde # Datos en la Base
              if f == f1 and cd == cd1 and form.instance.pk == l.pk:
                jump = True
              elif (f != f1 or cd != cd1) and form.instance.pk == l.pk and accion == 'Modificacion':
                modaus = True
          elif form.instance.tipo == 'INT':
            if not analizaLic(idagen, form.instance.fechadesde):
              url = "/personal/vacas?idagente="+str(idagen)
              error = ": No existe licencia"
              return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos, 'url':url},)
            if not analizaLicanio(idagen, form.instance.fechadesde, int(anio)):
              url = "/personal/vacas?idagente="+str(idagen)
              error = ": Año no correspondiente "
              error.decode('utf-8')
              return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos, 'url':url},)
        except IndexError:
          print ("")
        #fin superposicion de licencias
        #superposicion con ausentismo
        pprint("jump: "+str(jump))
        pprint("modaus: "+str(modaus))
        if not jump and not modaus and form.instance.tipo == 'LIC':
          ausen = Ausent.objects.order_by('-fechainicio').filter(idagente__exact = idagen)
          try:
            for au in ausen:
              if au.pk != form.instance.idausent :
                cd = form.instance.cantdias # Datos del Formulario
                f = form.instance.fechadesde # Datos del Formulario
                cd1 = au.cantdias # Datos en la Base
                f1 = au.fechainicio # Datos en la Base
                if f == f1:
                  url = "/personal/vacas?idagente="+str(idagen)
                  error = ": Ya existe un ausentismo con esa fecha"
                  return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos, 'url':url},)
                for i in range(1,cd+1):
                  for j in range(1,cd1+1):
                    f = form.instance.fechadesde + timedelta(days=i)
                    f1 = au.fechainicio + timedelta(days=j)
                    if f == f1:
                      url = "/personal/vacas?idagente="+str(idagen)
                      error = ": Ya existe un ausentismo con esa fecha"
                      return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos,'url':url},)
          except IndexError:
            print ("")
        #fin superposicion ausentismo
      
        #supera dias de licencia
        if not jump and form.instance.tipo == 'LIC':
          if modaus:
            lic = Licenciaanual.objects.get(pk = form.instance.pk)
            diastomados = Licenciaanualagente.objects.get(idagente__exact = idagen, anio__exact = anio).diastomados
            diadelicencia = Licenciaanualagente.objects.get(idagente__exact = idagen, anio__exact = anio).cantidaddias
            if (form.instance.cantdias + (diastomados - lic.cantdias)) > diadelicencia:
              url = "/personal/vacas?idagente="+str(idagen)
              error = ": Supera la cantidad de dias permitidos"
              return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos, 'url':url},)
          else:
            diastomados = Licenciaanualagente.objects.get(idagente__exact = idagen, anio__exact = anio).diastomados
            diadelicencia = Licenciaanualagente.objects.get(idagente__exact = idagen, anio__exact = anio).cantidaddias
            if (form.instance.cantdias + diastomados) > diadelicencia:
              url = "/personal/vacas?idagente="+str(idagen)
              error = ": Supera la cantidad de dias permitidos"
              return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos, 'url':url},)
        #fin supera dias de licencia

        #Vinculacion con ausent
        ausent = Ausent()

        if form.instance.tipo == 'LIC':
          #Obtengo la fecha de termino de una licencia
          fechafinal=contarDiasHabiles(form.instance.fechadesde,int(form.instance.cantdias),idagen)
          #Modificacion de Licencia
          if modaus:
            ausent = Licenciaanual.objects.get(pk = form.instance.pk).idausent
            ausent.fechainicio = form.instance.fechadesde
            ausent.cantdias = form.instance.cantdias
            ausent.fechafin=fechafinal
            ausent.save()

            licenciaanual=Licenciaanual.objects.filter(idausent=ausent.idausent,tipo="LIC").first()
            licenciaanual.fechadesde=ausent.fechainicio
            licenciaanual.cantdias=ausent.cantdias
            licenciaanual.save()

            url="../vacas?idagente="+str(idagen)
            return render_to_response('appPersonal/mensaje.html',{'url':url,'user':user,'mensaje':'Licencia modificada exitosamente para el agente '+agente.apellido+' '+agente.nombres})
          #Carga de Licencia
          else:

            ausent = Ausent()
            ausent.idagente_id = idagen
            ausent.fechainicio = form.instance.fechadesde
            ausent.cantdias = form.instance.cantdias
            ausent.idarticulo_id = 999
            ausent.direccion = Agente.objects.get(pk=idagen).iddireccion
            ausent.fechafin=fechafinal
            ausent.save()
            
            #NOTA: Si se guarda una licenciaanual,un trigger se encarga de reflejaron en la tabla "licenciaanualagente"
            licenciaanual=Licenciaanual()
            licenciaanual.idausent=ausent
            licenciaanual.idagente=agente
            licenciaanual.anio=anio
            licenciaanual.tipo=form.instance.tipo
            licenciaanual.fechadesde=ausent.fechainicio
            licenciaanual.cantdias=ausent.cantdias
            licenciaanual.observaciones=ausent.observaciones
            licenciaanual.save()
        
        #Carga de interrupcion
        elif form.instance.tipo == 'INT':
          
          ausent = getLicEnFecha(idagen, form.instance.fechadesde).idausent
          
          dias_originales_lictomada=ausent.cantdias

          #La diferencia de dias entre la nueva fecha de fin(ingresada en el formulario) ,y la fecha de inicio del ausentismo
          dif_dias=diffFecha(form.instance.fechadesde , ausent.fechainicio)+1
          
          ausent.fechafin=form.instance.fechadesde

          #Obtengo la cantidad de dias habiles de la licencia que queda luego de la interrupcion
          dias_habiles=cantDias(ausent.fechainicio,dif_dias,idagen)
          
          pprint("Cant DIAS HABILES: "+str(dias_habiles))
          ausent.cantdias=dias_habiles
          
          ausent.save()
          
          #Obtengo la licenciaanual del agente
          licenciaanualagente=Licenciaanualagente.objects.get(idagente=idagen,anio=anio)
          
          #Se modifica la licencia anual
          licenciaanual=Licenciaanual.objects.filter(idausent=ausent.idausent,tipo="LIC").first()
          licenciaanual.fechainicio=ausent.fechainicio
          licenciaanual.cantdias=dias_habiles
          licenciaanual.save()
          
          if(accion == 'Modificacion'):
            #Se modifica una interrupcion
            pprint("Modificacion de una interrupcion")
            interrupcion=Licenciaanual.objects.get(pk=form.instance.pk)
            interrupcion.fechadesde=ausent.fechainicio
            interrupcion.observaciones=ausent.observaciones
            interrupcion.save()

            url="../vacas?idagente="+str(idagen)
            return render_to_response('appPersonal/mensaje.html',{'url':url,'user':user,'mensaje':'Interrupcion de licencia modificada exitosamente para el agente '+agente.apellido+' '+agente.nombres})
          else:
            #Se crea una interrupccion
            interrupcion=Licenciaanual()
            interrupcion.idausent=ausent
            interrupcion.idagente=agente
            interrupcion.anio=anio
            interrupcion.tipo=form.instance.tipo
            interrupcion.fechadesde=ausent.fechainicio
            interrupcion.observaciones=ausent.observaciones
            interrupcion.save()
          
          #Se modicia la licencianualagente con la nueva cantidad de dias tomados
          licenciaanualagente.diastomados=licenciaanualagente.diastomados-dias_originales_lictomada
          licenciaanualagente.diastomados=licenciaanualagente.diastomados+dias_habiles
          licenciaanualagente.save()
          
          url="../vacas?idagente="+str(idagen)
          return render_to_response('appPersonal/mensaje.html',{'url':url,'user':user,'mensaje':'Interrupcion de licencia generada exitosamente para el agente '+agente.apellido+' '+agente.nombres})
        '''
          if accion == 'Alta':
              registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
          elif accion == 'Modificacion':
              registrar(user, name,accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
              
          url = '/personal/vacas?idagente='+str(idagen)
          return HttpResponseRedirect(url)'''
    
    #RENDERIZACION DE FORMULARIO    
    else:
      if int(idlicanual) > 0 and int(idagen)> 0:
        a = Licenciaanual.objects.get(pk=idlicanual)

        #Obtengo el ausentismo y extraigo la fecha de fin para setear en el formulario
        ausentismo=Ausent.objects.get(idausent=a.idausent.idausent)
       
        if(a.tipo=="INT"):
          form = formLicenciaanual(initial={'fechahasta': ausentismo.fechafin,'fechadesde':ausentismo.fechafin},instance=a)
          form.fields['cantdias'].widget.attrs['readonly'] = True
        else:
          form = formLicenciaanual(initial={'fechahasta': ausentismo.fechafin},instance=a)
        
        if(a.cantdias):
          form.fields['cantdias'].widget.attrs['max']=diasRestantes+a.cantdias
        
        form.fields['tipo'].widget.attrs['readonly'] = True

        titulo_form="Detalles / Modificar licencia / "+str(a.fechadesde)
      elif int(idagen) > 0 or int(anio)> 0:          
        a = Agente.objects.get(pk=idagen)
        b = Licenciaanual()
        b.idagente = a
        b.anio = anio

        form = formLicenciaanual(instance=b)
        form.fields['cantdias'].widget.attrs['max']=diasRestantes
        
        titulo_form=" "+str(anio)
      else:
        form = formLicenciaanual()
        form.fields['cantdias'].widget.attrs['max']=diasRestantes
        titulo_form=" Cargar licencia"
    pag_licenciaanual=True
    #Obtengo los feriados para cargar en datepicker
    feriadosArray=feriados()
    return render(peticion,'appPersonal/forms/abm.html',{'feriados':feriadosArray,'pag_licenciaanual':pag_licenciaanual,'titulo_form':titulo_form,'agente':agente,'form':form,'name':name,'user':user, 'grupos':grupos})
    #FIN RENDERIZACION DE FORMULARIO

#Funcion que retorna un array(de strings) con todas las fechas de feriados de la base de datos
def feriados():

  objectsFeriados=Feriado.objects.all()
  feriados=[]
  for objectsF in objectsFeriados:
      #Obtengo dia,mes,anio
      dia=datetime.strftime(objectsF.Fecha, '%d')
      mes=datetime.strftime(objectsF.Fecha, '%m')
      anio=datetime.strftime(objectsF.Fecha, '%Y')
      
      #Quito 0 a la izquierda para que el formato sea reconocido por datepicker
      feriado_dia=dia.lstrip('+-0')
      feriado_mes=mes.lstrip('+-0')
      
      #Creo la fecha en formato de string
      fecha_feriado=""+feriado_mes+"-"+feriado_dia+"-"+anio
      feriados.append(fecha_feriado)

  return feriados

#Funcion que cuenta los dias habiles(lunes a viernes) entre dos fechas(se omiten findes asi como tambien feriados)
def cantDias(fechainicio,cantdias,idagente):
  fechafinal=fechainicio
  i=0
  cantdias_habiles=0

  while i<=cantdias:
    if(i==cantdias):
      fechafinal=fechafinal-timedelta(days=1)
      break
    #Si la fecha es sabado o domingo incremento en uno la fecha final
    if(fechafinal.strftime("%A") == "Sunday" or fechafinal.strftime("%A") == "Saturday"):
      fechafinal=fechafinal+timedelta(days=1)
      i+=1 

    #Si es un feriado incremento en uno la fecha final
    elif(esFeriado(idagente,fechafinal)):
      fechafinal=fechafinal+timedelta(days=1)
      i+=1 
    #Si es un dia 'normal' ademas de incrementar la fecha incremento el contador "i"
    else:
        fechafinal=fechafinal+timedelta(days=1)
        cantdias_habiles+=1
        i+=1 

  return cantdias_habiles

#Adapto la funcion "contardiashabiles" de la base de datos,a codigo python
def contarDiasHabiles(fechainicio,cantdias,idagente):
  
  fechafinal=fechainicio
  i=0
  #Contadores de sabados/domingos y feriados
  sabados_y_domingos=0
  feriados=0

  while i<=cantdias:
    if(i==cantdias):
      fechafinal=fechafinal-timedelta(days=1)
      break

    #Si la fecha es sabado o domingo incremento en uno la fecha final
    if(fechafinal.strftime("%A") == "Sunday" or fechafinal.strftime("%A") == "Saturday"):
      sabados_y_domingos+=1
      fechafinal=fechafinal+timedelta(days=1)

    #Si es un feriado incremento en uno la fecha final
    elif(esFeriado(idagente,fechafinal)):
      pprint("SE ENCONTRO UN FERIADO el dia "+str(fechafinal))
      feriados+=1
      fechafinal=fechafinal+timedelta(days=1)

    #Si es un dia 'normal' ademas de incrementar la fecha incremento el contador "i"
    else:
        fechafinal=fechafinal+timedelta(days=1)
        i+=1 

  pprint("*Cantdias="+str(cantdias)+" *sabados_y_domingos="+str(sabados_y_domingos)+" *Feriados="+str(feriados)+" *Fecha inicio="+str(fechainicio))
  pprint("Fecha final: "+str(fechafinal))

  return fechafinal
  

#Adapto la funcion "esferiado" de la base de datos,a codigo python
def esFeriado(idagente,fechadada):
  zona=Agente.objects.get(idagente=idagente).idzonareal.idzona
  try:
    feriado=Feriado.objects.get(Fecha=fechadada)
    pprint(feriado)
  except Exception as e:
    feriado = None

  if(feriado==None):
    return False
  else:
    if(feriado.lugar == 0):
      return True
    else:
      if(feriado.lugar == zona):
        return True
      else:
        return False


#Metodo que valida si una licencia nueva o a modificar,se superpone sobre alguna tomada
def validarFechaLicencia(idagente,fecha,cantdias,idausentismo):
  
  ausentismos=Ausent.objects.filter(idagente=idagente)
  superposicion=0
  #Recorro todos los ausentismos
  for ausent in ausentismos:
    #Si se recibe un id de ausentismo,significa que es una modificacion asique al momento de comparar las fechas la misma no se toma en cuenta
    if(ausent.idausent!=idausentismo):
      try:
        
        pprint("superposicion: "+str(superposicion))
            
        pprint("|*Idausent: "+str(ausent.idausent)+"\n*Fecha inicio: "+str(ausent.fechainicio)+"\n *Fecha fin: "+str(ausent.fechafin)+"\n *Nueva fecha: "+str(fecha)+"\n *FIN Nueva fecha"+str(fecha+timedelta(days=cantdias-1))+"| \n ---------------")
        if(ausent.fechainicio <= fecha+timedelta(days=cantdias-1) <= ausent.fechafin):
          superposicion=superposicion+1
        
      except Licenciaanual.DoesNotExist as e:
        pprint("licencia no encontrada")
    else:
      pprint("SON IGUALES: "+str(idausentismo)+" -- "+str(ausent.idausent))

  #Si no se encontro ningun ausentismo con esa fecha retorno verdadero
  if(superposicion>0):
    return False
  else:
    return True

@csrf_exempt
#Metodo que recibe un id de una licencia,la busca y la elimina de la base de datos,asi como tambien sus referencias a otras tablas en la base de datos       
def eliminarLicenciaTomada(peticion):
  user = peticion.user
  idagente=int(peticion.GET.get('idagente'))
  agente=Agente.objects.get(idagente=idagente)
  idlicanual=int(peticion.GET.get('idlicanual'))
  anio=int(peticion.GET.get('anio'))
  
  licencia = Licenciaanual.objects.get(pk=idlicanual)
  licenciaanualagente=Licenciaanualagente.objects.get(idagente=idagente,anio=anio)
  #Si la licencia es de tipo "INT" la elimino de la tabla licenciaanual y retorno
  if licencia.tipo=='INT':
    pprint("Eliminacion de una interrupcion")
    dias_totales=licenciaanualagente.diastomados
    licencia.delete()
    licenciaanualagente.diastomados=dias_totales
    licenciaanualagente.save()
    url="vacas?idagente="+str(idagente)
    return render_to_response('appPersonal/mensaje.html',{'url':url,'user':user,'mensaje':'Se ha eliminado interrupcion de licencia de '+agente.apellido+' '+agente.nombres})
  #Si por el contrario,la licencia es de tipo "LIC" la elimino de la tabla licenciaanual asi como tambien su referencia a las otras tablas
  else:
    pprint("Eliminacion de una licencia")
    
    ausent=Ausent.objects.get(idausent=licencia.idausent.idausent)
    
    #Elimino la licencia de la tabla "licenciaanual"
    licencia.delete()
    '''
    A su vez elimino el ausentismo generado a partir de la licencia creada,es decir elimino el ausentismo
    que hace referencia a la licencia eliminada en la tabla "ausent" 
    '''
    ausent.delete()

    licenciaanualagente.diastomados=licenciaanualagente.diastomados-ausent.cantdias
    licenciaanualagente.save()
    url="vacas?idagente="+str(idagente)
    return render_to_response('appPersonal/mensaje.html',{'url':url,'user':user,'mensaje':'Se ha eliminado licencia de '+agente.apellido+' '+agente.nombres})

@login_required(login_url='login')
def abmSancion(peticion):

    idsan=int(peticion.GET.get('idsan'))
    idagen=int(peticion.GET.get('idagen'))
    user = peticion.user
    grupos = get_grupos(user)
    name = 'Sanción'
    form_old = ''
    accion = ''
    
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
    
    if peticion.POST:
      if int(idsan) >0:
	      a = Sancion.objects.get(pk=idsan)
	      form_old = formSancion(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formSancion(peticion.POST, instance=a)
	      accion = 'Modificacion'
	      
      else:
	      form = formSancion(peticion.POST)
	      accion = 'Alta'
    
      if form.is_valid():
	      form.instance.idagente_id = idagen
	      form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name, accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      url = 'appPersonal/listado/listadoxagente/sancionxagente/'+str(idagen)+'/-1/'
	      return HttpResponseRedirect(url)
    else:
      if int(idsan) > 0 and int(idagen)> 0:
        a = Sancion.objects.get(pk=idsan)
        form = formSancion(instance=a)
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Sancion()
          b.idagente = a
          form = formSancion(instance=b)
      else:
        form = formSancion()
      
    return render_to_response(peticion,'appPersonal/forms/abm.html',{'form': form, 'name':name, 'user':user, 'grupos':grupos})
    
        

@login_required(login_url='login')
def abmLicencia(peticion,idlicencia,idagen):
  
    user = peticion.user
    grupos = get_grupos(user)
    name = 'Licencia'
    accion = ''
    form_old=''
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
    if peticion.POST:
      
      if int(idlicencia) >0:
	      a = Licencia.objects.get(pk=idlicencia)
	      form_old = formLicencia(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formLicencia(peticion.POST, instance=a)
	      accion = 'Modificacion'
      else:
	      form = formLicencia(peticion.POST)
	      accion = 'Alta'
    
      if form.is_valid():
        form.save()
        if accion == "Alta":
          registrar(user, name, accion, getTime(), None, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
        elif accion == "Modificacion":
          registrar(user, name, accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
          url = '/personal/index/'
          return HttpResponseRedirect(url)
    else:
      if int(idlicencia) > 0 and int(idagen)> 0:
        a = Licencia.objects.get(pk=idservprest)
        form = formLicencia(instance=a)
      elif int(idagen) > 0:          
        a = Agente.objects.get(pk=idagen)
        b = Licencia()
        b.idagente = a
        form = formLicencia(instance=b)
          
      else:
        form = formLicencia()
    
    return render_to_response('appPersonal/forms/abm.html',{'user':user,'form': form, 'name':name, 'user':user, 'grupos':grupos}, )

    
    
@login_required(login_url='login')
def abmCertificadoaccidente(peticion,idcertf, idacc, idagen):
    
    user = peticion.user
    grupos = get_grupos(user)
    name = 'Certificado Accidente de Trabajo'
    accion = ''
    form_old=''
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
    grupos = get_grupos(user)
    if peticion.POST:
    
      if int(idcertf) >0:
	      a = Certificadoaccidente.objects.get(pk=idcertf)
	      form_old = formCertificadoaccidente(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formCertificadoaccidente(peticion.POST, instance=a)
	      accion = 'Modificacion'

      else:
	      form = formCertificadoaccidente(peticion.POST)
	      accion = 'Alta'
    
      if form.is_valid():
        form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
        form.fields['idaccidentetrabajo'].widget.attrs['enabled'] = 'enabled'
        form.instance.idagente_id = idagen
        form.instance.idaccidentetrabajo_id = idacc
        b = Accidentetrabajo.objects.get(pk=idacc)
        form.instance.nroexpediente = b.nroexpediente
        form.save()
        if accion == "Alta":
          registrar(user, name, accion, getTime(), None, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
        elif accion == "Modificacion":
          registrar(user, name, accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
          url = '/personal/listado/listadoxaccdt/certificadoxaccdt/'+str(idacc)+'/'+str(form.instance.idagente_id)+'/-1/'
          return HttpResponseRedirect(url)
        else:
          if int(idacc) > 0 and int(idagen)> 0 and int(idcertf)> 0:
            a = Certificadoaccidente.objects.get(pk=idcertf)
            form = formCertificadoaccidente(instance=a)
    elif int(idagen) > 0 or int(idacc)>0:
      a = Agente.objects.get(pk=idagen)
      b = Accidentetrabajo.objects.get(pk=idacc)
      c = Certificadoaccidente()
      c.idagente = a
      c.idaccidentetrabajo = b
      form = formCertificadoaccidente(instance=c)
          
    else:
      form = formCertificadoaccidente()
      
    return render_to_response('appPersonal/forms/abm.html',{'user':user,'form': form, 'name':name, 'user':user, 'grupos':grupos}, ) 
 

@login_required(login_url='login')
def abmAdscriptos(peticion,idads, idagen):
    
    user = peticion.user
    grupos = get_grupos(user)
    name = 'Adsciptos'
    form_old = ''
    accion = ''
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
    
    if peticion.POST:
       
      if int(idads) > 0 :
	      a = Adscripcion.objects.get(pk=idads)
	      form_old = formAdscriptos(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formAdscriptos(peticion.POST, instance=a)   
	      accion = 'Modificacion'

      else:
	      form = formAdscriptos(peticion.POST)
	      accion = 'Alta'
	      
      if form.is_valid():
	      form.instance.idagente_id = idagen
	      form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name, accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      url = '/personal/index/'
	      return HttpResponseRedirect(url)
    else:
      if int(idads) > 0 and int(idagen)> 0:
        a = Adscripcion.objects.get(pk=idads)
        form = formAdscriptos(instance=a)
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Adscripcion()
          b.idagente = a
          form = formAdscriptos(instance=b)
      else:
        form = formAdscriptos()
      
    return render_to_response('appPersonal/forms/abm.html',{'user':user,'form': form, 'name':name, 'user':user, 'grupos':grupos}, )  
 
@login_required(login_url='login')
def abmEstudioscursados(peticion):
    
    idestcur=int(peticion.GET.get('idestcur'))
    idagen=int(peticion.GET.get('idagen'))
    user = peticion.user
    grupos = get_grupos(user)
    name = 'Estudios Cursados'
    form_old = ''
    accion = ''
    agente=Agente.objects.get(idagente=idagen)
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
    if peticion.POST:
      if int(idestcur) >0:
	      a = Estudiocursado.objects.get(pk=idestcur)
	      form_old = formEstudiosCursados(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formEstudiosCursados(peticion.POST, instance=a)   
	      accion = 'Modificacion'

      else:
	      form = formEstudiosCursados(peticion.POST)
	      accion = 'Alta'
	      
      if form.is_valid():
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name, accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      url = '/personal/listado/listadoxagente/estudioscursados/'+ idagen +'/-1/'
	      return HttpResponseRedirect(url)
    else:
      if int(idestcur) > 0 and int(idagen)> 0:
        a = Estudiocursado.objects.get(pk=idestcur)
        form = formEstudiosCursados(instance=a)
        titulo_form=" Estudios cursados / Modificar estudio cursado"
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Estudiocursado()
          b.idagente = a
          form = formEstudiosCursados(instance=b)
          titulo_form=" Estudios cursados / Cargar estudio cursado"
      else:
        form = formEstudiosCursados()
        titulo_form=" Estudios cursados / Cargar estudio cursado"
    '''
    ###Variable para la paginacion en un formulario,debido a que todos los formularios de la aplicacion comparten
      el mismo template .html
    '''
    pag_agentes=True
    return render_to_response('appPersonal/forms/abm.html',{'pag_agentes':pag_agentes,'titulo_form':titulo_form,'agente':agente,'form': form,'name':name,'grupos':grupos, 'user':user}, )

    
@login_required(login_url='login')
def abmArticulos(peticion,idarticulo):
  
    user = peticion.user
    grupos = get_grupos(user)
    name = 'Artículo'
    form_old = ''
    accion = ''
    
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
    
    if peticion.POST:
      if int(idarticulo) >0:
	      a = Articulo.objects.get(pk=idarticulo)
	      form_old = formArticulos(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formArticulos(peticion.POST, instance=a)   
	      accion = 'Modificacion'
      else:
	      form = formArticulos(peticion.POST)
	      accion = 'Alta'
    
      if form.is_valid():
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name, accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      url = '/personal/index/'
	      return HttpResponseRedirect(url)
    else:
      if int(idarticulo) >0:
        a = Articulo.objects.get(pk=idarticulo)
        form = formArticulos(instance=a)
        titulo_form="Modificar articulo"
      else:
          form = formArticulos()
          titulo_form="Cargar articulo"
      pag_articulos=True
      return render_to_response('appPersonal/forms/abm.html',{'pag_articulos':pag_articulos,'titulo_form':titulo_form,'form': form, 'name':name, 'grupos':grupos, 'user':user}, )

    
@login_required(login_url='login')
def abmEscolaridad(peticion):
    
    idescolaridad=int(peticion.GET.get('idescolaridad'))
    idasigfam=int(peticion.GET.get('idasigfam'))
    user = peticion.user
    grupos = get_grupos(user)
    name = 'Escolaridad'
    form_old = ''
    accion = ''
    
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
    if peticion.POST:
      
    
      if int(idescolaridad) >0:
	      a = Escolaridad.objects.get(pk=idescolaridad)
	      form_old = formEscolaridad(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formEscolaridad(peticion.POST, instance=a)
	      accion = 'Modificacion'
      else:
	      form = formEscolaridad(peticion.POST)
	      accion = 'Alta'
    
      if form.is_valid():
	      form.instance.idasigfam_id = idasigfam
	      form.fields['idasigfam'].widget.attrs['enabled'] = 'enabled'
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name, accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	          
	      url = '/personal/listado/listadoxaf/escolaridadxaf?idfac='+str(form.instance.idasigfam_id)+'&borrado=-1'
	      return HttpResponseRedirect(url)
    else:
      if int(idescolaridad) > 0  and int(idasigfam)> 0:
        a = Escolaridad.objects.get(pk=idescolaridad)
        form = formEscolaridad(instance=a)
      elif int(idasigfam)>0:
        b = Asignacionfamiliar.objects.get(pk=idasigfam)
        c = Escolaridad()
        c.idasigfam = b
        form = formEscolaridad(instance=c)
      else:
        form = formEscolaridad()
    
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name,'grupos':grupos, 'user':user}, ) 
    
    
@csrf_exempt   
@login_required(login_url='login')
def abmMedica(peticion):
    
    user = peticion.user
    grupos = get_grupos(user)
    idagen = int(peticion.GET.get('idagente'))
    idmed = int(peticion.GET.get('idmedica'))
    agente=Agente.objects.get(idagente=idagen)
    try:
      idausent = int(peticion.GET.get('idausent'))
    except ValueError:
        idausent = None
    name = 'Medica'
    form_old = ''
    accion = ''
    
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    
    if peticion.POST:
       
      if int(idmed) > 0 :
	      a = Medica.objects.get(pk=idmed)
	      form_old = formMedica(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formMedica(peticion.POST, instance=a)   
	      accion = 'Modificacion'
	      
      else:
	      form = formMedica(peticion.POST)
	      accion = 'Alta'
    
      if form.is_valid():
        form.fields['agente'].widget.attrs['enabled'] = 'enabled'
        #form.fields['idausent'].widget.attrs['enabled'] = 'enabled'
        form.instance.agente = Agente.objects.get(pk=idagen)
        form.instance.idausent = Ausent.objects.get(pk=idausent)
        form.save()
        
        ###Retornar al index de licencias medicas###
        medica=Medica.objects.filter(agente__exact=idagen)
        lista=paginar(medica,peticion)
        return render_to_response('appPersonal/listado/listadoxagente/medicaxagente.html',{'lista':lista,'user':user,'idagente':idagen,'agente':agente,'grupos':grupos, 'idausent':idausent})
        '''if accion == 'Alta':
          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.get(pk=form.instance.pk)))
        elif accion == 'Modificacion':
          registrar(user, name, accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
          url = "listado/listadoxagente/medica?idagente='+str(idagen)+'&borrado=-1&idausent='+str(idausent)"
          return HttpResponseRedirect(url)'''
    else:
      if int(idmed) > 0 and int(idagen)> 0:
        a = Medica.objects.get(pk=idmed)
        form = formMedica(instance=a)
        titulo_form="Modificar licencia medica"
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          aus = Ausent.objects.get(pk=idausent)
          b = Medica()
          b.agente = a
          b.idausent = aus
          form = formMedica(instance=b)
          titulo_form="Modificar licencia medica"
      else:
        form = formMedica()
        titulo_form="Nueva licencia medica"
    
    pag_medica=True
    return render_to_response('appPersonal/forms/abm.html',{'idausent':idausent,'titulo_form':titulo_form,'pag_medica':pag_medica,'agente':agente,'form': form , 'name':name, 'user':user, 'grupos':grupos},)
    

@login_required(login_url='login')
def abmJuntaMedica(peticion):
    
    idjm=int(peticion.GET.get("idjm"))
    idmed=int(peticion.GET.get("idmed"))
    idagen=int(peticion.GET.get("idagen"))
    user = peticion.user
    name = 'Junta Medica'
    form_old = ''
    accion = ''
    grupos = get_grupos(user)
    if permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)
    if peticion.POST:
    
    
      if int(idjm) >0:
	      a = Juntamedica.objects.get(pk=idjm)
	      form_old = formJuntaMedica(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formJuntaMedica(peticion.POST, instance=a)   
	      accion = 'Modificacion'

      else:
	      form = formJuntaMedica(peticion.POST)
	      accion = 'Alta'
    
      if form.is_valid():
	      form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
	      form.fields['medica'].widget.attrs['enabled'] = 'enabled'
	      form.instance.idagente_id = idagen
	      b = Medica.objects.get(pk=idmed)
	      form.instance.medica = b
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name, accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      
	      url = '/personal/listado/listadoxmedica/juntamedica/'+str(form.instance.idagente_id)+'/'+str(idmed)+'/-1/'
	      return HttpResponseRedirect(url)
    else:
      if int(idjm) > 0 and int(idagen)> 0 and int(idmed)> 0:
        a = Juntamedica.objects.get(pk=idjm)
        form = formJuntaMedica(instance=a)
      elif int(idagen) > 0 or int(idmed)>0:          
          a = Agente.objects.get(pk=idagen)
          b = Medica.objects.get(pk=idmed)
          c = Juntamedica()
          c.idagente = a
          c.medica = b
          form = formJuntaMedica(instance=c)
      else:
        form = formJuntaMedica()
      
      return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'user':user, 'grupos':grupos}, ) 
    
    
@login_required(login_url='login')
def abmJuntaMedicavieja(peticion):
  
    user = peticion.user
    name = 'Junta Medica'
    idagente = str(peticion.GET.get('idagente'))
    idjm = str(peticion.GET.get('idjm'))
    grupos = get_grupos(user)
    
    if peticion.POST:
      try:
      	if int(idjm) >0:
      		a = Juntamedicavieja.objects.get(pk=idjm)
      		form = formJuntamedicavieja(peticion.POST, instance=a)   
      	else:
      		form = formJuntamedicavieja(peticion.POST)
      except ValueError:
          form = formJuntamedicavieja(peticion.POST)
      if form.is_valid():
          form.save()
          url = '/patrimonio/index/'
          return HttpResponseRedirect(url)
    else:
      try:
        if int(idagente) > 0 and int(idjm)> 0:
          a = Juntamedicavieja.objects.get(pk=idjm)
          form = formJuntamedicavieja(instance=a)
        elif int(idagente) > 0:        
          a = Agente.objects.get(pk=idagente)
          b = Juntamedicavieja()
          b.idagente = a
          form = formJuntamedicavieja(instance=b)
        else:
          form = formJuntamedicavieja()
      except ValueError:
        form = formJuntamedicavieja()
      	
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'user':user, 'grupos':grupos}, )

@login_required(login_url='login')
def abmMedicavieja(peticion):
  
    user = peticion.user
    name = 'Medica'
    idagente = str(peticion.GET.get('idagente'))
    idm = str(peticion.GET.get('idm'))
    grupos = get_grupos(user)
    agente=Agente.objects.get(idagente=idagente)
    pag_medicavieja=True
    if peticion.POST:
      try:
        if int(idm) >0:
          a = Medicavieja.objects.get(pk=idm)
          form = formMedicavieja(peticion.POST, instance=a)   
        else:
          form = formMedicavieja(peticion.POST)
      except ValueError:
        form = formMedicavieja(peticion.POST)
      if form.is_valid():
        form.save()
        url = '/patrimonio/index/'
        return HttpResponseRedirect(url)
    else:
      try:
        if int(idagente) > 0 and int(idm)> 0:
          a = Medicavieja.objects.get(pk=idm)
          form = formMedicavieja(instance=a)

        elif int(idagente) > 0:        
          a = Agente.objects.get(pk=idagente)
          b = Medicavieja()
          b.idagente = a
          form = formMedicavieja(instance=b)
          return render_to_response('appPersonal/forms/abm.html',{'pag_medicavieja':pag_medicavieja,'agente':a,'form': form, 'name':name, 'user':user, 'grupos':grupos}, )
        else:
          form = formMedicavieja()
      except ValueError:
        form = formMedicavieja()
	  
    return render_to_response('appPersonal/forms/abm.html',{'idm':idm,'agente':agente,'pag_medicavieja':pag_medicavieja,'form': form, 'name':name, 'user':user, 'grupos':grupos}, )

@login_required(login_url='login')
def abmLicenciaanualvieja(peticion):
  
    user = peticion.user
    name = 'Licencia'
    idagente = str(peticion.GET.get('idagente'))
    agente=Agente.objects.get(idagente=idagente)
    idlic = str(peticion.GET.get('idlic'))
    grupos = get_grupos(user)
    if peticion.POST:
      try:
        if int(idlic) >0:
          a = Licenciaanualvieja.objects.get(pk=idlic)
          form = formLicenciaanualvieja(peticion.POST, instance=a)   
        else:
          form = formLicenciaanualvieja(peticion.POST)
      except ValueError:
        form = formLicenciaanualvieja(peticion.POST)
        if form.is_valid():
          form.save()
          url = '/patrimonio/index/'
          return HttpResponseRedirect(url)
    else:
      try:
        if int(idagente) > 0 and int(idlic)> 0:
          a = Licenciaanualvieja.objects.get(pk=idlic)
          form = formLicenciaanualvieja(instance=a)
        elif int(idagente) > 0:        
          a = Agente.objects.get(pk=idagente)
          b = Licenciaanualvieja()
          b.idagente = a
          form = formLicenciaanualvieja(instance=b)

        else:
          form = formLicenciaanualvieja()
      except ValueError:
          form = formLicenciaanualvieja()

    pag_licenciavieja=True
    return render_to_response('appPersonal/forms/abm.html',{'pag_licenciavieja':pag_licenciavieja,'agente':agente,'form': form, 'name':name, 'user':user, 'grupos':grupos}, )

@csrf_exempt
@login_required(login_url='login')
def altaFeriado(peticion):
  name="Feriado"
  user=peticion.user
  grupos = get_grupos(user)
  idferiado=int(peticion.GET.get('idferiado'))

  if(peticion.POST):
    fecha=datetime.strptime(peticion.POST['Fecha'], '%d/%m/%Y')
    feriado=Feriado()
    mensaje="Feriado creado el dia "+str(fecha.strftime('%d/%m/%Y'))
    feriado.Fecha=fecha
    feriado.descripcion=peticion.POST['descripcion']
    feriado.lugar=int(peticion.POST['lugar'])
    feriado.save()
    url="listado/feriados$"
    return render_to_response('appPersonal/mensaje.html',{'url':url,'user':user,'mensaje':mensaje})
  else:
    feriadosArray=feriados()
    pag_feriado=True
    form=formFeriado()
    return render_to_response('appPersonal/forms/abm.html',{'feriados':feriadosArray,'pag_feriado':pag_feriado,'form': form, 'name':name, 'user':user, 'grupos':grupos}, )

@csrf_exempt
def modificarFeriado(peticion):
  name="Feriado"
  user=peticion.user
  grupos = get_grupos(user)
  idferiado=int(peticion.GET.get('idferiado'))

  if(peticion.POST):
    fecha=datetime.strptime(peticion.POST['Fecha'], '%d/%m/%Y')
    feriado=Feriado.objects.get(idferiado=idferiado)
    mensaje="Feriado del dia "+str(feriado.Fecha.strftime('%d/%m/%Y'))+" modificado correctamente"
    feriado.Fecha=fecha
    feriado.descripcion=peticion.POST['descripcion']
    feriado.lugar=int(peticion.POST['lugar'])
    feriado.save()
    url="listado/feriados$"
    return render_to_response('appPersonal/mensaje.html',{'url':url,'user':user,'mensaje':mensaje})
  else:
    feriadosArray=feriados()
    pag_feriado=True
    feriado=Feriado.objects.get(idferiado=idferiado)
    form=formFeriado(instance=feriado)
    return render_to_response('appPersonal/forms/abm.html',{'feriados':feriadosArray,'pag_feriado':pag_feriado,'form': form, 'name':name, 'user':user, 'grupos':grupos}, )


@csrf_exempt
@login_required(login_url='login')
def eliminarFeriado(peticion):
  name="Feriado"
  user=peticion.user
  grupos = get_grupos(user)
  
  idferiado=int(peticion.GET.get('idferiado'))
  feriado=Feriado.objects.get(idferiado=idferiado)
  fecha=feriado.Fecha
  feriado.delete()
  
  mensaje="Se ha eliminado el feriado del dia "+str(fecha.strftime('%d/%m/%Y'))
  url="listado/feriados$?mensaje="+str(mensaje)
  
  return render_to_response('appPersonal/mensaje.html',{'url':url,'user':user,'mensaje':mensaje})
  
  