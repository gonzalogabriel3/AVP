# -*- coding: utf-8 -*-

#IMPORTS PARA PDF
#====================================================

#import ho.pisa as pisa #esto hay que bajarlo de internet, se puede instalar con easy install - http://pypi.python.org/pypi/pisa/
#import cStringIO as StringIO
import cgi
from django.template import RequestContext, Template, Context
from django.template.loader import *
from django.http import HttpResponse
from datetime import *

#====================================================
from depoapp.models import *
import psycopg2
from django.shortcuts import render_to_response
#===================================================
from django import http
#from django.core.context_processors import csrf #para formularios
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
#from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from depoapp.filtrodepositos import *
from datetime import date

from django.http import HttpResponse
#from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
#from reportlab.lib import colors
#from reportlab.platypus import Image
#from reportlab.platypus import Spacer
import os
#from reportlab.lib.pagesizes import letter,inch,A4,landscape
#from reportlab.pdfgen import canvas
#from reportlab.lib.units import mm
#from reportlab.platypus.paragraph import Paragraph 
#from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import operator
#from reportlab.pdfbase import pdfmetrics

from operator import itemgetter


#============================================================================================
# LISTADOS
#===========================================================================================
"""
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        #add page info to each page (page x of y)
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(280*mm, 5*mm,
            "Page %d of %d" % (self._pageNumber, page_count))
"""
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////		
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            

def generar_pdf_fecha(html,nomb,fecha):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()

    pisa.CreatePDF(html,result)
#    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    response = HttpResponse(result.getvalue(), mimetype ='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+nomb+'-'+str(fecha)+'.pdf'
    return response
    #if not pdf.err:
     #   return HttpResponse(result.getvalue(), mimetype ='application/pdf')
    #return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////		
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////    


#=======================================================
# GRAFICO COMBUSTIBLES
#=======================================================

@login_required
def graficocombustibles(peticion):
	
	#c={}
	#c.update(csrf(peticion))
	
	global fechainit
	fechainit = peticion.GET.get('desde')
	
	global fechafin
	fechafin = peticion.GET.get('hasta')
	
	global nronota
	nronota = str(peticion.GET.get('nronota'))
	
	global sexo
	sexo = peticion.GET.get('sexo')
	
	global nombre
	nombre = peticion.GET.get('nombre')
	  
	global cargo
	cargo = peticion.GET.get('cargo')   
		
	aux = obtenerUsuario(peticion.user)
	
	posiciondepo = peticion.GET.get('posiciondepo')
	
	opcion = obtenerUsuario(peticion.user)
	user = peticion.user
	
	artctapatrimonial = Articulo.objects.filter(Q(idarticulo__exact=10474) | Q(idarticulo__exact=10502) | Q(idarticulo__exact=10513) | Q(idarticulo__exact=10485) | Q(idarticulo__exact=10487) | Q(idarticulo__exact=10497) | Q(idarticulo__exact=10477))
	
	listexistencia = list()
	
	for a in artctapatrimonial:
		listartaux = Articulodeposito.objects.filter(idarticulo__exact=a.idarticulo).filter(iddeposito__exact=posiciondepo)
		listartauxcompleta = Articulodeposito.objects.filter(idarticulo__exact=a.idarticulo)
		listartauxcons = MovArt.objects.filter(idarticulo__exact=a.idarticulo).filter( Q(descripcion__exact="Salida") | Q(descripcion__exact="T. Salida") ).filter(deposito__exact=posiciondepo)

		cantidadex = 0
		for b in listartaux:
			cantidadex = cantidadex + b.stock

		cantidadexesq = 0
		cantidadexgm = 0
		cantidadexrw = 0
		cantidadextrv = 0
		cantidadexsrm = 0
		cantidadexmad = 0
		for d in listartauxcompleta:
			if (d.iddeposito == 1):
				cantidadexsrm = cantidadexsrm + d.stock
			if (d.iddeposito == 2):
				cantidadexmad = cantidadexmad + d.stock
			if (d.iddeposito == 3):
				cantidadexesq = cantidadexesq + d.stock
			if (d.iddeposito == 4):
				cantidadexgm = cantidadexgm + d.stock
			if (d.iddeposito == 5):
				cantidadexrw = cantidadexrw + d.stock
			if (d.iddeposito == 6):
				cantidadextrv = cantidadextrv + d.stock

		cantidadcons = 0
		for c in listartauxcons:
			cantidadcons = cantidadcons + c.cantidad

		for bm in listartaux:
			cantidadexmad = cantidadexmad + bm.stock

		#listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex]) 	

		if (int(posiciondepo) == 1):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm, cantidadexrw,cantidadextrv, cantidadexmad])
		if (int(posiciondepo) == 2):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm, cantidadexrw,cantidadextrv, cantidadexsrm])
		if (int(posiciondepo) == 3):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexgm, cantidadexrw,cantidadextrv, cantidadexsrm, cantidadexmad])
		if (int(posiciondepo) == 4):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq, cantidadexrw,cantidadextrv, cantidadexsrm, cantidadexmad])
		if (int(posiciondepo) == 5):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm,cantidadextrv, cantidadexsrm, cantidadexmad])
		if (int(posiciondepo) == 6):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm, cantidadexrw, cantidadexsrm, cantidadexmad])
	
	return render_to_response('graficocombustibles.html',{'listexistencia':listexistencia,'opcion':opcion,'user':user,},)


#=======================================================
# INGRESO OPCIONES LISTADO DE STOCK ACTUAL PARA UN DEPOSITO
#=======================================================

@login_required
def ingopcliststockactual(peticion):
	datos = list(Cuentaspatrimoniales.objects.all())
	
	opcion = obtenerUsuario(peticion.user)
	
	user = peticion.user
	
	return render_to_response('ingopcliststockactual.html',{'datos':datos,'opcion':opcion,'user':user,},)
	

#=======================================================
# LISTADO DE STOCK ACTUAL PARA UN DEPOSITO
#=======================================================
"""
@login_required
def stockactualdepo(peticion):
    c={}
    c.update(csrf(peticion))
             
    user = peticion.user
    
    
    # Obtencion de datos Json
    pdfon = int(peticion.GET.get('pdf'))
    opcion = int(peticion.GET.get('dato')) #nro cuenta patrimonial
    opciondepo = int(peticion.GET.get('opciondepo'))
     
    # --------------------------------------------------------------------------------------------- 
    
    # Filtro de datos desde la BD a traves de los modelos de django
    # Opciondepo = deposito seleccionado a traves del usuario admin.
    if (opciondepo == 0):
	nombredep = Deposito.objects.all()
	artdeposito = ArticuloDepositoAd.objects.filter(nrocuentapatrimonial__exact=opcion).order_by('idarticulo')
	
    else:
	nombredep = Deposito.objects.get(iddeposito__exact=opciondepo).direccion
	artdeposito = ArticuloDepositoAd.objects.filter(direccion__exact=nombredep,nrocuentapatrimonial__exact=opcion).order_by('idarticulo')
	    
         
    # --------------------------------------------------------------------------------------------- 
    # If pdfon = 0 genero el pdf, de ser 1 genero el listado html. 
    if pdfon == 1:
	return render_to_response('liststockactual.html',{'listdartdep':artdeposito,'opcion':opcion,'opciondepo':opciondepo,'user':user,},)
    else: 
     
	# Creamos el objeto HttpResponse con los headers apropiados para PDF.
	response = HttpResponse(mimetype='application/pdf')
	
	# Fecha actual
	fecha = date.today()
	# Armamos la Fecha para el nombre del pdf
	fechastring = str(fecha.day)+"-"+str(fecha.month)+"-"+str(fecha.year)
	fechastring2 = str(fecha.day)+"/"+str(fecha.month)+"/"+str(fecha.year)
	
	# Nombre del pdf 
	styleSheet = getSampleStyleSheet()  
	response['Content-Disposition'] = 'attachment; filename= stockactual-'+fechastring+'.pdf'

	#Creamos una lista que contendrá todos los elementos que se dibujaran en el PDF y le damos un formato predeterminado utilizando la clase <code>SimpleDocTemplate</code>
	elements = []
	doc = SimpleDocTemplate(response,pagesize=A4)
	
	# Logo de AVP para el pdf
	fichero_imagen = "../avp/media/admin/img/logo-avp.png"
	I = Image(os.path.abspath(fichero_imagen),width=107,height=42)
	
	# Informacion utilizada para la tabla superior de la cabecera del pdf. Se utiliza Paragraph para q se encuadre a la celda de la tabla.
	Pfecha = Paragraph('''
	  <para align=center spaceb=3><b>Fecha: '''+fechastring2+'''</b> </para>''',
	  styleSheet["BodyText"])
	
	Pcuenta = Paragraph('''
	  <para align=center spaceb=3><b>Cuenta Patrimonial: '''+str(opcion)+'''</b> </para>''',
	  styleSheet["BodyText"])
	
	# Definimos lo que va a contener cada celda de la Tabla Cabecera. 
	head_table=  [[ I, 'ADMINISTRACIÓN VIALIDAD PROVINCIAL',''],
	    ['', 'Reporte Listado Actual Depósito',''],
	    ['', Pcuenta,Pfecha],
	    ]
	
	# Creacion de la tabla, con el ancho de las columnas.
	th = Table(head_table,colWidths=[1.7*inch, 2.3*inch, 2*inch])
	
	# Definimos estilo de la tabla.
	th.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black),
				('SPAN',(0,2),(0,0)),
				('SPAN',(2,1),(1,1)),
				('SPAN',(2,0),(1,0)),
				('BACKGROUND',(1,0),(-1,0),colors.orange)
				
				]))
				
	# --------------------------------------------------------------------------------------------- 
	
	# Definimos lo que va a contener cada celda de la Tabla Informacion. 
	data_table = [['ID', 'Descripcion', 'Stock']] # this is the header row 
	
	# Definimos lo que va a contener la Tabla Informacion. artdeposito es la inormacion obtenida mediante los filters. el append defines el contenido para cada fila de la tabla.
	for p in artdeposito:
	    Pdesc = Paragraph('''
	  <para> Cuenta Patrimonial: '''+p.descripcionitem+'''</para>''',
	  styleSheet["BodyText"])
	    data_table.append([p.idarticulo,Pdesc,p.stock])
	
	#Le pasamos la lista con los datos a la tabla, le damos color con ayuda de la clase <code>setStyle</code>, agregamos la tabla a la lista de elementos y finalmente construimos el PDF
	t = Table(data_table, colWidths=[0.5*inch, 5*inch, 0.5*inch])
	t.setStyle(TableStyle([('GRID',(0,0),(2,artdeposito.count()),1,colors.black),
			      ('TEXTCOLOR',(0,1),(0,-1),colors.green),
			      ('BACKGROUND',(0,0),(-1,0),colors.orange),
			      ]))
	
	elements.append(th)
	elements.append(Spacer(0,20))
	elements.append(t)
	doc.build(elements,canvasmaker=NumberedCanvas)
	return response
"""	
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////		
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////   


#=======================================================
# LISTADO DE STOCK ACTUAL PARA TODOS LOS DEPOSITOS
#=======================================================
"""
@login_required
def stockactual(peticion):
    
    c={}
    c.update(csrf(peticion))
    
    # Obtencion de datos Json
    pdfon = int(peticion.GET.get('pdf'))
    opcion = int(peticion.GET.get('dato')) #nro cuenta patrimonial
    
 
    # --------------------------------------------------------------------------------------------- 
    
    # Filtro de datos desde la BD a traves de los modelos de django
    
    # Aux es el el usuario ingresado a traves del login.
    aux = obtenerUsuario(peticion.user)
     
    if (aux == 0):
	nombredep = Deposito.objects.all()
	artdeposito = ArticuloDepositoAd.objects.filter(nrocuentapatrimonial__exact=opcion).order_by('idarticulo')
      	
    else:
	nombredep = Deposito.objects.get(iddeposito__exact=aux).direccion
        artdeposito = ArticuloDepositoAd.objects.filter(direccion__exact=nombredep,nrocuentapatrimonial__exact=opcion).order_by('idarticulo')
   
    user = peticion.user

    
    # --------------------------------------------------------------------------------------------- 
    # If pdfon = 0 genero el pdf, de ser 1 genero el listado html.
    if pdfon == 1:
	return render_to_response('liststockactual.html',{'listdartdep':artdeposito,'opcion':opcion,'opciondepo':aux,'user':user,},)
    else: 
     
	# Creamos el objeto HttpResponse con los headers apropiados para PDF.
	response = HttpResponse(mimetype='application/pdf')
	
	# Fecha actual.
	fecha = date.today()
	# Armamos la Fecha para el nombre del pdf.
	fechastring = str(fecha.day)+"-"+str(fecha.month)+"-"+str(fecha.year)
	fechastring2 = str(fecha.day)+"/"+str(fecha.month)+"/"+str(fecha.year)
	
	# Nombre del PDF.
	styleSheet = getSampleStyleSheet()  
	response['Content-Disposition'] = 'attachment; filename= stockactual-'+fechastring+'.pdf'

	#Creamos una lista que contendrá todos los elementos que se dibujaran en el PDF y le damos un formato predeterminado utilizando la clase <code>SimpleDocTemplate</code>
	elements = []
	doc = SimpleDocTemplate(response,pagesize=A4)
	
	# Logo de AVP para el pdf
	fichero_imagen = "../avp/media/admin/img/logo-avp.png"
	I = Image(os.path.abspath(fichero_imagen),width=107,height=42)
	
	# Informacion utilizada para la tabla superior de la cabecera del pdf. Se utiliza Paragraph para q se encuadre a la celda de la tabla.
	Pfecha = Paragraph('''
	  <para align=center spaceb=3><b>Fecha: '''+fechastring2+'''</b> </para>''',
	  styleSheet["BodyText"])
	
	Pcuenta = Paragraph('''
	  <para align=center spaceb=3><b>Cuenta Patrimonial: '''+str(opcion)+'''</b> </para>''',
	  styleSheet["BodyText"])
	
	# Definimos lo que va a contener cada celda de la Tabla Cabecera. 
	head_table=  [[ I, 'ADMINISTRACIÓN VIALIDAD PROVINCIAL',''],
	    ['', 'Reporte Listado Actual Depósito',''],
	    ['', Pcuenta,Pfecha],
	    ]
	
	# Creacion de la tabla, con el ancho de las columnas.
	th = Table(head_table,colWidths=[1.7*inch, 2.3*inch, 2*inch])
	
	# Definimos estilo de la tabla.
	th.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black),
				('SPAN',(0,2),(0,0)),
				('SPAN',(2,1),(1,1)),
				('SPAN',(2,0),(1,0)),
				('BACKGROUND',(1,0),(-1,0),colors.orange)
				
				]))
				
	# --------------------------------------------------------------------------------------------- 
	    
	
	# Definimos lo que va a contener cada celda de la Tabla Informacion. 
	data_table = [['ID', 'Descripcion', 'Stock']] # this is the header row 
	
	# Definimos lo que va a contener la Tabla Informacion. artdeposito es la inormacion obtenida mediante los filters. el append defines el contenido para cada fila de la tabla.
	for p in artdeposito:
	    Pdesc = Paragraph('''
		    <para> Cuenta Patrimonial: '''+p.descripcionitem+'''</para>''',
		    styleSheet["BodyText"])
	    data_table.append([p.idarticulo,Pdesc,p.stock])
	
	#Le pasamos la lista con los datos a la tabla, le damos color con ayuda de la clase <code>setStyle</code>, agregamos la tabla a la lista de elementos y finalmente construimos el PDF
	t = Table(data_table, colWidths=[0.5*inch, 5*inch, 0.5*inch])
	t.setStyle(TableStyle([('GRID',(0,0),(2,artdeposito.count()),1,colors.black),
			      ('TEXTCOLOR',(0,1),(0,-1),colors.green),
			      ('BACKGROUND',(0,0),(-1,0),colors.orange),
			      ]))
	
	elements.append(th)
	elements.append(Spacer(0,20))
	elements.append(t)
	doc.build(elements,canvasmaker=NumberedCanvas)
	
	return response
"""
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////		
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#=====================================================================
# LISTADO DE STOCK QUE ESTA CON STOCK CERO (TRANSFERENCIAS - SALIDAS)
#=====================================================================

@login_required
def stockcero(peticion):
	#c={}
	#c.update(csrf(peticion))

	pdfon = int(peticion.GET.get('pdf'))

	# Aux es el el usuario ingresado a traves del login.
	aux = obtenerUsuario(peticion.user)

	if (aux != 0): # No soy el admin, solo tengo que Filtrar un deposito.
		# TRANSFERENCIAS
		# -----------------------------------------------------------
		#listtransf = list(Transferencia.objects.all())
		listtransf = list(Transferencia.objects.filter(depositosalida__exact=aux))
		listdtransf = list()
		for a in listtransf:
			listdtransfaux = list(Detalletrasferencia.objects.filter(idtransferencia__exact=a.idtransferencia)) 
			for b in listdtransfaux:
				if len(listdtransf) == 0:
					if b.deterr == "Falta Stock":
						listdtransf.append(a)

			else:
				if b.deterr == "Falta Stock":
					w = 0
					for c in listdtransf:
						if c.idtransferencia == b.idtransferencia:
							w = 1
						if w == 0:
							listdtransf.append(a)
		# SALIDAS
	    # ----------------------------------------------------------- 
		listsalidas = list(Salida.objects.all())
		listdsalidas = list()
		for a2 in listsalidas:
			listdsalidasaux = list(Detallesalida.objects.filter(idsalida__exact=a2.idsalida)) 
			for b2 in listdsalidasaux:
				if len(listdsalidas) == 0:
					if b2.deterr == "Falta Stock":
						listdsalidas.append(a2)
				else:
					if b2.deterr == "Falta Stock":
						w = 0
						for c2 in listdsalidas:
							if c2.idsalida == b2.idsalida:
								w = 1
							if w == 0:
								listdsalidas.append(a2)
		#################################################################
	else: # Soy el adimn, se trabaja con todos los elementos de la tabla.
	    # TRANSFERENCIAS ADMIN
		# -----------------------------------------------------------
		listtransf = list(Transferencia.objects.all())
		listdtransf = list()
		for a in listtransf:
			listdtransfaux = list(Detalletrasferencia.objects.filter(idtransferencia__exact=a.idtransferencia)) 
			for b in listdtransfaux:
				if len(listdtransf) == 0:
				  if b.deterr == "Falta Stock":
				    listdtransf.append(a)
				else:
					if b.deterr == "Falta Stock":
						w = 0
						for c in listdtransf:
							if c.idtransferencia == b.idtransferencia:
								w = 1
							if w == 0:
								listdtransf.append(a)
		# SALIDAS ADMIN
	    # ----------------------------------------------------------- 
		listsalidas = list(Salida.objects.all())
		listdsalidas = list()
		for a2 in listsalidas:
			listdsalidasaux = list(Detallesalida.objects.filter(idsalida__exact=a2.idsalida)) 
			for b2 in listdsalidasaux:
				if len(listdsalidas) == 0:
					if b2.deterr == "Falta Stock":
						listdsalidas.append(a2)

				else:
					if b2.deterr == "Falta Stock":
						w = 0
						for c2 in listdsalidas:
							if c2.idsalida == b2.idsalida:
								w = 1
							if w == 0:
								listdsalidas.append(a2)
		#################################################################

	user = peticion.user

	# If pdfon = 0 genero el pdf, de ser 1 genero el listado html.
	if pdfon == 1:
		return render_to_response('liststockcero.html',{'aux':aux,'listdtransf':listdtransf,'listdsalidas':listdsalidas,'user':user,},)
	else:
		# Creamos el objeto HttpResponse con los headers apropiados para PDF.
		response = HttpResponse(content_type='application/pdf')

		# Fecha para nombre archivo.
		fecha = date.today()
		fechastring = str(fecha.day)+"-"+str(fecha.month)+"-"+str(fecha.year)

		# Nombre pdf.
		styleSheet = getSampleStyleSheet()  
		response['Content-Disposition'] = 'attachment; filename= stockcero-'+fechastring+'.pdf'

		#Creamos una lista que contendrá todos los elementos que se dibujaran en el PDF y le damos un formato predeterminado utilizando la clase <code>SimpleDocTemplate</code>
		elements = []
		doc = SimpleDocTemplate(response,pagesize=A4)

		# Logo AVP pdf.
		fichero_imagen = "/var/www/avp/media/admin/img/logo-avp.png"
		I = Image(os.path.abspath(fichero_imagen),width=107,height=42)

		# Informacion utilizada para la tabla superior de la cabecera del pdf. Se utiliza Paragraph para q se encuadre a la celda de la tabla.
		Pfecha = Paragraph('''
		  <para align=center spaceb=3><b>Fecha: '''+fechastring+'''</b> </para>''',
		  styleSheet["BodyText"])

		# Definimos lo que va a contener cada celda de la Tabla Cabecera. 
		head_table=  [[ I, 'ADMINISTRACIÓN VIALIDAD PROVINCIAL',''],
		    ['', 'Reporte Listado Entradas Entre Fechas',''],
		    ['', Pfecha,''],
		    ]

		# Creacion de la tabla, con el ancho de las columnas.
		th = Table(head_table,colWidths=[1.7*inch, 2.3*inch, 2*inch])

		# Definimos estilo de la tabla.
		th.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black),
					('SPAN',(0,2),(0,0)),
					('SPAN',(2,1),(1,1)),
					('SPAN',(2,2),(1,2)),
					('SPAN',(2,0),(1,0)),
					('BACKGROUND',(1,0),(-1,0),colors.orange)
					
					]))
					
		# --------------------------------------------------------------------------------------------- 

		# TABLA SALIDAS	

		# Definimos lo que va a contener cada celda de la Tabla SALIDAS. 
		data_table = [['ID', 'Fecha', 'Destino', 'Observaciones']] # this is the header row 

		# Definimos lo que va a contener la Tabla SALIDAS. listdsalidas es la inormacion obtenida mediante los filters. el append defines el contenido para cada fila de la tabla.
		for p in listdsalidas:
		    
		    contentdest = p.destino
		    # Ignora los caracteres que desconoce, utilizado para el error de caracteres Ascii de Django.
		    sincoddest = contentdest.encode('ascii','ignore')
		    
		    Pdest = Paragraph('''
			   <para> '''+str(sincoddest)+'''</para>''',
			   styleSheet["BodyText"])
		    #---
		    contentobs = p.observaciones
		    sincodobs = contentobs.encode('ascii','ignore')
		    
		    Pobs = Paragraph('''
			   <para> '''+str(sincodobs)+'''</para>''',
			   styleSheet["BodyText"])
			   
		    data_table.append([p.idsalida,p.fecha,Pdest,Pobs])

		#Le pasamos la lista con los datos a la tabla y le damos estilo.

		t = Table(data_table, colWidths=[ 1*inch, 1.5*inch, 1.5*inch, 2*inch])
			
		t.setStyle(TableStyle([('GRID',(0,0),(3,len(listdsalidas)),1,colors.black),
				      ('TEXTCOLOR',(0,1),(0,-1),colors.green),
				      ('BACKGROUND',(0,0),(-1,0),colors.orange),
				      ]))
		      


		#################################################################

		# TABLA TRANSFERENCIAS	

		# Definimos lo que va a contener cada celda de la Tabla TRANSFERENCIAS. 
		data_table2 = [['ID', 'Fecha Salida', 'Deposito Salida']] # this is the header row 

		# Definimos lo que va a contener la Tabla TRANSFERENCIAS. listdtransf es la inormacion obtenida mediante los filters. el append defines el contenido para cada fila de la tabla.
		for p2 in listdtransf:
		    data_table2.append([p2.idtransferencia,p2.fechasalida,p2.depositosalida])


		#Le pasamos la lista con los datos a la tabla y le damos estilo.
		t2 = Table(data_table2, colWidths=[ 1*inch, 2.5*inch, 2.5*inch])
			
		t2.setStyle(TableStyle([('GRID',(0,0),(2,len(listdsalidas)),1,colors.black),
				      ('TEXTCOLOR',(0,1),(0,-1),colors.green),
				      ('BACKGROUND',(0,0),(-1,0),colors.orange),
				      ]))
			
		#################################################################

		#  Agregamos todos los elementos a la lista de elementos y finalmente construimos el PDF	
		elements.append(th)
		elements.append(Spacer(0,20))

		# Titulo tabla Salidas
		Ptit1 = Paragraph('''
			   <para> '''+"SALIDAS"+'''</para>''',
			   styleSheet["BodyText"])

		elements.append(Ptit1)
		# Tabla Salidas
		elements.append(t)
		elements.append(Spacer(0,20))

		# Titulo tabla Transferencias
		Ptit2 = Paragraph('''
			   <para> '''+"TRANSFERENCIAS"+'''</para>''',
			   styleSheet["BodyText"])

		elements.append(Ptit2)
		# Tabla Transferencias
		elements.append(t2)
		# Construimos el PDF.
		doc.build(elements,canvasmaker=NumberedCanvas)

	return response	
    
    
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////		
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ==================================================================
# INGRESO OPCIONES EGRESOS 
# ==================================================================

@login_required
def ingopclistegresos(peticion):
	datos = list(Cuentaspatrimoniales.objects.all())
	allorigdest = list(MovArt.objects.all())
	origdestaux = list()
	for mov in allorigdest:
		if mov.origdest not in origdestaux:
			origdestaux.append(mov.origdest)

	origdest = sorted(origdestaux)
	opcion = obtenerUsuario(peticion.user)
	user = peticion.user
	return render_to_response('ingopclistegresos.html',{'datos':datos,'opcion':opcion,'user':user,'origdest':origdest,},)


# ==================================================================
# EGRESOS 
# ==================================================================

@login_required
def listegresos(peticion):
	#c={}
	#c.update(csrf(peticion))
	destino = peticion.GET.get('destino')
	listopc = str(peticion.GET.get('listopc'))
	opciondepo = str(peticion.GET.get('opciondepo'))
	fechainit = peticion.GET.get('desde')
	fechafin = peticion.GET.get('hasta')
	pdfon = int(peticion.GET.get('pdf'))
	cta = int(peticion.GET.get('dato')) #nro cuenta patrimonial
	aux = obtenerUsuario(peticion.user)

	if (aux != 0):
		if (destino == "Ninguno"):
			if (cta != 0):
				salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") ).filter(deposito__exact=aux).filter(nrocuentapatrimonial__exact=cta)
				tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") ).filter(deposito__exact=aux).filter(nrocuentapatrimonial__exact=cta)
			else:
				salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") ).filter(deposito__exact=aux)
				tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") ).filter(deposito__exact=aux)
		else:
			if (cta != 0):
				salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") ).filter(deposito__exact=aux).filter(origdest__exact=destino).filter(nrocuentapatrimonial__exact=cta) #descripcion__exact="T. Salida" #descripcion__exact="T. Salida"
				tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") ).filter(deposito__exact=aux).filter(origdest__exact=destino).filter(nrocuentapatrimonial__exact=cta) #descripcion__exact="T. Salida"
			else:
				salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") ).filter(deposito__exact=aux).filter(origdest__exact=destino)
				tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") ).filter(deposito__exact=aux).filter(origdest__exact=destino)

	else:
		if (opciondepo == "0"):
			if (destino == "Ninguno"):
				if (cta != 0):
					salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") ).filter(nrocuentapatrimonial__exact=cta)
					tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") ).filter(nrocuentapatrimonial__exact=cta)
				else:
					salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") )
					tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") )
			else:
				if (cta != 0):  
					salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") ).filter(origdest__exact=destino).filter(nrocuentapatrimonial__exact=cta) #descripcion__exact="T. Salida"
					tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") ).filter(origdest__exact=destino).filter(nrocuentapatrimonial__exact=cta) #descripcion__exact="T. Salida"
				else:
					salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") ).filter(origdest__exact=destino) #descripcion__exact="T. Salida"
					tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") ).filter(origdest__exact=destino) #descripcion__exact="T. Salida"
		else:
			if (destino == "Ninguno"):
				if (cta != 0):
					salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") ).filter(nrocuentapatrimonial__exact=cta).filter(deposito__exact=opciondepo)
					tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") ).filter(nrocuentapatrimonial__exact=cta).filter(deposito__exact=opciondepo)
				else:
					salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") ).filter(deposito__exact=opciondepo)
					tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") ).filter(deposito__exact=opciondepo)
			else:
				if (cta != 0):  
					salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") ).filter(origdest__exact=destino).filter(nrocuentapatrimonial__exact=cta).filter(deposito__exact=opciondepo) #descripcion__exact="T. Salida"
					tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") ).filter(origdest__exact=destino).filter(nrocuentapatrimonial__exact=cta).filter(deposito__exact=opciondepo) #descripcion__exact="T. Salida"
				else:
					salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") ).filter(origdest__exact=destino).filter(deposito__exact=opciondepo) #descripcion__exact="T. Salida"
					tsalidaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Salida") ).filter(origdest__exact=destino).filter(deposito__exact=opciondepo) #descripcion__exact="T. Salida"

	listdettransf = list()
	for t in tsalidaaux:
		taux = Transferencia.objects.get(idtransferencia__exact=t.idaccion)
		listdettransf.append([taux.entrega, taux.recibe, taux.confirmado])
	#entrega - recibe - confirmado
	
	listdetsalida = list()
	for s in salidartaux:
		tsal = Salida.objects.get(idsalida__exact=s.idaccion)
		listdetsalida.append([tsal.entregadoa, tsal.observaciones])
      
    # Lista de transferencia Final
	listfintsalida = list()
	for tsf in zip(tsalidaaux,listdettransf):
		listfintsalida.append(tsf)
	
    #Lista de salidas final	
	listfinsalida = list()
	for ts in zip(salidartaux,listdetsalida):	
		listfinsalida.append(ts)

    # listfintsalida[1] para ver una posicion	
    
    # Ordenar Listas (lista a ordenar, campo a ordenar, si reverse = true mayor a menor)
	if (listopc == "Fecha"):
		listfintsalida = sorted(listfintsalida, key=lambda x: (x[0].fecha))
		listfinsalida = sorted(listfinsalida, key=lambda x: (x[0].fecha))
	else:
		if (listopc == "Mayor-Menor Cantidad"):  
			listfintsalida = sorted(listfintsalida, key=lambda x: (x[0].cantidad),reverse=True)
			listfinsalida = sorted(listfinsalida, key=lambda x: (x[0].cantidad),reverse=True)
		else:
			if (listopc == "Menor-Mayor Cantidad"):
				listfintsalida = sorted(listfintsalida, key=lambda x: (x[0].cantidad))
				listfinsalida = sorted(listfinsalida, key=lambda x: (x[0].cantidad))
			else:
				if (listopc == "Articulo"):
					listfintsalida = sorted(listfintsalida, key=lambda x: (x[0].descripcionitem))
					listfinsalida = sorted(listfinsalida, key=lambda x: (x[0].descripcionitem))
				else:
					if (listopc == "Destino"):
						listfintsalida = sorted(listfintsalida, key=lambda x: (x[0].destino))
						listfinsalida = sorted(listfinsalida, key=lambda x: (x[0].destino))  
					else:
						if (listopc == "Cuenta Patrimonial"):
							listfintentrada = sorted(listfintentrada, key=lambda x: (x[0].nrocuentapatrimonial))
							listfincompra = sorted(listfincompra, key=lambda x: (x[0].nrocuentapatrimonial))
						else:
							listfintsalida = listfintsalida
							listfinsalida = listfinsalida

	if (listopc == "Fecha"):
		salidart = salidartaux.extra(order_by = ['fecha'])
	else:
		if (listopc == "Articulo"):
			salidart = salidartaux.extra(order_by = ['idarticulo__descripcionitem'])
		else:
			if (listopc == "Menor-Mayor Cantidad"):
				salidart = salidartaux.extra(order_by = ['cantidad'])
			else:
				if (listopc == "Mayor-Menor Cantidad"):
					salidart = salidartaux.extra(order_by = ['-cantidad'])
				else:  
					if (listopc == "Destino"):
						salidart = salidartaux.extra(order_by = ['origdest'])
					else:
						salidart = salidartaux

	user = peticion.user
	if pdfon == 1:
		#return render_to_response('listsalidadestino.html',{'listopc':listopc,'salidart':salidart,'user':user, 'fechainit':peticion.GET.get('desde'), 'fechafin':peticion.GET.get('hasta'),},)
		return render_to_response('listegresos.html',{'aux':aux,'listopc':listopc,'opciondepo':opciondepo,'destino':destino,'listfintsalida':listfintsalida,'opcion':cta,'listfinsalida':listfinsalida,'user':user, 'fechainit':peticion.GET.get('desde'), 'fechafin':peticion.GET.get('hasta'),},)
	else: 
		# Creamos el objeto HttpResponse con los headers apropiados para PDF.
		response = HttpResponse(content_type='application/pdf')
		fecha = date.today()
		fechastring = str(fecha.day)+"-"+str(fecha.month)+"-"+str(fecha.year)
		styleSheet = getSampleStyleSheet()  
		response['Content-Disposition'] = 'attachment; filename= stockegresos-'+fechastring+'.pdf'

		#Creamos una lista que contendrá todos los elementos que se dibujaran en el PDF y le damos un formato predeterminado utilizando la clase <code>SimpleDocTemplate</code>
		elements = []
		
		#landscape se utiliza para generar una hoja horizontal	
		doc = SimpleDocTemplate(response,topMargin=2,botMargin=2,pagesize=landscape(A4))
		fichero_imagen = "/var/www/avp/media/admin/img/logo-avp.png"
		I = Image(os.path.abspath(fichero_imagen),width=107,height=42)
		Pfecha = Paragraph('''
		  <para align=center spaceb=3><b>Fecha Hasta: '''+str(fechafin)+'''</b> </para>''',
		  styleSheet["BodyText"])
		Pcuenta = Paragraph('''
		  <para align=center spaceb=3><b>Fecha Desde: '''+str(fechainit)+'''</b> </para>''',
		  styleSheet["BodyText"])
		head_table=  [[ I, 'ADMINISTRACIÓN VIALIDAD PROVINCIAL',''],
		    ['', 'Reporte Listado Salidas y T.Salidas Entre Fechas',''],
		    ['', Pcuenta,Pfecha],
		    ]
		th = Table(head_table,colWidths=[1.7*inch, 4.3*inch, 4*inch])
		th.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black),
					('SPAN',(0,2),(0,0)),
					('SPAN',(2,1),(1,1)),
					('SPAN',(2,0),(1,0)),
					('BACKGROUND',(1,0),(-1,0),colors.orange)
					
					]))
		# --------------------------------------------------------------------------------------------- 
		    
		#Extraemos la información de la base de datos
		
		#SALIDAS
		tit1 = Paragraph('''
			   <para> '''+"SALIDAS"+'''</para>''',
			   styleSheet["BodyText"])
		
		data_table = [['Cta.Patrim.','Articulo', 'Fecha', 'Cantidad', 'Orig-Dest','Entregado A','Observaciones']] # this is the header row 
		
		for p in listfinsalida:
			Part2 = Paragraph('''
		  <para> '''+str(p[0].idarticulo)+'''</para>''',
		  styleSheet["BodyText"])
			Porigdest2 = Paragraph('''
		  <para> '''+p[0].origdest+'''</para>''',
		  styleSheet["BodyText"])
			Pobs2 = Paragraph('''
		  <para> '''+p[1][1]+'''</para>''',
		  styleSheet["BodyText"])
			data_table.append([p[0].nrocuentapatrimonial,Part2,p[0].fecha,p[0].cantidad,Porigdest2, p[1][0], Pobs2 ])
		
		#Le pasamos la lista con los datos a la tabla, le damos color con ayuda de la clase <code>setStyle</code>, agregamos la tabla a la lista de elementos y finalmente construimos el PDF
		
		t = Table(data_table, colWidths=[ 0.8*inch,2*inch, 1*inch, 0.8*inch , 1.4*inch, 2.0*inch, 2*inch])
		t.setStyle(TableStyle([('GRID',(0,0),(6,salidartaux.count()),1,colors.black),
				      ('TEXTCOLOR',(0,1),(0,-1),colors.green),
				      ('BACKGROUND',(0,0),(-1,0),colors.orange),
				      ]))
					      
		# T.SALIDAS
		tit2 = Paragraph('''
			   <para> '''+"TRANSFERENCIAS SALIDAS"+'''</para>''',
			   styleSheet["BodyText"])
			
		data_table = [['Cta.Patrim.','Articulo', 'Fecha', 'Cantidad', 'Orig-Dest','Entrega','Recibe','Confirmado']] # this is the header row 
		
		for p2 in listfintsalida:
			Part22 = Paragraph('''
		  <para> '''+str(p[0].idarticulo)+'''</para>''',
		  styleSheet["BodyText"])
			Porigdest22 = Paragraph('''
		  <para> '''+str(p[0].origdest)+'''</para>''',
		  styleSheet["BodyText"])
			Pentrega = Paragraph('''
		  <para> '''+ p2[1][0] +'''</para>''',
		  styleSheet["BodyText"])
			Precibe = Paragraph('''
		  <para> '''+ str(p2[1][1])  +'''</para>''',
		  styleSheet["BodyText"])
			data_table.append([p[0].nrocuentapatrimonial, Part22,p2[0].fecha,p2[0].cantidad,Porigdest22, Pentrega, Precibe, p2[1][2] ])
		
		#Le pasamos la lista con los datos a la tabla, le damos color con ayuda de la clase <code>setStyle</code>, agregamos la tabla a la lista de elementos y finalmente construimos el PDF
		
		t2 = Table(data_table, colWidths=[ 0.8*inch, 2.6*inch, 1*inch, 0.8*inch , 1.8*inch, 1*inch, 1*inch, 1*inch])
		t2.setStyle(TableStyle([('GRID',(0,0),(7,tsalidaaux.count()),1,colors.black),
				      ('TEXTCOLOR',(0,1),(0,-1),colors.green),
				      ('BACKGROUND',(0,0),(-1,0),colors.orange),
				      ]))
		
		#('ALIGN',(0,0),(-1,-1),'CENTER')
		
		elements.append(th)
		elements.append(Spacer(0,20))
		elements.append(tit1)
		elements.append(t)
		elements.append(Spacer(0,10))
		elements.append(tit2)
		elements.append(t2)		
		doc.build(elements,canvasmaker=NumberedCanvas)
		return response	
    
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////		
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ==================================================================
# INGRESO OPCIONES LISTADO INGRESOS
# ==================================================================

@login_required
def ingopclistingresos(peticion):
	datos = list(Cuentaspatrimoniales.objects.all())
	allorigdest = list(MovArt.objects.all())
	origdestaux = list()
	for mov in allorigdest:
		if mov.origdest not in origdestaux:
			origdestaux.append(mov.origdest)
	origdest = sorted(origdestaux)
	opcion = obtenerUsuario(peticion.user)
	user = peticion.user
	return render_to_response('ingopclistingresos.html',{'datos':datos,'opcion':opcion,'user':user,'origdest':origdest,},)
	
# ==================================================================
# LISTADO INGRESOS
# ==================================================================
	
@login_required
def listingresos(peticion):
	#c={}
	#c.update(csrf(peticion))
	listopc = str(peticion.GET.get('listopc'))
	opciondepo = str(peticion.GET.get('opciondepo'))
	fechainit = peticion.GET.get('desde')
	fechafin = peticion.GET.get('hasta')
	pdfon = int(peticion.GET.get('pdf'))
	cta = int(peticion.GET.get('dato')) #nro cuenta patrimonial
	aux = obtenerUsuario(peticion.user)
	if (aux != 0): # No soy el ADMIN
		if (cta == 0):
			#salidartaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Salida") | Q(descripcion__exact="T. Salida") ).filter(deposito__exact=aux)
			compraaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Compra") ).filter(deposito__exact=aux)
			tentradaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Entrada") ).filter(deposito__exact=aux)
		else:
			compraaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Compra") ).filter(deposito__exact=aux).filter(nrocuentapatrimonial__exact=cta)
			tentradaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Entrada") ).filter(deposito__exact=aux).filter(nrocuentapatrimonial__exact=cta)
	else: #Soy el ADMIN
		if (opciondepo == "0"): #No hay deposito seleccionado en select de ingopclistingresos
			if (cta == 0):
				compraaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Compra") )
				tentradaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Entrada") )
			else:
				compraaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Compra") ).filter(nrocuentapatrimonial__exact=cta)
				tentradaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Entrada") ).filter(nrocuentapatrimonial__exact=cta)
		else:
			if (cta == 0):
				compraaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Compra") ).filter(deposito__exact=opciondepo)
				tentradaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Entrada") ).filter(deposito__exact=opciondepo)
			else:
				compraaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="Compra") ).filter(deposito__exact=opciondepo).filter(nrocuentapatrimonial__exact=cta)
				tentradaaux = MovArt.objects.filter(fecha__range=(fechainit, fechafin)).filter( Q(descripcion__exact="T. Entrada") ).filter(deposito__exact=opciondepo).filter(nrocuentapatrimonial__exact=cta)

	listdettransf = list()
	for t in tentradaaux:
		taux = Transferencia.objects.get(idtransferencia__exact=t.idaccion)
		listdettransf.append([taux.entrega, taux.recibe, taux.confirmado])
	#entrega - recibe - confirmado
	
	listdetcompra = list()
	for s in compraaux:
		tent = Compra.objects.get(idcompra__exact=s.idaccion)
		listdetcompra.append([tent.nroremito, tent.nroordencompra, tent.nroexpediente, tent.observaciones])
	#entregadoa - observaciones
    
    # Se puede probar map(list.__add__, L1, L2)
    
    # Lista de transferencia Final
	listfintentrada = list()
	for tsf in zip(tentradaaux,listdettransf):	
		listfintentrada.append(tsf)
	
    #Lista de salidas final	
	listfincompra = list()
	for ts in zip(compraaux,listdetcompra):	
		listfincompra.append(ts)

    # listfintsalida[1] para ver una posicion	
   
	if (listopc == "Fecha"):
		listfintentrada = sorted(listfintentrada, key=lambda x: (x[0].fecha))
		listfincompra = sorted(listfincompra, key=lambda x: (x[0].fecha))
	else:
		if (listopc == "Mayor-Menor Cantidad"):  
			listfintentrada = sorted(listfintentrada, key=lambda x: (x[0].cantidad),reverse=True)
			listfincompra = sorted(listfincompra, key=lambda x: (x[0].cantidad),reverse=True)
		else:
			if (listopc == "Menor-Mayor Cantidad"):
				listfintentrada = sorted(listfintentrada, key=lambda x: (x[0].cantidad))
				listfincompra = sorted(listfincompra, key=lambda x: (x[0].cantidad))
			else:
				if (listopc == "Articulo"):
					listfintentrada = sorted(listfintentrada, key=lambda x: (x[0].descripcionitem))
					listfincompra = sorted(listfincompra, key=lambda x: (x[0].descripcionitem))
				else:
					if (listopc == "Cuenta Patrimonial"):
						listfintentrada = sorted(listfintentrada, key=lambda x: (x[0].nrocuentapatrimonial))
						listfincompra = sorted(listfincompra, key=lambda x: (x[0].nrocuentapatrimonial))
					else:		     
						listfintentrada = listfintentrada
						listfincompra = listfincompra
	user = peticion.user
	if pdfon == 1:
		#return render_to_response('listsalidadestino.html',{'listopc':listopc,'salidart':salidart,'user':user, 'fechainit':peticion.GET.get('desde'), 'fechafin':peticion.GET.get('hasta'),},)
		return render_to_response('listingresos.html',{'aux':aux,'listopc':listopc,'opciondepo':opciondepo,'listfintentrada':listfintentrada,'opcion':cta,'listfincompra':listfincompra,'user':user, 'fechainit':peticion.GET.get('desde'), 'fechafin':peticion.GET.get('hasta'),},)
	else: 
		# Creamos el objeto HttpResponse con los headers apropiados para PDF.
		response = HttpResponse(content_type='application/pdf')
		
		fecha = date.today()
		fechastring = str(fecha.day)+"-"+str(fecha.month)+"-"+str(fecha.year)
		
		styleSheet = getSampleStyleSheet()  
		response['Content-Disposition'] = 'attachment; filename= stockingresos-'+fechastring+'.pdf'

		#Creamos una lista que contendrá todos los elementos que se dibujaran en el PDF y le damos un formato predeterminado utilizando la clase <code>SimpleDocTemplate</code>
		elements = []
		
		#landscape se utiliza para generar una hoja horizontal	
		doc = SimpleDocTemplate(response,topMargin=2,bottomMargin=2,pagesize=landscape(A4))
		fichero_imagen = "/var/www/avp/media/admin/img/logo-avp.png"
		I = Image(os.path.abspath(fichero_imagen),width=107,height=42)
		
		Pfecha = Paragraph('''
		  <para align=center spaceb=3><b>Fecha Hasta: '''+str(fechafin)+'''</b> </para>''',
		  styleSheet["BodyText"])
		
		Pcuenta = Paragraph('''
		  <para align=center spaceb=3><b>Fecha Desde: '''+str(fechainit)+'''</b> </para>''',
		  styleSheet["BodyText"])
		
		
		head_table=  [[ I, 'ADMINISTRACIÓN VIALIDAD PROVINCIAL',''],
		    ['', 'Reporte Listado Compras y T.Entrada Entre Fechas',''],
		    ['', Pcuenta,Pfecha],
		    ]
		
		th = Table(head_table,colWidths=[1.7*inch, 4.3*inch, 4*inch])
		
		th.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black),
					('SPAN',(0,2),(0,0)),
					('SPAN',(2,1),(1,1)),
					('SPAN',(2,0),(1,0)),
					('BACKGROUND',(1,0),(-1,0),colors.orange)
					
					]))
					
		# --------------------------------------------------------------------------------------------- 
		    
		#Extraemos la información de la base de datos
		
		#Compras
		tit1 = Paragraph('''
			   <para> '''+"COMPRAS"+'''</para>''',
			   styleSheet["BodyText"])
		
		
		
		data_table = [['Cta.Patrim.','Articulo', 'Fecha', 'Cantidad','Orig-Dest','Remito','Orden', 'Exp.','Obs.']] # this is the header row 
		
		anchorows = []
		
		anchorows.append(0.2*inch)
		
		for p in listfincompra:
			Part2 = Paragraph('''
		  	<para> '''+str(p[0].idarticulo)+'''</para>''',
		  	styleSheet["BodyText"])
			Porigdest2 = Paragraph('''
		  	<para> '''+p[0].origdest+'''</para>''',
		  	styleSheet["BodyText"])
		    
			Premito2 = Paragraph('''
		  	<para> '''+str(chunk_split(p[1][0],12))+'''</para>''',
		  	styleSheet["BodyText"])
			Pobs2 = Paragraph('''
			<para> '''+str(chunk_split(p[1][3],12))+'''</para>''',
			styleSheet["BodyText"])
			data_table.append([p[0].nrocuentapatrimonial,Part2,p[0].fecha,p[0].cantidad,Porigdest2, Premito2, p[1][1],p[1][2],Pobs2 ])

		#Le pasamos la lista con los datos a la tabla, le damos color con ayuda de la clase <code>setStyle</code>, agregamos la tabla a la lista de elementos y finalmente construimos el PDF
		t = Table(data_table, colWidths=[ 0.8*inch, 2*inch, 1*inch, 0.8*inch, 1.4*inch , 1.4*inch, 0.8*inch , 0.8*inch,  2.1*inch])
		t.setStyle(TableStyle([('GRID',(0,0),(9,compraaux.count()),1,colors.black),
				      ('TEXTCOLOR',(0,1),(0,-1),colors.green),
				      ('BACKGROUND',(0,0),(-1,0),colors.orange),
				      ]))
					      
		# T.ENTRADAS
		tit2 = Paragraph('''
			   <para> '''+"TRANSFERENCIAS ENTRADAS"+'''</para>''',
			   styleSheet["BodyText"])
			
		data_table = [['Cta.Patrim.','Articulo', 'Fecha', 'Cantidad', 'Orig-Dest','Entrega','Recibe','Confirmado']] # this is the header row 
		
		for p2 in listfintentrada:
			Part22 = Paragraph('''
		  	<para> '''+str(p[0].idarticulo)+'''</para>''',
		  	styleSheet["BodyText"])
			Porigdest22 = Paragraph('''
		  	<para> '''+str(p[0].origdest)+'''</para>''',
			styleSheet["BodyText"])
			Pentrega = Paragraph('''
			<para> '''+ str(p2[1][0]) +'''</para>''',
			styleSheet["BodyText"])
			Precibe = Paragraph('''
			<para> '''+ str(p2[1][1])  +'''</para>''',
			styleSheet["BodyText"])
			data_table.append([p[0].nrocuentapatrimonial,Part22,p2[0].fecha,p2[0].cantidad,p2[0].origdest,Porigdest22, Pentrega, Precibe, p2[1][2] ])

		#Le pasamos la lista con los datos a la tabla, le damos color con ayuda de la clase <code>setStyle</code>, agregamos la tabla a la lista de elementos y finalmente construimos el PDF
		t2 = Table(data_table, colWidths=[ 0.8*inch, 2.6*inch, 1*inch, 0.8*inch , 1*inch, 1.4*inch, 1.4*inch, 1*inch])
		t2.setStyle(TableStyle([('GRID',(0,0),(8,tentradaaux.count()),1,colors.black),
				      ('TEXTCOLOR',(0,1),(0,-1),colors.green),
				      ('BACKGROUND',(0,0),(-1,0),colors.orange),
				      ]))
		elements.append(th)
		elements.append(Spacer(0,20))
		elements.append(tit1)
		elements.append(t)
		elements.append(Spacer(0,10))
		elements.append(tit2)
		elements.append(t2)
		doc.build(elements,canvasmaker=NumberedCanvas)
		return response	
    
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////		
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ==================================================================
# INGRESO OPCIONES LISTADO INGRESOS
# ==================================================================

@login_required
def ingopccombustibles(peticion):
	opcion = obtenerUsuario(peticion.user)
	user = peticion.user
	return render_to_response('ingopccombustibles.html',{'opcion':opcion,'user':user,},)
	
# ==================================================================
# METODO MYFIRSTPAGE QUE ESTABLECE EL ESTILO DE LA PRIMER PAGINA
# ==================================================================

def myFirstPage(canvas, doc):
	canvas.saveState()
	canvas.setFont('Times-Roman', 6)
	canvas.drawString(53,798,'REPÚBLICA ARGENTINA')
	canvas.setFont('Times-Roman', 5)
	canvas.drawString(62,793,'Provincia del CHUBUT')
	canvas.setFont('Times-Bold', 6)
	canvas.drawString(45,784,'MINISTERIO DE ECONOMIA,')
	canvas.setFont('Times-Bold', 6)
	canvas.drawString(55,777,'Y CREDITO PÚBLICOS')
	canvas.setFont('Times-BoldItalic', 10)
	canvas.drawString(31,768,'Administracion de Vialidad')
	canvas.setFont('Times-BoldItalic', 10)
	canvas.drawString(66,759,'Provincial')
	imagen = "/var/www/avp/media/img/logochubut.png"
	canvas.drawInlineImage(os.path.abspath(imagen), 300,760,width=50,height=48)
	fecha = date.today()
	dia = str(fecha.day)
	mes = str(fecha.month)
	   
	if mes == "1":
		nombremes = "Enero"
	if mes == "2":
		nombremes = "Febrero"
	if mes == "3":
		nombremes = "Marzo"
	if mes == "4":
		nombremes = "Abril"
	if mes == "5":
		nombremes = "Mayo"
	if mes == "6":
		nombremes = "Junio"
	if mes == "7":
		nombremes = "Julio"
	elif mes == "8":
		nombremes = "Agosto"
	elif mes == "9":
		nombremes = "Septiembre"
	if mes == "10":
		nombremes = "Octubre"
	if mes == "11":
		nombremes = "Junio"
	if mes == "12":
		nombremes = "Junio"

	anio = str(fecha.year)
	canvas.setFont('Times-Bold', 10)
	canvas.drawString(300,745,nombredepoactual.upper()+', '+dia+' de '+nombremes+' del '+anio+'.-')
	canvas.setFont('Helvetica-Bold', 12)
	canvas.drawString(25,720,'NOTA N° '+nronota+' '+nombredepoactual)
	canvas.setFont('Helvetica', 8)
	canvas.drawString(25,700,sexo)
	canvas.setFont('Helvetica', 8)
	canvas.drawString(25,690,cargo)
	canvas.setFont('Helvetica', 8)
	canvas.drawString(25,680,nombre)
	canvas.setFont('Helvetica-Bold', 8)
	canvas.drawString(25,670,"S______/______D.-")
	canvas.setFont('Helvetica-Bold', 8)
	canvas.drawString(265,660,"REF:")
	canvas.setFont('Helvetica', 8)
	canvas.drawString(284,660,"S/Elevación movimiento Combustibles y Lubricantes")
	canvas.setFont('Helvetica', 8)
	canvas.drawString(265,650,"correspondiente entre las fechas, ")
	canvas.setFont('Helvetica-Bold', 8)
	canvas.drawString(388,650,str(fechainit))
	canvas.setFont('Helvetica', 8)
	canvas.drawString(430,650," y ")
	canvas.setFont('Helvetica-Bold', 8)
	canvas.drawString(440,650,str(fechafin))
	canvas.setFont('Helvetica', 8)
	canvas.drawString(287,640,"Elevo a Ud. para su conociemiento, movimiento")
	canvas.setFont('Helvetica', 8)
	canvas.drawString(25,630,"de Combustibles y Lubricantes segun el siguiente detalle:")
	canvas.restoreState()

# ==================================================================
# METODO CHUNK_SPLIT DIVIDE LA CADENA EN NUMERO ESPECIFICO
# ==================================================================

def chunk_split(body,chunklen=76,end="\r\n"):
	data = ""
	for i in range(0,len(body),chunklen):
		data += body[i:min(i+chunklen,len(body))] + end
	return data	
	
	
# ==================================================================
# LISTADO COMBUSTIBLES
# ==================================================================
	
@login_required
def listcombustibles(peticion):
	#c={}
	#c.update(csrf(peticion))
	global fechainit
	fechainit = peticion.GET.get('desde')
	global fechafin
	fechafin = peticion.GET.get('hasta')
	global nronota
	nronota = str(peticion.GET.get('nronota'))
	global sexo
	sexo = peticion.GET.get('sexo')
	global nombre
	nombre = peticion.GET.get('nombre')
	global cargo
	cargo = peticion.GET.get('cargo')   
	excel = int(peticion.GET.get('excel'))
	aux = obtenerUsuario(peticion.user)
	global posiciondepo
	ingresos = list()
	if (aux != 0): # No soy el ADMIN
		detcompra = Detallecompra.objects.filter(Q(idarticulo__exact=10474) | Q(idarticulo__exact=10502))
		for dc in detcompra:
			compra = Compra.objects.filter(idcompra__exact=dc.idcompra).filter(fecha__range=(fechainit, fechafin)).filter(iddeposito__exact=aux)
			if (dc.idarticulo == 10474):
				articulo = "Gas Oil"
			else:
				articulo = "Nafta"
				ingresos.append([compra.nroremito, compra.nroordencompra ,compra.nroexpediente,compra.nroactuacion,compra.idproveedor, articulo, dc.cantidad, dc.preciounitario, compra.fecha])
	
	#ingresos = Compra.objects.filter(fecha__range=(fechainit, fechafin)).filter(iddeposito__exact=aux)
	#artctapatrimonial = Articulo.objects.filter(nrocuentapatrimonial__exact=21203)
	artctapatrimonial = Articulo.objects.filter(Q(idarticulo__exact=10474) | Q(idarticulo__exact=10502) | Q(idarticulo__exact=10513) | Q(idarticulo__exact=10485) | Q(idarticulo__exact=10487) | Q(idarticulo__exact=10497) | Q(idarticulo__exact=10477))
	listexistencia = list()

	for a in artctapatrimonial:
		listartaux = Articulodeposito.objects.filter(idarticulo__exact=a.idarticulo).filter(iddeposito__exact=aux)
		listartauxcompleta = Articulodeposito.objects.filter(idarticulo__exact=a.idarticulo)
		listartauxcons = MovArt.objects.filter(idarticulo__exact=a.idarticulo).filter( Q(descripcion__exact="Salida") | Q(descripcion__exact="T. Salida") ).filter(deposito__exact=aux)
		cantidadex = 0
		for b in listartaux:
			cantidadex = cantidadex + b.stock

		cantidadexesq = 0
		cantidadexgm = 0
		cantidadexrw = 0
		cantidadextrv = 0
		cantidadexsrm = 0
		cantidadexmad = 0
		for d in listartauxcompleta:
			if (d.iddeposito == 1):
			    cantidadexsrm = cantidadexsrm + d.stock
			if (d.iddeposito == 2):
			    cantidadexmad = cantidadexmad + d.stock
			if (d.iddeposito == 3):
			    cantidadexesq = cantidadexesq + d.stock
			if (d.iddeposito == 4):
			    cantidadexgm = cantidadexgm + d.stock
			if (d.iddeposito == 5):
			    cantidadexrw = cantidadexrw + d.stock
			if (d.iddeposito == 6):
			    cantidadextrv = cantidadextrv + d.stock

		cantidadcons = 0
		for c in listartauxcons:
			cantidadcons = cantidadcons + c.cantidad

		for bm in listartaux:
			cantidadexmad = cantidadexmad + bm.stock

	    #listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex]) 	
	    
		if (aux == 1):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm, cantidadexrw,cantidadextrv, cantidadexmad])
		if (aux == 2):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm, cantidadexrw,cantidadextrv, cantidadexsrm])
		if (aux == 3):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexgm, cantidadexrw,cantidadextrv, cantidadexsrm, cantidadexmad])
		if (aux == 4):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq, cantidadexrw,cantidadextrv, cantidadexsrm, cantidadexmad])
		if (aux == 5):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm,cantidadextrv, cantidadexsrm, cantidadexmad])
		if (aux == 6):
			listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm, cantidadexrw, cantidadexsrm, cantidadexmad])
	else:
	#SOY EL ADMIN!!!!!!!!!!!!!!!!!!!!!!!!!!!
		posiciondepo = peticion.GET.get('posiciondepo')
		
		detcompra = Detallecompra.objects.filter(Q(idarticulo__exact=10474) | Q(idarticulo__exact=10502))
		for dc in detcompra:
			comp = Compra.objects.filter(idcompra__exact=dc.idcompra.pk)
			for c in comp:
				if (dc.idarticulo == 10474):
					articulo = "Gas Oil"
				else:
					articulo = "Nafta"
				ingresos.append([c.nroremito, c.nroordencompra ,c.nroexpediente,c.nroactuacion,c.idproveedor, articulo, dc.cantidad, dc.preciounitario, c.fecha])
		#ingresos = Compra.objects.filter(fecha__range=(fechainit, fechafin)).filter(iddeposito__exact=posiciondepo)
		#artctapatrimonial = Articulo.objects.filter(nrocuentapatrimonial__exact=21203)
		artctapatrimonial = Articulo.objects.filter(Q(idarticulo__exact=10474) | Q(idarticulo__exact=10502) | Q(idarticulo__exact=10513) | Q(idarticulo__exact=10485) | Q(idarticulo__exact=10487) | Q(idarticulo__exact=10497) | Q(idarticulo__exact=10477))
		listexistencia = list()
		for a in artctapatrimonial:
			listartaux = Articulodeposito.objects.filter(idarticulo__exact=a.idarticulo).filter(iddeposito__exact=posiciondepo)
			listartauxcompleta = Articulodeposito.objects.filter(idarticulo__exact=a.idarticulo)
			listartauxcons = MovArt.objects.filter(idarticulo__exact=a.idarticulo).filter( Q(descripcion__exact="Salida") | Q(descripcion__exact="T. Salida") ).filter(deposito__exact=posiciondepo)
			cantidadex = 0
			for b in listartaux:
				cantidadex = cantidadex + b.stock

			cantidadexesq = 0
			cantidadexgm = 0
			cantidadexrw = 0
			cantidadextrv = 0
			cantidadexsrm = 0
			cantidadexmad = 0
			for d in listartauxcompleta:
				if (d.iddeposito == 1):
					cantidadexsrm = cantidadexsrm + d.stock
				if (d.iddeposito == 2):
					cantidadexmad = cantidadexmad + d.stock
				if (d.iddeposito == 3):
					cantidadexesq = cantidadexesq + d.stock
				if (d.iddeposito == 4):
					cantidadexgm = cantidadexgm + d.stock
				if (d.iddeposito == 5):
					cantidadexrw = cantidadexrw + d.stock
				if (d.iddeposito == 6):
					cantidadextrv = cantidadextrv + d.stock

			cantidadcons = 0
			for c in listartauxcons:
				cantidadcons = cantidadcons + c.cantidad

			for bm in listartaux:
				cantidadexmad = cantidadexmad + bm.stock

		    #listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex]) 	

			if (int(posiciondepo) == 1):
				listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm, cantidadexrw,cantidadextrv, cantidadexmad])
			if (int(posiciondepo) == 2):
				listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm, cantidadexrw,cantidadextrv, cantidadexsrm])
			if (int(posiciondepo) == 3):
				listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexgm, cantidadexrw,cantidadextrv, cantidadexsrm, cantidadexmad])
			if (int(posiciondepo) == 4):
				listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq, cantidadexrw,cantidadextrv, cantidadexsrm, cantidadexmad])
			if (int(posiciondepo) == 5):
				listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm,cantidadextrv, cantidadexsrm, cantidadexmad])
			if (int(posiciondepo) == 6):
				listexistencia.append([a.descripcionitem, cantidadcons ,cantidadex,cantidadexesq,cantidadexgm, cantidadexrw, cantidadexsrm, cantidadexmad])
	
		fechaactual = date.today()
		fechastring = str(fechaactual.day)+"-"+str(fechaactual.month)+"-"+str(fechaactual.year)

		if excel == 1:
			# your excel html format
			template_name = "comb_excel.html"
			
			response = render_to_response(template_name, {'listexistencia': listexistencia,'ingresos': ingresos,'aux': aux,'posiciondepo':int(posiciondepo)})
			
			# this is the output file
			filename = "comb_"+fechastring+".csv"

			response['Content-Disposition'] = 'attachment; filename='+filename
			response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
			return response    
		else: 
			# Creamos el objeto HttpResponse con los headers apropiados para PDF.
			response = HttpResponse(content_type='application/pdf')
			styleSheet = getSampleStyleSheet()  
			response['Content-Disposition'] = 'attachment; filename= listcombustibles-'+fechastring+'.pdf'
			#Creamos una lista que contendrá todos los elementos que se dibujaran en el PDF y le damos un formato predeterminado utilizando la clase <code>SimpleDocTemplate</code>
			elements = []
			#landscape se utiliza para generar una hoja horizontal	
			doc = SimpleDocTemplate(response,leftMargin=18,rightMargin=15,topMargin=2,bottomMargin=2,pagesize=A4)
			fichero_imagen = "/var/www/avp/media/admin/img/logo-avp.png"
			I = Image(os.path.abspath(fichero_imagen),width=107,height=42)
			global nombredepoactual

			if (aux != 0):
				nombredepoactual = str(Deposito.objects.get(iddeposito__exact=aux).direccion)
			else:
				nombredepoactual = str(Deposito.objects.get(iddeposito__exact=posiciondepo).direccion)
			#nota = Paragraph('''
			#		<para> '''+"NOTA N° "+str(nronota)+" "+ nombredepo + '''</para>''',
			#		styleSheet["BodyText"])
			
			titing = Paragraph('Ingreso de Combustible', styleSheet["BodyText"])
			data_table = [['Remito', 'Ord.Compra', 'Expediente','Actuacion','Proveedor','Articulo','Cant.','Precio Unit.','Fecha']] # this is the header row 
			style = ParagraphStyle(name='Helvetica')
			style.fontSize = 8
			styleobs = ParagraphStyle(name='Helvetica')
			styleobs.fontSize = 6
			
			anchorows = []
			anchorows.append(0.15*inch) #Por cabecera
			
			for p in ingresos:
				#compra.nroremito, compra.nroordencompra ,
				#compra.nroexpediente,compra.nroactuacion,compra.idproveedor, 
				#articulo, dc.cantidad, compra.fecha,dc.preciounitario])
				content = p[0]
				sincodremito = content.encode('ascii','ignore')
				Premito = Paragraph(str(chunk_split(sincodremito,28)),style)
				#-----
				content2 = str(p[1])
				sincodorden = content2.encode('ascii','ignore')
				Pordencompra = Paragraph(str(chunk_split(sincodorden,12)),style)
				#-----
				content3 = str(p[4])
				sincodproveedor = content3.encode('ascii','ignore')
				Pproveedor = Paragraph(str(chunk_split(sincodproveedor,12)),style)
			    #-----
				if (len(str(sincodorden)) > 24 or len(str(sincodremito)) > 56 or len(str(sincodproveedor)) > 24 ):
					anchorows.append(0.45*inch)
				else:
					if (len(str(sincodorden)) > 12 or len(str(sincodremito)) > 28 or len(str(sincodproveedor)) > 12 ):
						anchorows.append(0.30*inch)
					else:
						anchorows.append(0.15*inch)
				data_table.append([Premito,Pordencompra,p[2],p[3],Pproveedor,p[5],p[6],p[7],p[8]])
			#end for
			t = Table(data_table, colWidths=[ 1*inch ,0.7*inch, 0.6*inch ,0.6*inch, 1.2*inch, 0.8*inch, 0.8*inch, 0.8*inch , 0.8*inch],rowHeights= anchorows)
			t.setStyle(TableStyle([
					      ('TEXTCOLOR',(0,1),(0,-1),colors.green),
					      ('FONT', (0,0), (-1,-1), 'Helvetica'),
					      ('FONTSIZE', (0,0), (-1,-1), 8),
					      ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
					      ('LINEABOVE', (0,0), (-1,0), 2, colors.green),
					      ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
					      ('LINEBELOW', (0,-1), (-1,-1), 2, colors.green),
					      ]))
			elements.append(Spacer(0,220))
			elements.append(titing)
			elements.append(Spacer(0,15))
			elements.append(t)
			titexist = Paragraph('Existencia de Combustible', styleSheet["BodyText"])
			elements.append(titexist)
			elements.append(Spacer(0,15))
			if ( aux!= 0):
				if (aux == 1):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Esq.','Gaim.','Raw.','Trev.','Madr.']] # this is the header row 
				if (aux == 2):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Esq.','Gaim.','Raw.','Trev.','Sarm.']] # this is the header row 
				if (aux == 3):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Gaim.','Raw.','Trev.','Sarm.','Madr.']] # this is the header row 
				if (aux == 4):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Esq.','Raw.','Trev.','Sarm.','Madr.']] # this is the header row 
				if (aux == 5):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Esq.','Gaim.','Trev.','Sarm.','Madr.']] # this is the header row 
				if (aux == 6):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Esq.','Gaim.','Raw.','Sarm.','Madr.']] # this is the header row 
				style2 = ParagraphStyle(name='Helvetica')
				style2.fontSize = 8
				style2.valign = 'MIDDLE'
				anchorows2 = []
				anchorows2.append(0.15*inch) #Por cabecera
				for p in listexistencia:
					if (len(p[0]) > 42):
						anchorows2.append(0.30*inch)
					else:
						if (len(p[0]) > 84):
							anchorows2.append(0.45*inch)
						else:
							anchorows2.append(0.15*inch)
				Part = Paragraph(chunk_split(p[0],12),style2)
				data_table2.append([Part,p[1],p[2],p[3],p[4],p[5],p[6],p[7]])
				#t = Table(data_table, colWidths=[ 1.2*inch, 1.8*inch, 1*inch, 1*inch, 1*inch , 1*inch],rowHeights= (cant+1)*[0.15*inch])
				t2 = Table(data_table2, colWidths=[ 3*inch, 0.5*inch , 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch],rowHeights= anchorows2)
			else:
				if (int(posiciondepo) == 1):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Esq.','Gaim.','Raw.','Trev.','Madr.']]
				if (int(posiciondepo) == 2):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Esq.','Gaim.','Raw.','Trev.','Sarm.']]
				if (int(posiciondepo) == 3):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Gaim.','Raw.','Trev.','Sarm.','Madr.']]
				if (int(posiciondepo) == 4):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Esq.','Raw.','Trev.','Sarm.','Madr.']]
				if (int(posiciondepo) == 5):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Esq.','Gaim.','Trev.','Sarm.','Madr.']]
				if (int(posiciondepo) == 6):
					data_table2 = [['Descripción', 'Consumo' ,'Exist.','Esq.','Gaim.','Raw.','Sarm.','Madr.']]

				style2 = ParagraphStyle(name='Helvetica')
				style2.fontSize = 8
				style2.valign = 'MIDDLE'
				anchorows2 = []
				anchorows2.append(0.15*inch) #Por cabecera
				for p in listexistencia:
					if (len(p[0]) > 42):
						anchorows2.append(0.30*inch)
					else:
						if (len(p[0]) > 84):
							anchorows2.append(0.45*inch)
						else:
							anchorows2.append(0.15*inch)
				Part2 = Paragraph(chunk_split(p[0],12),style2)
				data_table2.append([Part2,p[1],p[2],p[3],p[4],p[5],p[6],p[7]])
				t2 = Table(data_table2, colWidths=[ 3*inch, 0.5*inch , 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch],rowHeights= anchorows2)
				t2.setStyle(TableStyle([
					      ('TEXTCOLOR',(0,1),(0,-1),colors.green),
					      ('FONT', (0,0), (-1,-1), 'Helvetica'),
					      ('FONTSIZE', (0,0), (-1,-1), 8),
					      ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
					      ('LINEABOVE', (0,0), (-1,0), 2, colors.green),
					      ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
					      ('LINEBELOW', (0,-1), (-1,-1), 2, colors.green),
					      ]))
		      
				elements.append(t2)
				doc.build(elements,canvasmaker=NumberedCanvas,onFirstPage=myFirstPage)

			return response	

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////		
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@login_required
def listaSalida(peticion):
	#c={}
	#c.update(csrf(peticion))
	start_date = date(2005, 1, 1)
	end_date = date(2012, 10, 26)
	listasalida = list(Salida.objects.all())
	#listasalida = list(Salida.objects.filter(fecha__range=(start_date, end_date)).filter(iddeposito__exact=3))   
	listadsalida = []
	for a in listasalida:
		listadsalidaaux = list(Detallesalida.objects.filter(idsalida__exact=a.idsalida))
		if len(listadsalida) == 0:
			for b in listadsalidaaux:
				listadsalida.append(b)
		else:	
			for b in listadsalidaaux:
				w = 0
				for c in listadsalida:
					if c.idarticulo == b.idarticulo:
						c.cantidad += b.cantidad
						w = 1				
				if w == 0:
					listadsalida.append(b)
	user = peticion.user
	return render_to_response('listasalida.html',{'lista':listadsalida,'user':user,},)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////		
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
@login_required
def listaTransf(peticion):
	#c={}
	#c.update(csrf(peticion))
	start_date = date(2005, 1, 1)
	end_date = date(2012, 10, 26)
	#listatransf = list(Transferencia.objects.filter(fechaentrada__range=(start_date, end_date)))    
	listatransf = list(Transferencia.objects.all())
	listadtransf = []
	lista2dtransf = []
	for a in listatransf:
		listadtransfaux = list(Detalletrasferencia.objects.filter(idtransferencia__exact=a.idtransferencia))
		if len(listadtransf) == 0:
			for b in listadtransfaux:
				listadtransf.append(b)
				lista2dtransf.append([b,a.depositoentrada,a.depositosalida])
		else:
			for b in listadtransfaux:
				w = 0
				for c in listadtransf:
					if c.idarticulo == b.idarticulo:
						c.cantidadconfirmada += b.cantidadconfirmada
						c.cantidad += b.cantidad
						w = 1
				if w == 0:
					listadtransf.append(b)
					lista2dtransf.append([b,a.depositoentrada,a.depositosalida])
	user = peticion.user
	return render_to_response('listatransf.html',{'lista':listatransf,'lista2':lista2dtransf,'user':user,},)
    

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////		
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#============================================================================================
# GENERAR PDF's
#===========================================================================================

def pdfarticulo (peticion,id):
    
    objarticulo = Articulo.objects.get(idarticulo=id)
    html = render_to_string('articulosr.html', {'pagesize':'A4', 'objarticulo':objarticulo},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'articulo',objarticulo.idarticulo)
    

def pdfarticulodeposito (peticion,id,depo):
    
    objarticulodeposito = Articulodeposito.objects.get(idarticulo=id, iddeposito=depo)
    art = Articulo.objects.get(idarticulo=id)
    historialprecios = HistorialPrecios.objects.filter(idarticulo__exact=id)
    html = render_to_string('articulodepositor.html', {'pagesize':'A4', 'objarticulodeposito':objarticulodeposito,'historialprecios':historialprecios,'articulo':art},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'articulodeposito',objarticulodeposito.idarticulodeposito)
    
def pdfarticulodepositoad (peticion,id):
  
    objarticulodepositoad = ArticuloDepositoAd.objects.get(idarticulodeposito=id)
    objarticulodepositoad.idarticulo = list(Articulo.objects.filter(idarticulo__exact=id))
    html = render_to_string('articulodepositoadr.html', {'pagesize':'A4', 'objarticulodepositoad':objarticulodepositoad},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'articulodepositoad',objarticulodepositoad.idarticulodeposito)

def combustockindex(peticion):
    user = peticion.user
    return render_to_response('combustockindex.html',{'user':user,},)

def combustock(peticion,depo,a1,m1,d1,a2,m2,d2):
    listasal = list()
    gasoil = 0
    nafta = 0
    fechaini = datetime(int(a1),int(m1),int(d1))
    fechafin = datetime(int(a2),int(m2),int(d2))
    sal = Salida.objects.filter(iddeposito=int(depo))
    sal = sal.filter(fecha__range=(fechaini,fechafin))
    depo = int(depo)
    for s in sal:
        listasal.append(s.pk)

    if depo == 1:
        combus = DetallesalidaSarmiento.objects.filter((Q(idarticulo__exact=10474)|Q(idarticulo__exact=10502)),Q(idsalida__in=listasal))
    elif depo == 2:
        combus = DetallesalidaMadryn.objects.filter((Q(idarticulo__exact=10474)|Q(idarticulo__exact=10502)),Q(idsalida__in=listasal))
    elif depo == 3:
        combus = DetallesalidaEsquel.objects.filter((Q(idarticulo__exact=10474)|Q(idarticulo__exact=10502)),Q(idsalida__in=listasal))  
    elif depo == 4:
        combus = DetallesalidaGaiman.objects.filter((Q(idarticulo__exact=10474)|Q(idarticulo__exact=10502)),Q(idsalida__in=listasal))
    elif depo == 5:
        combus = DetallesalidaRw.objects.filter((Q(idarticulo__exact=10474)|Q(idarticulo__exact=10502)),Q(idsalida__in=listasal))
    elif depo == 6:
        combus = DetallesalidaTrevelin.objects.filter((Q(idarticulo__exact=10474)|Q(idarticulo__exact=10502)),Q(idsalida__in=listasal))
        
    for c in combus:
        if c.idarticulo_id==10474:
            gasoil=gasoil + c.cantidad
        elif c.idarticulo_id==10502:
            nafta = nafta + c.cantidad 

    print ("stock deta salida" + str(combus.count()))
    user = peticion.user
    return render_to_response('combustock.html',{'combus':combus.order_by('idsalida__fecha'),'user':user,'gasoil':gasoil,'nafta':nafta,'a1':a1,'m1':m1,'d1':d1,'a2':a2,'m2':m2,'d2':d2,},)


