# -*- coding: utf-8 -*-
#import cStringIO as StringIO
import cgi
from django.template import RequestContext, Template, Context
from django.template.loader import *
from django.http import HttpResponse
from datetime import *
#from reportlab.pdfgen import canvas
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

from depoapp.viewslistado import *




def index(peticion):
	return render_to_response('index.html',)

def depos(preticion):
	return render_to_response('deposito.html',)
#==========================================================================================================
def conexion():
        """
        Realiza la conexion a la base de datos y devuelve el cursor correspondiente
        """
        conec = "host='172.155.0.8'  dbname='deposito' user='postgres' password='sistemasavp'"
        cnx = psycopg2.connect(conec)
        cursor = cnx.cursor()
        return cursor

#==========================================================================================================
def generar_pdf_completo(html,nomb,id,fecha):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()

    pisa.CreatePDF(html,result)
#    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    response = HttpResponse(result.getvalue(), mimetype ='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+nomb+'-'+str(id)+'-'+str(fecha)+'.pdf'
    return response
    #if not pdf.err:
     #   return HttpResponse(result.getvalue(), mimetype ='application/pdf')
    #return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))
    
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
    

def generar_pdf_nombre(html,nomb,id):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()

    pisa.CreatePDF(html,result)
#    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    response = HttpResponse(result.getvalue(), mimetype ='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+nomb+'-'+str(id)+'.pdf'
    return response
    #if not pdf.err:
     #   return HttpResponse(result.getvalue(), mimetype ='application/pdf')
    #return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


#==========================================================================================
@csrf_exempt
@login_required
def listado(peticion,Nmodelo):
    """
    Vista que retorno el template index.html
    """
    c={}
    c.update(csrf(peticion))
    modelo = models.get_model('depoapp',Nmodelo)
    campos = modelo._meta.fields
    listCampos = list()
    for a in campos:
        listCampos.append(a.name)
    lista = list(modelo.objects.all())    
    user = peticion.user

    return render_to_response('listado.html',{'lista':lista,'user':user,'campos':listCampos,'modelo':Nmodelo,},)
#--------------------------------------------------------------------------------------------------------------------------
    
@csrf_exempt
@login_required
def salida(peticion):
    
    c={}
    c.update(csrf(peticion))
    modelo = models.get_model('depoapp',"Salida")
    campos = modelo._meta.fields
    listCampos = list()
    for a in campos:
        listCampos.append(a.name)
    lista = list(modelo.objects.all())    
    user = peticion.user

    return render_to_response('listado.html',{'lista':lista,'user':user,'campos':listCampos,'modelo':Nmodelo,},)    
    
#--------------------------------------------------------------------------------------------------------------------------    

#============================================================================================
# LISTADOS
#===========================================================================================

@csrf_exempt
@login_required
def listPdf(peticion,Nmodelo):
    """
    Vista que retorno el template index.html
    """
    c={}
    c.update(csrf(peticion))
    modelo = models.get_model('depoapp',Nmodelo)
    campos = modelo._meta.fields
    listCampos = list()
    for a in campos:
        listCampos.append(a.name)
    lista = list(modelo.objects.all())    
    user = peticion.user

    return generar_pdf(render_to_response('listPdf.html',{'lista':lista,'user':user,'campos':listCampos,'modelo':Nmodelo,},))

@login_required
def listaCompra(peticion):
    c={}
    c.update(csrf(peticion))
    start_date = date(2005, 1, 1)
    end_date = date(2012, 10, 26)
    #listacompra = list(Compra.objects.filter(fecha__range=(start_date, end_date)))    
    listacompra = list(Compra.objects.all())
    listadcompra = []
    for a in listacompra:
        listadcompraaux = list(Detallecompra.objects.filter(idcompra__exact=a.idcompra))
        if len(listadcompra) == 0:
        	for b in listadcompraaux:
        		listadcompra.append(b)
        else:	
        	for b in listadcompraaux:
        		w = 0
        		for c in listadcompra:
        			if c.idarticulo == b.idarticulo:
        				c.cantidad += b.cantidad
        				w = 1				
        		if w == 0:
        			listadcompra.append(b)
	
    user = peticion.user
    return generar_pdf(render_to_response('listacompra.html',{'lista':listadcompra,'user':user,},))

@login_required
def listaSalida(peticion):

    c={}
    c.update(csrf(peticion))
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


@login_required
def listaTransf(peticion):

    c={}
    c.update(csrf(peticion))
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
    #objarticulodepositoad.idarticulo = list(Articulo.objects.filter(idarticulo__exact=id))
    html = render_to_string('articulodepositoadr.html', {'pagesize':'A4', 'objarticulodepositoad':objarticulodepositoad},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'articulodepositoad',objarticulodepositoad.idarticulodeposito)
    
def pdfdevoluciones (peticion,id):
    devolucion = Devoluciones.objects.get(iddevolucion=id)
    detalledevolucion = Detalledevolucion.objects.filter(iddevolucion__exact=id)
    html = render_to_string('devolucionesr.html', {'pagesize':'A4', 'devolucion':devolucion,'detalledevolucion':detalledevolucion,'deposito':devolucion.iddeposito,'proveedor':devolucion.idproveedor},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'devolucion',devolucion.iddevolucion)

def pdfdevolucionesdepo (peticion,id,depo):
    devolucion = Devoluciones.objects.get(iddevolucion=id, iddeposito=depo)
    detalledevolucion = Detalledevolucion.objects.filter(iddevolucion__exact=id)
    html = render_to_string('devolucionesdepor.html', {'pagesize':'A4', 'devolucion':devolucion,'detalledevolucion':detalledevolucion,'proveedor':devolucion.idproveedor},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'devoluciondepo',devolucion.iddevolucion)

def pdfarticulomov (peticion,id):
    articulomov = ArticuloMov.objects.get(idarticulo=id)
    movart = MovArt.objects.filter(idarticulo__exact=id)
    html = render_to_string('articulomovr.html', {'pagesize':'A4', 'articulomov':articulomov,'movart':movart},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'articulomov',articulomov.idarticulo)

def pdfarticulomovdepo (peticion,id,depo):
    if (int(depo) == 3):
        aux = "Esquel"
    if (int(depo) == 4):
        aux = "Gaiman"
    if (int(depo) == 2):
        aux = "Pto. Madryn"
    if (int(depo) == 5):
        aux = "Rawson"
    if (int(depo) == 1):
        aux = "Sarmiento"
  
    articulomov = ArticuloMov.objects.get(idarticulo=id)
    movart = MovArt.objects.filter(idarticulo__exact=id, direccion=aux)
    html = render_to_string('articulomovdepor.html', {'pagesize':'A4', 'articulomov':articulomov,'movart':movart},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'articulomovdepo',articulomov.idarticulo)

    
def pdftransferencia (peticion,id):
    objtransferencia = Transferencia.objects.get(idtransferencia=id)
    dettransferencia = list(Detalletrasferencia.objects.filter(idtransferencia__exact=id))
    html = render_to_string('transferenciasr.html', {'pagesize':'A4', 'objtransferencia':objtransferencia,'dettransferencia':dettransferencia},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'transferencia',objtransferencia.idtransferencia)

def pdftransferenciaent (peticion,id,depo):
    objtransferencia = Transferencia.objects.get(idtransferencia=id)
    dettransferencia = list(Detalletrasferencia.objects.filter(idtransferencia__exact=id))
    html = render_to_string('transferenciasentr.html', {'pagesize':'A4', 'objtransferencia':objtransferencia,'dettransferencia':dettransferencia},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'transferenciaent',objtransferencia.idtransferencia)

def pdftransferenciasal (peticion,id,depo):
    objtransferencia = Transferencia.objects.get(idtransferencia=id)
    dettransferencia = list(Detalletrasferencia.objects.filter(idtransferencia__exact=id))
    html = render_to_string('transferenciassalr.html', {'pagesize':'A4', 'objtransferencia':objtransferencia,'dettransferencia':dettransferencia},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'transferenciasal',objtransferencia.idtransferencia)

    
def pdfcompra (peticion,id):
    
    objcompra= Compra.objects.get(idcompra=id)
    detcompra = list(Detallecompra.objects.filter(idcompra__exact=id))
    html = render_to_string('comprasr.html', {'pagesize':'A4', 'detcompra':detcompra,'objcompra':objcompra},context_instance=RequestContext(peticion))
    return generar_pdf_completo(html,'compra',objcompra.idcompra,objcompra.fecha)

def pdfsalida (peticion,id):
    salida = Salida.objects.get(idsalida=id)
    detallesalida = Detallesalida.objects.filter(idsalida__exact=id)
    html = render_to_string('salidar.html', {'pagesize':'A4', 'salida':salida,'detallesalida':detallesalida},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'salida',salida.idsalida)
   
def pdfsalidadepo (peticion,id,depo):
    salida = Salida.objects.get(idsalida=id, iddeposito=depo)
    detallesalida = Detallesalida.objects.filter(idsalida__exact=id)
    html = render_to_string('salidadepor.html', {'pagesize':'A4', 'salida':salida,'detallesalida':detallesalida},context_instance=RequestContext(peticion))
    return generar_pdf_nombre(html,'salidadepo',salida.idsalida)

