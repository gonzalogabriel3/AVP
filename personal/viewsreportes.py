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
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from personal.funciones import *
from django.db.models import Q

from personal.views import *

import datetime
from datetime import datetime, timedelta, date
import xlwt


def fechaEnRango(anio,mes,fi,ff):
    """
    Este metodo en funcion del mes arma una lista con todos los dias del mes, para luego tomar uno a uno cada uno de ellos
    y comprar si se encuentra en el intervalo dado por fechainicio (fi) y fechafin (ff). Utiliza el metodo diasMes tomado de 
    funciones.py. Luego suma la cantidad de insasitencias que ocurrieron en un mes, en caso de no existir retorna 0.
    """
    rango = list()
    cant = 0;
    for i in range(1,diasMes(anio,mes)+1):
        rango.append(date(anio, mes, i))
    
    for r in rango:
        if fi <= r <=ff:
        	cant = cant+1  
    return cant

    
@login_required
def ausRepLicenciasPendientes_excel(peticion):
	
	user = peticion.user
	
	cantMensual = 0
	
	book = xlwt.Workbook(encoding='utf8')
	
	sheet = book.add_sheet('Reporte Licencias')
	
	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
		
	licencias = Licenciaanualagente.objects.filter(resta__exact=True).order_by('idagente__idzona','idagente__iddireccion','idagente__apellido','idagente__nombres','anio')
				
	i = 0
	sheet.write(i, 0, 'Nombre y Apellido', style=default_style)
	sheet.write(i, 1, 'Legajo', style=default_style)
	sheet.write(i, 2, 'Año', style=default_style)
	sheet.write(i, 3, 'Cant. Dias', style=default_style)
	sheet.write(i, 4, 'Dias Tomados', style=date_style)
	sheet.write(i, 5, 'Zona', style=default_style)
	sheet.write(i, 6, 'Dirección', style=date_style)
	
	for a in licencias:
	    i = i + 1
	    
	    nombres = a.idagente.nombres
	    #sincodnombres = nombres.encode('ascii','ignore')
	    sincodnombres = str(nombres)
	    apellido = a.idagente.apellido
	    #sincodapellido = apellido.encode('ascii','ignore')
	    sincodapellido = str(apellido)

	    nombre = sincodapellido+", "+sincodnombres
	    
	    sheet.write(i, 0, nombre, style=default_style)
	    sheet.write(i, 1, a.idagente.nrolegajo, style=default_style)
	    sheet.write(i, 2, a.anio, style=default_style)
	    sheet.write(i, 3, a.cantidaddias, style=default_style)
	    sheet.write(i, 4, a.diastomados, style=default_style)
	    try:
	    	sheet.write(i, 5, a.idagente.idzona.descripcion, style=default_style)
	    except:
	    	sheet.write(i, 5, "", style=default_style)
	    sheet.write(i, 6, a.idagente.iddireccion.descripcion, style=default_style)
	    

	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Licencia_excel.xls'
	book.save(response)
	return response
	
    
@login_required
def ausRepMensualCMO_excel(peticion):
	
	user = peticion.user
	
	mes = int(peticion.GET.get('mes'))
	anio = int(peticion.GET.get('anio'))
	
	cantMensual = 0
	
	book = xlwt.Workbook(encoding='utf8')
	
	sheet = book.add_sheet('Ausentismo Mensual Falta CMO')
	
	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
		
		
	ausentismos = Ausent.objects.filter(Q(idarticulo__exact=1011) | Q(idarticulo__exact=1021) | Q(idarticulo__exact=1811))
			
	i = 0
	sheet.write(i, 0, 'Apellido y Nombres', style=default_style)
	sheet.write(i, 1, 'Documento', style=default_style)
	sheet.write(i, 2, 'Articulo', style=default_style)
	sheet.write(i, 3, 'Desde', style=date_style)
	sheet.write(i, 4, 'Hasta', style=default_style)
	sheet.write(i, 5, 'Domicilio', style=default_style)
	sheet.write(i, 6, 'Localidad', style=default_style)
	
	for a in ausentismos:
	    cant = fechaEnRango(anio,mes,a.fechainicio,a.fechafin)
	    if cant !=0 :
	    	agente = Agente.objects.get(idagente__exact=a.idagente.pk)

	    	if ((int(agente.codigopostal.idcodpos == 2)) or (int(agente.codigopostal.idcodpos) == 3)):
			    nombres = agente.nombres
			    sincodnombres = nombres.encode('ascii','ignore')
			    
			    apellido = agente.apellido
			    sincodapellido = apellido.encode('ascii','ignore')
			    
			    nombre = sincodapellido+", "+sincodnombres
			    
			    i = i + 1
			    sheet.write(i, 0, nombre, style=default_style)
			    sheet.write(i, 1, agente.nrodocumento, style=default_style)
			    sheet.write(i, 2, a.idarticulo.descripcion, style=default_style)
			    sheet.write(i, 3, a.fechainicio, style=date_style)
			    sheet.write(i, 4, a.fechafin, style=date_style)
			    sheet.write(i, 5, agente.domicilio, style=default_style)
			    sheet.write(i, 6, agente.codigopostal.descripcion, style=default_style)

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=ausRepMensualCMO_'+str(mes)+"-"+str(anio)+'_excel.xls'
	book.save(response)
	return response
	

@login_required
def ausRepMensual_excel(peticion):
	
	user = peticion.user
	
	mes = int(peticion.GET.get('mes'))
	anio = int(peticion.GET.get('anio'))
	
	cantMensual = 0
	
	book = xlwt.Workbook(encoding='utf8')
	
	sheet = book.add_sheet('Ausentismo Reporte Mensual')
	
	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
	
	
	listaAus = list()
	
	if permisoEstadistica(user):
	    return HttpResponseRedirect('/personal/error/')
	    
	aus = Ausent.objects.all()
	for a in aus:
	    cant = fechaEnRango(anio,mes,a.fechainicio,a.fechafin)
	    if cant !=0 :
	    	agente = a.idagente.apellido +' '+ a.idagente.nombres

	    	if a.idarticulo.pk==3:
	    		try:
	    			articulo = a.idarticulo.descripcion + " - " +a.tiempolltarde.strftime("%H:%M:%S")
	    		except AttributeError:
	    			articulo = a.idarticulo.descripcion + " "
    		else:
    			articulo = a.idarticulo.descripcion
	listaAus.append((agente,cant,articulo,a.fechainicio,a.fechafin))
	
	listexcel = sorted(listaAus, key=lambda agen: agen[0])
	
	i = 0
	sheet.write(i, 0, 'Agente', style=default_style)
	sheet.write(i, 1, 'Cantidad Faltas', style=default_style)
	sheet.write(i, 2, 'Artículo', style=default_style)
	sheet.write(i, 3, 'Fecha Inicio', style=default_style)
	sheet.write(i, 4, 'Fecha Fin', style=default_style)
	
	for le in listexcel:
	    i = i + 1
	    sheet.write(i, 0, le[0], style=default_style)
	    sheet.write(i, 1, le[1], style=default_style)
	    sheet.write(i, 2, le[2], style=default_style)
	    sheet.write(i, 3, le[3], style=date_style)
	    sheet.write(i, 4, le[4], style=date_style)
		
	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=ausRepMensual_'+str(mes)+"-"+str(anio)+'_excel.xls'
	book.save(response)
	return response


@login_required
def ingopcsalidasmesagentes_excel(peticion):
	
	user = peticion.user
		
	return render_to_response('appPersonal/reports/ingopcsalidasmesagentes_excel.html',{'user':user,},)
		
		
@login_required
def salidasmesagentes_excel(peticion):
	
	user = peticion.user
	
	mes = int(peticion.GET.get('mes'))
	anio = int(peticion.GET.get('anio'))
	nombremes = peticion.GET.get('nombremes')
	
	    
	
	book = xlwt.Workbook(encoding='utf8')
	
	sheet = book.add_sheet('Salidas Agentes Mes')
	
	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
	
	salidasaux = Salida.objects.all()
	
	salidas = list()
	
	i = 0
	sheet.write(i, 0, 'Apellido', style=default_style)
	sheet.write(i, 1, 'Nombres', style=default_style)
	sheet.write(i, 2, 'DNI', style=default_style)
	sheet.write(i, 3, 'Fecha', style=date_style)
	sheet.write(i, 4, 'Hora Salida', style=default_style)
	sheet.write(i, 5, 'Hora Regreso', style=default_style)
	sheet.write(i, 6, 'Tipo Salida', style=default_style)
	sheet.write(i, 7, 'Observaciones', style=default_style)
		
	
	for s in salidasaux:
	    fecha = s.fecha
	    n = str(fecha).split("-");
	    numanio = n[0];
	    nummes = n[1];
	    
	    if (int(numanio) == anio):
	    	if (int(nummes) == mes): 
	    		agente = Agente.objects.get(idagente__exact=s.idagente.pk)
	    		if (s.oficial == "TRUE"):
	    			tiposalida = "Oficial"
	    		else:
	    			tiposalida = "No oficial"
	    			i = i + 1
	    			sheet.write(i, 0, agente.apellido, style=default_style)
	    			sheet.write(i, 1, agente.nombres, style=default_style)
	    			sheet.write(i, 2, agente.nrodocumento, style=default_style)
	    			sheet.write(i, 3, s.fecha, style=date_style)
	    			sheet.write(i, 4, s.horasalida, style=default_style)
	    			sheet.write(i, 5, s.horaregreso, style=default_style)
	    			sheet.write(i, 6, tiposalida, style=default_style)
	    			sheet.write(i, 7, s.observaciones, style=default_style)
	
	'''
	sheet.write(i+1, 4, ventames, style=default_style)
	sheet.write(i+1, 6, comision, style=default_style)
	sheet.write(i+1, 7, cobro, style=default_style)
	'''
		
	
	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=salidasmes_'+nombremes+str(anio)+'_excel.xls'
	book.save(response)
	return response

	
@login_required
def ingopcsalidasanioagente_excel(peticion):
	
	user = peticion.user
	
	agentes = Agente.objects.all().order_by('apellido')
			
	return render_to_response('appPersonal/reports/ingopcsalidasanioagente_excel.html',{'agentes':agentes,'user':user,},)	

	
@login_required
def salidasanioagente_excel(peticion):
	
	user = peticion.user
	
	agente = int(peticion.GET.get('idagente'))
	anio = int(peticion.GET.get('anio'))
	
	
	book = xlwt.Workbook(encoding='utf8')
	
	sheet = book.add_sheet('Salida Agente Año')
	
	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
	
		
	salidasaux = Salida.objects.filter(idagente__exact=agente)
		
	salidas = list()
	
	agente = Agente.objects.get(idagente__exact=agente)
	        
	nombres = agente.nombres
	sincodnombres = nombres.encode('ascii','ignore')
    
	apellido = agente.apellido
	sincodapellido = apellido.encode('ascii','ignore')
    
	nombreag = sincodapellido+","+sincodnombres
	
	i = 0
	sheet.write(i, 0, 'Agente:', style=default_style)
	sheet.write(i, 1, nombreag, style=default_style)
	
	i = 1
	sheet.write(i, 0, 'DNI:', style=default_style)
	sheet.write(i, 1, agente.nrodocumento, style=default_style)
	
	
	i = 3
	sheet.write(i, 0, 'Fecha', style=default_style)
	sheet.write(i, 1, 'Hora Salida', style=default_style)
	sheet.write(i, 2, 'Hora Regreso', style=default_style)
	sheet.write(i, 3, 'Tipo Salida', style=default_style)
	sheet.write(i, 4, 'Observaciones', style=default_style)
	
	for s in salidasaux:
	    fecha = s.fecha
	    n = str(fecha).split("-");
	    numanio = n[0];
	  	    
	    if (int(numanio) == anio):
	    	if (s.oficial == "TRUE"):
	    		tiposalida = "Oficial"
	    	else:
	    		tiposalida = "No oficial"
	    		i = i + 1
	    		sheet.write(i, 0, s.fecha, style=date_style)
	    		sheet.write(i, 1, s.horasalida, style=default_style)
	    		sheet.write(i, 2,  s.horaregreso, style=default_style)
	    		sheet.write(i, 3, tiposalida, style=default_style)
	    		sheet.write(i, 4, s.observaciones, style=default_style)
	
	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=salidasmes_'+sincodapellido+'_'+str(anio)+'_excel.xls'
	book.save(response)
	return response


	

def agentes_excel(request):
  
    book = xlwt.Workbook(encoding='utf8')
	
    sheet = book.add_sheet('Agentes')
    
    default_style = xlwt.Style.default_style
    datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
    date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
  
    lists = Agente.objects.all().values_list()
    
    i = 0
    sheet.write(i, 0, 'ID', style=datetime_style)
    sheet.write(i, 1, 'Nro. Legajo', style=default_style)
    sheet.write(i, 2, 'Apellido', style=default_style)
    sheet.write(i, 3, 'Nombres', style=default_style)
    sheet.write(i, 4, 'Tipo Doc.', style=default_style)
    sheet.write(i, 5, 'Nro. Doc.', style=default_style)
    sheet.write(i, 6, 'Sexo', style=default_style)
    sheet.write(i, 7, 'Fecha Nacimiento', style=default_style)
    sheet.write(i, 8, 'Nacionalidad', style=default_style)
    sheet.write(i, 9, 'Estado Civil', style=default_style)
    sheet.write(i, 10, 'Cod. Postal', style=default_style)
    sheet.write(i, 11, 'Domicilio', style=default_style)
    sheet.write(i, 12, 'Telefono', style=default_style)
    sheet.write(i, 13, 'Fecha Alta', style=default_style)
    sheet.write(i, 14, 'Cargo', style=default_style)
    sheet.write(i, 15, 'Antigraños', style=default_style)
    sheet.write(i, 16, 'Antigrmeses', style=default_style)
    sheet.write(i, 17, 'Antigrvaños', style=default_style)
    sheet.write(i, 18, 'Antigrvmeses', style=default_style)
    sheet.write(i, 19, 'Antigravpaños', style=default_style)
    sheet.write(i, 20, 'Antigravpmeses', style=default_style)
    sheet.write(i, 21, 'Situacion', style=default_style)
    sheet.write(i, 22, 'Fecha Baja', style=default_style)
    sheet.write(i, 23, 'Razon Baja', style=default_style)
    sheet.write(i, 24, 'Clase', style=default_style)
    sheet.write(i, 25, 'Categoria', style=default_style)
    sheet.write(i, 26, 'Titulo', style=default_style)
    sheet.write(i, 27, 'Planta', style=default_style)
    sheet.write(i, 28, 'Agrupamiento', style=default_style)
    sheet.write(i, 29, 'Id direccion', style=default_style)
    sheet.write(i, 30, 'Id direccion real', style=default_style)
    sheet.write(i, 31, 'Nro. Cuenta', style=default_style)
    sheet.write(i, 32, 'Nro. Contrado', style=default_style)
    sheet.write(i, 33, 'Nro. LegajoSueldos', style=default_style)
    sheet.write(i, 34, 'Observaciones', style=default_style)
    sheet.write(i, 35, 'Total 102', style=default_style)
    sheet.write(i, 36, 'Seccion', style=default_style)
    sheet.write(i, 37, 'Dexc', style=default_style)
    sheet.write(i, 38, 'DeFun', style=default_style)
    sheet.write(i, 39, 'Funcion', style=default_style)
    sheet.write(i, 40, 'Id Zona', style=default_style)
    sheet.write(i, 41, 'Id ZonaReal', style=default_style)
    sheet.write(i, 42, 'ClaseAc', style=default_style)
    
    #sheet.write(i, 27, 'Sucursal', style=default_style)
        
    
    for row, rowdata in enumerate(lists):
    	for col, val in enumerate(rowdata):
    		if isinstance(val, datetime):
    			style = datetime_style
    		elif isinstance(val, date):
    			style = date_style
    		else:
    			style = default_style
    			sheet.write(row+1, col, val, style=style)
    
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=agentes_excel.xls'
    book.save(response)
    return response
    
    
@login_required
def ingfechapartdiarioausent_excel(peticion):
	
	user = peticion.user
	
	return render_to_response('appPersonal/ingfechapartdiarioausent_excel.html',{'user':user,},)
    
    

def partdiarioaus_excel(peticion):
    
    #fechain = peticion.GET.get('fechain')
    
    anio = int(peticion.GET.get('anio'))
    mes = int(peticion.GET.get('mes'))
    dia = int(peticion.GET.get('dia'))
    
    book = xlwt.Workbook(encoding='utf8')
	
    sheet = book.add_sheet('Parte Diario Ausentismo')
    
    default_style = xlwt.Style.default_style
    datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
    date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
    
    #ausentismos = Ausent.objects.filter(fecha__range=(fechainicio, fechafin)).filter(iddeposito__exact=posiciondepo)
    ausentismos = Ausent.objects.filter(Q(idarticulo=18) | Q(idarticulo=101) | Q(idarticulo=102) | Q(idarticulo=1011) | Q(idarticulo=1021) | Q(idarticulo=1811) | Q(idarticulo=103) | Q(idarticulo=181) )
    
    lista = list()
    
    i = 0
    sheet.write(i, 0, 'Apellido y Nombres', style=default_style)
    sheet.write(i, 1, 'Documento', style=default_style)
    sheet.write(i, 2, 'Articulo', style=default_style)
    sheet.write(i, 3, 'Desde', style=date_style)
    sheet.write(i, 4, 'Hasta', style=default_style)
    sheet.write(i, 5, 'Domicilio', style=default_style)
    sheet.write(i, 6, 'Localidad', style=default_style)
    
    for a in ausentismos:
    	if (analizaFechaRango(a.fechainicio,date(anio, mes, dia),a.fechafin)):
    		agente = Agente.objects.get(idagente__exact=a.idagente.pk)

    		if ((int(agente.codigopostal.idcodpos == 2)) or (int(agente.codigopostal.idcodpos) == 3)):
    			nombres = agente.nombres
    			sincodnombres = nombres.encode('ascii','ignore')
    			apellido = agente.apellido
    			sincodapellido = apellido.encode('ascii','ignore')
    			nombre = sincodapellido+", "+sincodnombres
    			i = i + 1
    			sheet.write(i, 0, nombre, style=default_style)
    			sheet.write(i, 1, agente.nrodocumento, style=default_style)
    			sheet.write(i, 2, a.idarticulo.descripcion, style=default_style)
    			sheet.write(i, 3, a.fechainicio, style=date_style)
    			sheet.write(i, 4, a.fechafin, style=date_style)
    			sheet.write(i, 5, agente.domicilio, style=default_style)
    			sheet.write(i, 6, agente.codigopostal.descripcion, style=default_style)

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=partdiarioaus_'+str(dia)+'-'+str(mes)+'-'+str(anio)+'_excel.xls'
    book.save(response)
    return response
