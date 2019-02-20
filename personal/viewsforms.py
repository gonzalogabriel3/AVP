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


#--------------------------------------------------------------------------
#---------------------------------VIEW FORM--------------------------------
@csrf_exempt
@login_required(login_url='login')
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
       
    cache.clear()
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'grupos':grupos}, )

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
          f = form.instance.fecha
          if f == fd:
            error = ": El agente se encuentra de vacaciones"
            return render_to_response('error.html',{'user':user,'error':error, 'grupos':grupos},)
          for i in range(1,cd):
            for j in range(1,cdl):
              f = form.instance.fecha + timedelta(days=i)
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
        form.save()
        for i in range(1,cd):
          a = Ausent()
          a.fechafin = form.instance.fechafin + timedelta(days=i)
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
        form = formAusentismo(instance=a)
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Ausent()
          b.idagente = a
          b.direccion = a.iddireccion 
          form = formAusent(instance=b)
          
      else:
        form = formAusent()
       
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'grupos':grupos})

@login_required(login_url='login')
def abmAgente(peticion):
    
    
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
        form = formAgente(instance=a)
      else:
        # ALTA
        form = formAgente()
      
    return render_to_response('appPersonal/forms/abm.html',{'form': form,'accion':accion, 'name':name,'grupos':grupos})


    
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
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Asignacionfamiliar()
          b.idagente = a
          form = formFamiliaresac(instance=b)
      else:
        form = formFamiliaresac()
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name,'grupos':grupos})

    
    
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
      
   return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name': name, 'grupos':grupos},)


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
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Salida()
          b.idagente = a
          form = formSalida(instance=b)
          
      else:
        form = formSalida()
      
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'grupos':grupos})

    
@login_required(login_url='login')
def abmTraslado(peticion):
    
    idtraslado=int(peticion.GET.get('idtraslado'))
    idagen=int(peticion.GET.get('idagen'))
    user = peticion.user
    name = 'Traslado'
    form_old = ''
    accion = ''
    
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
          
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Traslado()
          b.idagente = a
          form = formTraslado(instance=b)
          
          
      else:
        form = formTraslado()
      
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'grupos':grupos, 'user':user},)

    
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
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Servicioprestado()
          b.idagente = a
          form = formServicioprestado(instance=b)
          
      else:
        form = formSeguro()
      
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'user':user, 'grupos':grupos}, )
        


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
@login_required(login_url='login')
def abmLicenciaanual(peticion):
    idlicanual=int(peticion.GET.get('idlicanual'))
    idagen=int(peticion.GET.get('idagen'))
    anio=int(peticion.GET.get('anio'))
    user = peticion.user
    grupos = get_grupos(user)
    form_old = ''
    accion = ''
    
    if permisoZona(user) and permisoABM(user):
        error = "no posee permiso para carga de datos"
        return render_to_response('appPersonal/error.html',{'user':user,'error':error,'grupos':grupos},)

    name = 'Licencia Anual'

    if peticion.POST:
      if int(idlicanual) >0:
	      a = Licenciaanual.objects.get(pk=idlicanual)
	      form_old = formLicenciaanual(instance=a)
	      form_old = modeloLista(form_old.Meta.model.objects.filter(pk=form_old.instance.pk).values_list())
	      form = formLicenciaanual(peticion.POST, instance=a)   
	      accion = 'Modificacion'
      else:
	      form = formLicenciaanual(peticion.POST)
	      accion = 'Alta'
 
      if form.is_valid():
	      # superposicion de licencias
        jump = False
        modaus = False
        if accion == "Modificacion" and form.instance.tipo == 'INT':
          url = "/personal/vacas?idagente="+str(idagen)
          error = ": No se puede modificar interrupcion, elimine y vuelve a cargar"
          return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos, 'url':url},)

        lica = Licenciaanual.objects.filter(idagente__exact=idagen).order_by('fechadesde')
        ausent = Ausent()
        try:
          if form.instance.tipo == 'LIC':
            for l in lica:
              cd = form.instance.cantdias # Datos del Formulario
              f = form.instance.fechadesde # Datos del Formulario
              cd1 = l.cantdias # Datos en la Base
              f1 = l.fechadesde # Datos en la Base
			  # form.instance.pk == lica[0].pk && 
              if f == f1 and cd == cd1 and form.instance.pk == l.pk:
                jump = True
              elif (f != f1 or cd != cd1) and form.instance.pk == l.pk and accion == 'Modificacion':
                modaus = True
          elif form.instance.tipo == 'INT':
            if not analizaLic(idagen, form.instance.fechadesde):
              url = "/personal/vacas?idagente="+str(idagen)
              error = ": No existe licencia"
              return render_to_response('personal/error.html',{'user':user,'error':error, 'grupos':grupos, 'url':url},)
              if not analizaLicanio(idagen, form.instance.fechadesde, int(anio)):
                url = "/personal/vacas?idagente="+str(idagen)
                error = ": Año no correspondiente "
                error.decode('utf-8')
                return render_to_response('appPersonal/error.html',{'user':user,'error':error, 'grupos':grupos, 'url':url},)
        except IndexError:
	          print ("")
		# fin superposicion de licencias

	      # superposicion con ausentismo
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
                  return render_to_response('personal/error.html',{'user':user,'error':error, 'grupos':grupos, 'url':url},)
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
	      # fin superposicion ausentismo
	      
	      # supera dias de licencia
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
	      # fin supera dias de licencia

	      # Vinculacion con ausent
        ausent = Ausent()
      if form.instance.tipo == 'LIC':
        if modaus:
          ausent = Licenciaanual.objects.get(pk = form.instance.pk).idausent
          ausent.fechainicio = form.instance.fechadesde
          ausent.cantdias = form.instance.cantdias
          ausent.save()
        else:
          ausent = Ausent()
          ausent.idagente_id = idagen
          ausent.fechainicio = form.instance.fechadesde
          ausent.cantdias = form.instance.cantdias
          ausent.idarticulo_id = 999 
          ausent.direccion = Agente.objects.get(pk=idagen).iddireccion
          ausent.save()
      elif form.instance.tipo == 'INT':
        ausent = getLicEnFecha(idagen, form.instance.fechadesde).idausent
        ausent.save()
        # vinculacion con ausent
        form.fields['anio'].widget.attrs['enabled'] = 'enabled'
        form.instance.anio = anio
        form.fields['idagente'].widget.attrs['enabled'] = 'enabled'
        form.instance.idagente_id = idagen
        form.fields['idausent'].widget.attrs['enabled'] = 'enabled'
        form.instance.idausent = ausent
        form.save()
        if form.instance.tipo == 'INT':
          ausent = getLicEnFecha(idagen, form.instance.fechadesde).idausent
          ausent.cantdias = diffFecha(form.instance.fechadesde , ausent.fechainicio)
          ausent.save()
          if accion == 'Alta':
            registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
          elif accion == 'Modificacion':
            registrar(user, name,accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
            url = '/personal/vacas?idagente='+str(idagen)
            return HttpResponseRedirect(url)
    else:
      if int(idlicanual) > 0 and int(idagen)> 0:
        a = Licenciaanual.objects.get(pk=idlicanual)
        form = formLicenciaanual(instance=a)
      elif int(idagen) > 0 or int(anio)> 0:          
        a = Agente.objects.get(pk=idagen)
        b = Licenciaanual()
        b.idagente = a
        b.anio = anio

        form = formLicenciaanual(instance=b)
      else:
        form = formLicenciaanual()

    return render(peticion,'appPersonal/forms/abm.html',{'form':form,'name':name,'user':user, 'grupos':grupos})
        
        
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
    
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'user':user, 'grupos':grupos}, )

    
    
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
      
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'user':user, 'grupos':grupos}, ) 
 

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
      
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'user':user, 'grupos':grupos}, )  
 
@login_required(login_url='login')
def abmEstudioscursados(peticion):
    
    idestcur=int(peticion.GET.get('idestcur'))
    idagen=int(peticion.GET.get('idagen'))
    user = peticion.user
    grupos = get_grupos(user)
    name = 'Estudios Cursados'
    form_old = ''
    accion = ''
    
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
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          b = Estudiocursado()
          b.idagente = a
          form = formEstudiosCursados(instance=b)
          
      else:
        form = formEstudiosCursados()
    return render_to_response('appPersonal/forms/abm.html',{'form': form,'name':name,'grupos':grupos, 'user':user}, )

    
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
      else:
          form = formArticulos()

      return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'grupos':grupos, 'user':user}, )

    
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
    
    
    
@login_required(login_url='login')
def abmMedica(peticion):
    
    user = peticion.user
    grupos = get_grupos(user)
    idagen = int(peticion.GET.get('idagente'))
    idmed = int(peticion.GET.get('idmedica'))
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
	      form.fields['idausent'].widget.attrs['enabled'] = 'enabled'
	      form.instance.agente = Agente.objects.get(pk=idagen)
	      form.instance.idausent = Ausent.objects.get(pk=idausent)
	      form.save()
	      if accion == 'Alta':
	          registrar(user,name,accion,getTime(),None,modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      elif accion == 'Modificacion':
	          registrar(user, name, accion, getTime(), form_old, modeloLista(form.Meta.model.objects.filter(pk=form.instance.pk).values_list()))
	      
	      url = "listado/listadoxagente/medica?idagente='+str(idagen)+'&borrado=-1&idausent='+str(idausent)"
	      return HttpResponseRedirect(url)
    else:
      if int(idmed) > 0 and int(idagen)> 0:
        a = Medica.objects.get(pk=idmed)
        form = formMedica(instance=a)
      elif int(idagen) > 0:          
          a = Agente.objects.get(pk=idagen)
          aus = Ausent.objects.get(pk=idausent)
          b = Medica()
          b.agente = a
          b.idausent = aus
          form = formMedica(instance=b)
      else:
        form = formMedica()
      
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'user':user, 'grupos':grupos},)
    

@login_required(login_url='login')
def abmJuntaMedica(peticion,idjm, idmed, idagen):
    
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
            else:
              form = formMedicavieja()
          except ValueError:
            form = formMedicavieja()
	
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'user':user, 'grupos':grupos}, )

@login_required(login_url='login')
def abmLicenciaanualvieja(peticion):
  
    user = peticion.user
    name = 'Licencia'
    idagente = str(peticion.GET.get('idagente'))
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
    return render_to_response('appPersonal/forms/abm.html',{'form': form, 'name':name, 'user':user, 'grupos':grupos}, )

