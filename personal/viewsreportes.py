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
from weasyprint import HTML
import tempfile

#Metodo que obtiene los nombres de los campos de un modelo,los retorna en una lista
def obtenerNombreCampos(nombreModelo):
	#Obtengo el modelo
	modelo=getattr(sys.modules[__name__], nombreModelo)

	listaCampos=list()

	for campo in modelo._meta.fields:
		#Valido que no se guarde el campo de primary key del modelo
		if(campo.verbose_name!=modelo._meta.pk.name):
			listaCampos.append(campo.verbose_name)

	
	return listaCampos

#Metodo que obtiene los valores de uno/varios objetos y los devuelve en una lista
def obtenerValoresDeObjeto(objetos):

	listObjetos=list()

	for objeto in objetos:
			listaValores=list()
			for campo in objeto._meta.fields:
				#Obtengo el nombre del campo
				name=campo.name
				#Obtengo el valor del campo
				valor=getattr(objeto, name)
				
				#Verifico que no se cargue el id del objeto para mostrar 
				if(valor!=objeto.pk):
					if(valor==None or valor==''):
						listaValores.append("-")
					else:
						listaValores.append(str(valor))
			
			listObjetos.append(listaValores)

	return listObjetos

#Metodo que lista los valores de uno o varios objetos y lo retorna en formato PDF
def generarPDF(peticion,titulo,listaCampos,listaValores):
	#Obtengo la fecha actual para asignarla al nombre del pdf
	fecha=datetime.now()
	fecha=fecha.strftime("%d/%m/%Y")	

	#Renderizo la vista que sera devuelta
	html_string = render_to_string('appPersonal/reports/reportePDF.html', {'listaValores':listaValores,'listaCampos':listaCampos,'titulo':titulo,'fecha':fecha})
	#Agrego el 'base_url' para poder cargar imagenes en el pdf
	html = HTML(string=html_string,base_url=peticion.build_absolute_uri())
	result = html.write_pdf()
	#Indico el tipo de contenido en la respuesta,en este caso un PDF
	response = HttpResponse(content_type='application/pdf;')
	#Indico el nombre del nuevo pdf
	response['Content-Disposition'] = 'inline; filename=Reporte.pdf'
	response['Content-Transfer-Encoding'] = 'binary'
	#Creo un archivo temporal que va a contener el PDF generado
	with tempfile.NamedTemporaryFile(delete=True) as output:
		output.write(result)
		output.flush()
		output = open(output.name, 'rb')
		response.write(output.read())

	return response

def PDFausentismo(peticion):
	idagente=peticion.GET.get('idagente')
	ausentismos=Ausent.objects.filter(idagente=idagente).all()
	listaCampos=obtenerNombreCampos("Ausent")
	listaValores=obtenerValoresDeObjeto(ausentismos)

	return generarPDF(peticion,"Reporte de ausentismo",listaCampos,listaValores)

def salidasAgenteAñoPDF(peticion):
	idagente=peticion.GET.get('idagente')
	anio=peticion.GET.get('anio')
	salidas=Salida.objects.filter(idagente=idagente).all()

	listaCampos=obtenerNombreCampos("Salida")
	listaValores=obtenerValoresDeObjeto(salidas)

	return generarPDF(peticion,"Reporte de salidas",listaCampos,listaValores)

#Metodo que devuelve las licencias acumuladas de un agente,en un archivo en formato "pdf"
def repLicenciasAcumuladasPDF(peticion):
	idagente=peticion.GET.get('idagente')
	licencias=Licenciaanualagente.objects.filter(idagente=idagente)
	agente=Agente.objects.get(idagente=idagente)
	
	#Obtengo la fecha actual para asignarla al nombre del pdf
	fecha=datetime.now()
	fecha=fecha.strftime("%d/%m/%Y")
	
	#Renderizo la vista que sera devuelta
	html_string = render_to_string('appPersonal/reports/licenciasAcumuladas.html', {'licencias': licencias,'agente':agente,'fecha':fecha})
	#Agrego el 'base_url' para poder cargar imagenes en el pdf
	html = HTML(string=html_string,base_url=peticion.build_absolute_uri())
	result = html.write_pdf()
	#Indico el tipo de contenido en la respuesta,en este caso un PDF
	response = HttpResponse(content_type='application/pdf;')
	#Indico el nombre del nuevo pdf
	response['Content-Disposition'] = 'inline; filename=Licencias acumuladas de '+str(agente.apellido)+' '+str(agente.nombres)+'.pdf'
	response['Content-Transfer-Encoding'] = 'binary'

	#Creo un archivo temporal que va a contener el PDF generado
	with tempfile.NamedTemporaryFile(delete=True) as output:
		output.write(result)
		output.flush()
		output = open(output.name, 'rb')
		response.write(output.read())

	return response

def ausentismoExcel(peticion):
	idagente=peticion.GET.get('idagente')
	agente=Agente.objects.get(idagente=idagente)
	ausentismos=Ausent.objects.filter(idagente=idagente).all()
	listaCampos=obtenerNombreCampos("Ausent")
	listaValores=obtenerValoresDeObjeto(ausentismos)

	return generarExcel(peticion,"Reporte de ausentismo",listaCampos,listaValores)

def generarExcel(peticion,titulo,listaCampos,listaValores):

	book = xlwt.Workbook(encoding='utf8')

	sheet = book.add_sheet(str(titulo))
	
	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

	#Escribo los nombres de los campos
	i=0
	for nomCampo in listaCampos:
		sheet.write(0, i, nomCampo, style=default_style)
		i+=1

	j=1
	for objetos in listaValores:
		i=0
		for valor in objetos:
			sheet.write(j, i, valor, style=default_style)
			i+=1
		j+=1

	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename='+str(titulo)+'.xls'
	book.save(response)
	return response

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

def hojaAus(book,descrip):
	sheet = book.add_sheet(descrip, cell_overwrite_ok=True)
	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
	sheet.write(0, 0, 'Apellido y Nombres', style=default_style)
	sheet.write(0, 1, 'Documento', style=default_style)
	sheet.write(0, 2, 'Articulo', style=default_style)
	sheet.write(0, 3, 'Desde', style=date_style)
	sheet.write(0, 4, 'Hasta', style=default_style)
	sheet.write(0, 5, 'Domicilio', style=default_style)
	sheet.write(0, 6, 'Localidad', style=default_style)
	return sheet

def ausEnMes(a,mes,anio):
	if a.fechainicio.year == anio:
		if a.fechainicio.month <= mes <= a.fechafin.month:
			return True
		else:
			return False
	elif (a.fechainicio.year == anio-1) and (a.fechafin.year==anio):
		if a.fechafin.month >= mes:
			return True
		else:
			return False



#Metodo que devuelve las licencias acumuladas de un agente,en un archivo en formato "word"
@csrf_exempt
def repLicenciasAcumuladasWord(peticion):
	idagente=peticion.GET.get('idagente')
	agente=Agente.objects.get(idagente=idagente)
	licencias=Licenciaanualagente.objects.filter(idagente=idagente)

	book = xlwt.Workbook(encoding='utf8')

	sheet = book.add_sheet('Licencias acumuladas')
	
	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
	
	#Fila-Columna
	i = 0
	sheet.write(0, 0, 'Agente', style=default_style)
	sheet.write(0, 1, 'N° Legajo', style=default_style)
	sheet.write(1,0,agente.apellido+" "+agente.nombres, style=default_style)
	sheet.write(1,1,agente.nrolegajo, style=default_style)

	sheet.write(3,0,"Licencias acumuladas", style=default_style)
	sheet.write(4,0,"Año", style=default_style)
	sheet.write(4,1,"Dias disponibles", style=default_style)
	sheet.write(4,2,"Dias tomados", style=default_style)
	
	j=5
	for licencia in licencias:
		sheet.write(j,0,licencia.anio, style=default_style)
		sheet.write(j,1,licencia.cantidaddias, style=default_style)
		sheet.write(j,2,licencia.diastomados, style=default_style)
		j+=1

	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Licencias_acumuladas_'+str(agente.apellido)+' '+str(agente.nombres)+'.xls'
	book.save(response)
	return response
  
@login_required
def ausRepLicenciasPendientes_excel(peticion):
	
	user = peticion.user
	
	cantMensual = 0
	
	book = xlwt.Workbook(encoding='utf8')
	
	sheet = book.add_sheet('Reporte Licencias')
	
	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
		
	licencias = Licenciaanualagente.objects.filter(Q(resta__exact=True,idagente__situacion=2)).order_by('idagente__idzona','idagente__iddireccion','idagente__apellido','idagente__nombres','anio')
				
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
	    try:
	    	sheet.write(i, 6, a.idagente.iddireccion.descripcion, style=default_style)
	    except:
	    	sheet.write(i, 6, "", style=default_style)
	    
	    

	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Licencia_excel.xls'
	book.save(response)
	return response
	
    
@login_required
def ausRepMensualCMO_excel(peticion):
	user = peticion.user
	mes = int(peticion.GET.get('mes'))
	anio = int(peticion.GET.get('anio'))
	book = xlwt.Workbook(encoding='utf8')
	default_style = xlwt.Style.default_style
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
	cantMensual = 0
	ausentismos = Ausent.objects.filter(Q(idarticulo__exact=1011) | Q(idarticulo__exact=1021) | Q(idarticulo__exact=1811))
	i = 0
	sheet = hojaAus(book,"Ausentismo Falta CMO")
	for a in ausentismos:
	    cant = fechaEnRango(anio,mes,a.fechainicio,a.fechafin)
	    if cant !=0 :
	    	agente = Agente.objects.get(idagente__exact=a.idagente.pk)
	    	#if ((int(agente.codigopostal.idcodpos == 2)) or (int(agente.codigopostal.idcodpos) == 3)):
	    	if ausEnMes(a,mes,anio):
			    nombres = agente.nombres
			    apellido = agente.apellido
			    nombre = apellido+", "+nombres
			    i = i + 1
			    sheet.write(i, 0, nombre, style=default_style)
			    sheet.write(i, 1, agente.nrodocumento, style=default_style)
			    sheet.write(i, 2, a.idarticulo.descripcion, style=default_style)
			    sheet.write(i, 3, a.fechainicio, style=date_style)
			    sheet.write(i, 4, a.fechafin, style=date_style)
			    sheet.write(i, 5, agente.domicilio, style=default_style)
			    sheet.write(i, 6, agente.codigopostal.descripcion, style=default_style)

	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=ausRepMensualCMO_'+str(mes)+"-"+str(anio)+'_excel.xls'
	book.save(response)
	return response

@login_required
def ausRepMensualGrem_excel(peticion):
	user = peticion.user
	mes = int(peticion.GET.get('mes'))
	anio = int(peticion.GET.get('anio'))
	book = xlwt.Workbook(encoding='utf8')
	default_style = xlwt.Style.default_style
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
	#ausentismos = Ausent.objects.filter(Q(idarticulo__exact=37))
	ausentismos = Ausent.objects.filter(Q(idarticulo__exact=37,fechainicio__year=anio)|Q(idarticulo__exact=37,fechainicio__year=anio-1,fechafin__year=anio)).order_by('-fechainicio')
	cantMensual = 0
	i = 0
	sheet = hojaAus(book,"Ausentismo Lic GREMIAL")
	for a in ausentismos:
	    cant = fechaEnRango(anio,mes,a.fechainicio,a.fechafin)
	    if cant !=0 :
	    	agente = Agente.objects.get(idagente__exact=a.idagente.pk)
	    	#if ((int(agente.codigopostal.idcodpos == 2)) or (int(agente.codigopostal.idcodpos) == 3)):
	    	if ausEnMes(a,mes,anio):
			    nombres = agente.nombres
			    apellido = agente.apellido
			    nombre = apellido+", "+nombres
			    i = i + 1
			    sheet.write(i, 0, nombre, style=default_style)
			    sheet.write(i, 1, agente.nrodocumento, style=default_style)
			    sheet.write(i, 2, a.idarticulo.descripcion, style=default_style)
			    sheet.write(i, 3, a.fechainicio, style=date_style)
			    sheet.write(i, 4, a.fechafin, style=date_style)
			    sheet.write(i, 5, agente.domicilio, style=default_style)
			    sheet.write(i, 6, agente.codigopostal.descripcion, style=default_style)

	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=ausRepMensualGremial_'+str(mes)+"-"+str(anio)+'_excel.xls'
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
	    		agente = Agente.objects.get(idagente=s.idagente.pk)
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
		
	
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=salidasmes_'+str(nombremes)+str(anio)+'_excel.xls'
	book.save(response)
	return response

	
#@login_required
def ingopcsalidasanioagente_excel(peticion):
	
	user = peticion.user
	
	agentes = Agente.objects.all().order_by('apellido')
			
	return render_to_response('appPersonal/reports/ingopcsalidasanioagente_excel.html',{'agentes':agentes,'user':user,},)	

	
#@login_required
def salidasanioagente_excel(peticion):
	
	user = peticion.user
	
	agente = int(peticion.GET.get('idagente'))
	anio = int(peticion.GET.get('anio'))
	
	
	book = xlwt.Workbook(encoding='utf8')
	
	sheet = book.add_sheet('Salida Agente Año')
	
	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
	
		
	salidasaux = Salida.objects.filter(idagente=agente)
		
	salidas = list()
	
	agente = Agente.objects.get(idagente=agente)
	        
	nombres = agente.nombres
	
	apellido = agente.apellido
	
	
	nombreag= str(agente.apellido)+","+str(agente.nombres)
	
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
	
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=salidasmes_'+str(apellido)+'_'+str(anio)+'_excel.xls'
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
    
    
#@login_required
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

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=partdiarioaus_'+str(dia)+'-'+str(mes)+'-'+str(anio)+'_excel.xls'
    book.save(response)
    return response
