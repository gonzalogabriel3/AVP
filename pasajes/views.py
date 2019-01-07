from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import redirect
from .models import *
from .forms import *
from .funciones import *
import datetime, time
from io import BytesIO
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.contrib import messages

# Create your views here

#################################INDEX'S#################################################
def index(request):
	
	return render(request, 'index.html')


#Funcion para retornar los datos de la tabla de agente renderizados en un template
def indexAgenteView(request):
	agentes=Agente.objects.all().order_by('-id')
	
	context={
		'agentes':agentes,
	}
	
	return render(request, 'indexAgente.html', context)

def indexLocalidadView(request):
	localidades=Localidad.objects.all().order_by('-id')
	
	context={
		'localidades':localidades
	}
	
	return render(request, 'indexLocalidad.html', context)


def indexFamiliarView(request):
	familiares=Familiar.objects.all().order_by('-id')
	
	context={
		'familiares':familiares,
	}
	
	return render(request, 'indexFamiliar.html', context)

def indexEmpresaView(request):
	empresas=Empresa.objects.all().order_by('-id')
	
	context={
		'empresas':empresas,
	}
	
	return render(request, 'indexEmpresa.html', context)

def indexPasajeView(request):
	pasajes=Pasaje.objects.all().order_by('-id')
	
	context={
		'pasajes':pasajes,
	}
	
	return render(request, 'indexPasaje.html', context)

def indexPasajeroView(request):
	pasajeros=Pasajero.objects.all().order_by('-id')
	
	context={
		'pasajeros':pasajeros,
	}
	
	return render(request, 'indexPasajero.html', context)
################FIN DE INDEX'S########################################


################FORMULARIOS###########################################

#********ABM AGENTE***********#
def altaAgente(request):

	#Recibo el request,si es un request de tipo POST lo valido y guardo el nuevo agente
	if(request.method == 'POST'):
		
		form=formularioAgente(request.POST)	
		#Valido el formulario
		if(form.is_valid()):
				messages.success(request,"Se ha creado un nuevo agente")
				agente=form.save(commit=False)
				agente.save()
				return redirect('agente')
	
	#Si el request no es POST(GET) creo el formulario y lo renderizo en una vista
	else:
		form=formularioAgente()
		
	titulo="Agregar nuevo agente"	
	return render(request,'formularios/agente.html',{'form':form,'titulo':titulo})

def bajaAgente(request,idAgente):

	agente=Agente.objects.get(id=idAgente)

	if(request.method=="POST"):
		messages.success(request,"Se ha eliminado al agente '"+agente.apellido+" "+agente.nombre+"' con id "+str(agente.id))
		agente.delete()
		return redirect('agente')

	texto="el agente '"+agente.nombre+" "+agente.apellido+"',con id "+str(agente.id)+"?"
	nombreUrl="agente"

	return render(request,'confirmaciones/eliminar.html',{'texto':texto,'nombreUrl':nombreUrl})

def modificacionAgente(request,idAgente):

	agente=Agente.objects.get(id=idAgente)
	#Si se ingresa por GET creo el formulario y paso como instancia los datos de un agente
	if(request.method == 'GET'):
		form=formularioAgente(instance=agente)
		
	#Si por el contrario se ingresa por POST valido el formulario y guardo los datos en el agente	
	elif(request.method == "POST"):
		
		form=formularioAgente(request.POST, instance = agente)
		if(form.is_valid()):
			messages.success(request,"Se ha modificado al agente '"+agente.apellido+" "+agente.nombre+"' con id "+str(agente.id))
			form.save()
			return redirect('agente')

	titulo="Modificar agente"
	return render(request,'formularios/agente.html',{'form':form,'agente':agente,'titulo':titulo})

#********FIN ABM AGENTE***********#


#********ABM LOCALIDAD***********#
def altaLocalidad(request):

	#Recibo el request,si es un request de tipo POST lo valido y guardo el nuevo agente
	if(request.method == 'POST'):
		
		form=formularioLocalidad(request.POST)	
		#Valido el formulario
		if(form.is_valid()):
				messages.success(request,"Se ha creado nueva localidad")
				localidad=form.save(commit=False)
				localidad.save()
				return redirect('localidad')
	
	#Si el request no es POST(GET) creo el formulario y lo renderizo en una vista
	else:
		form=formularioLocalidad()
		
	titulo="Agregar nueva localidad"	
	return render(request,'formularios/localidad.html',{'form':form,'titulo':titulo})



def bajaLocalidad(request,idLocalidad):

	localidad=Localidad.objects.get(id=idLocalidad)

	if(request.method=="POST"):
		messages.success(request,"Se ha eliminado la localidad '"+localidad.nombre+ "',con id "+str(localidad.id))
		localidad.delete()
		return redirect('localidad')

	texto="la localidad '"+localidad.nombre+"',con id "+str(localidad.id)+"?"
	nombreUrl="localidad"

	return render(request,'confirmaciones/eliminar.html',{'texto':texto,'nombreUrl':nombreUrl})

def modificacionLocalidad(request,idLocalidad):

	localidad=Localidad.objects.get(id=idLocalidad)
	#Si se ingresa por GET creo el formulario y paso como instancia los datos de un Localidad
	if(request.method == 'GET'):
		form=formularioLocalidad(instance=localidad)
		
	#Si por el contrario se ingresa por POST valido el formulario y guardo los datos en el Localidad	
	elif(request.method == "POST"):
		form=formularioLocalidad(request.POST, instance = localidad)
		
		if(form.is_valid()):
			#Agrego un mensaje en caso de que se modifique correctamente
			messages.success(request,"Se ha modificado la localidad '"+localidad.nombre+ "',con id "+str(localidad.id))
			form.save()
			return redirect('localidad')

	titulo="Modificar localidad"
	return render(request,'formularios/localidad.html',{'form':form,'localidad':localidad,'titulo':titulo})


#********FIN ABM LOCALIDAD***********#


#********ABM FAMILIAR***********#
def altaFamiliar(request):

	if(request.method == 'POST'):
		
		form=formularioFamiliar(request.POST)	
		#Valido el formulario
		if(form.is_valid()):
				messages.success(request,"Se ha creado un nuevo familiar")
				familiar=form.save(commit=False)
				familiar.save()
				return redirect('familiar')
	
	#Si el request no es POST(GET) creo el formulario y lo renderizo en una vista
	else:
		form=formularioFamiliar()
		
	
	titulo="Agregar nuevo familiar"	
	return render(request,'formularios/familiar.html',{'form':form,'titulo':titulo})

def bajaFamiliar(request,idFamiliar):

	familiar=Familiar.objects.get(id=idFamiliar)

	if(request.method=="POST"):
		messages.success(request,"Se ha eliminado al familiar '"+familiar.apellido+" "+familiar.nombre+"' con id "+str(familiar.id))
		familiar.delete()
		return redirect('familiar')

	texto="a el familiar '"+familiar.nombre+" "+familiar.apellido+"',con id "+str(familiar.id)+"?"
	nombreUrl="familiar"

	return render(request,'confirmaciones/eliminar.html',{'texto':texto,'nombreUrl':nombreUrl})

def modificacionFamiliar(request,idFamiliar):

	familiar=Familiar.objects.get(id=idFamiliar)
	#Si se ingresa por GET creo el formulario y paso como instancia los datos de un Familiar
	if(request.method == 'GET'):
		form=formularioFamiliar(instance=familiar)
		
	#Si por el contrario se ingresa por POST valido el formulario y guardo los datos en el Familiar	
	elif(request.method == "POST"):
		
		form=formularioFamiliar(request.POST, instance = familiar)
		if(form.is_valid()):
			messages.success(request,"Se ha modificado al familiar '"+familiar.apellido+" "+familiar.nombre+"' con id "+str(familiar.id))
			form.save()
			return redirect('familiar')

	titulo="Modificar familiar"
	return render(request,'formularios/familiar.html',{'form':form,'familiar':familiar,'titulo':titulo})


#********FIN ABM FAMILIAR***********#



#********ABM EMPRESA***********#
def altaEmpresa(request):

	if(request.method == 'POST'):
		
		form=formularioEmpresa(request.POST)
		
		#Valido el formulario
		if(form.is_valid()):
				messages.success(request,"Se ha creado una nueva empresa")
				empresa=form.save(commit=False)
				empresa.save()
				return redirect('empresa')
	
	#Si el request no es POST(GET) creo el formulario y lo renderizo en una vista
	else:
		form=formularioEmpresa()
		
	titulo="Agregar nueva empresa"	
	return render(request,'formularios/empresa.html',{'form':form,'titulo':titulo})


def bajaEmpresa(request,idEmpresa):

	empresa=Empresa.objects.get(id=idEmpresa)

	if(request.method=="POST"):
		messages.success(request,"Se ha eliminado la empresa '"+empresa.nombre+"' con id "+str(empresa.id))
		empresa.delete()
		return redirect('empresa')

	texto="la empresa '"+empresa.nombre+"',con id "+str(empresa.id)+"?"
	nombreUrl="empresa"

	return render(request,'confirmaciones/eliminar.html',{'texto':texto,'nombreUrl':nombreUrl})

def modificacionEmpresa(request,idEmpresa):

	empresa=Empresa.objects.get(id=idEmpresa)
	#Si se ingresa por GET creo el formulario y paso como instancia los datos de un Empresa
	if(request.method == 'GET'):
		form=formularioEmpresa(instance=empresa)
		
	#Si por el contrario se ingresa por POST valido el formulario y guardo los datos en el Empresa	
	elif(request.method == "POST"):
		
		form=formularioEmpresa(request.POST, instance = empresa)
		if(form.is_valid()):
			messages.success(request,"Se ha modificado la empresa '"+empresa.nombre+"' con id "+str(empresa.id))
			form.save()
			return redirect('empresa')

	titulo="Modificar empresa"
	return render(request,'formularios/empresa.html',{'form':form,'empresa':empresa,'titulo':titulo})


#********FIN ABM EMPRESA***********#


#********ABM PASAJE***********#
def altaPasaje(request):

	
	if(request.method == 'POST'):
		
		form=formularioPasaje(request.POST)	
		#Valido el formulario
		if(form.is_valid()):
				messages.success(request,"Se ha creado un nuevo pasaje")
				pasaje=form.save(commit=False)
				#Digo que la fecha de emision es la fecha/hora actual,le resto 3 horas con timedelta porque datetime.now() guarda la hora
				#con 3 horas de adelanto
				pasaje.fecha_emision=datetime.datetime.now()-datetime.timedelta(hours=3)
				
				#(Si se desea que la fecha de emision sea automatica)pasaje.fecha_emision=datetime.datetime.now()
				pasaje.save()
				return redirect('pasaje')
	
	#Si el request no es POST(GET) creo el formulario y lo renderizo en una vista
	else:
		form=formularioPasaje()
		
	titulo="Agregar nuevo pasaje"	
	return render(request,'formularios/pasaje.html',{'form':form,'titulo':titulo})

def bajaPasaje(request,idPasaje):

	pasaje=Pasaje.objects.get(id=idPasaje)

	if(request.method=="POST"):
		messages.success(request,"Se ha eliminado el pasaje con id '"+str(pasaje.id)+"'")
		pasaje.delete()
		return redirect('pasaje')

	texto="el pasaje 'N°"+str(pasaje.id)+"',emitido el dia "+str(pasaje.fecha_emision.strftime('%Y-%m-%d %H:%M'))+"?"
	nombreUrl="pasaje"

	return render(request,'confirmaciones/eliminar.html',{'texto':texto,'nombreUrl':nombreUrl})

def modificacionPasaje(request,idPasaje):

	pasaje=Pasaje.objects.get(id=idPasaje)
	#Si se ingresa por GET creo el formulario y paso como instancia los datos de un Pasaje
	if(request.method == 'GET'):
		form=formularioPasaje(instance=pasaje)
		
	#Si por el contrario se ingresa por POST valido el formulario y guardo los datos en el Pasaje	
	elif(request.method == "POST"):
		
		form=formularioPasaje(request.POST, instance = pasaje)
		if(form.is_valid()):
			messages.success(request,"Se ha modificado el pasaje con id '"+str(pasaje.id)+"'")
			pasaje.fecha_emision=datetime.datetime.now()-datetime.timedelta(hours=3)
			form.save()
			return redirect('pasaje')

	titulo="Modificar Pasaje"
	return render(request,'formularios/pasaje.html',{'form':form,'pasaje':pasaje,'titulo':titulo})


#********FIN ABM PASAJE***********#

#********REPORTES********************#
def reportePasaje(request,idPasaje):
	pasaje=Pasaje.objects.get(id=idPasaje)

	#Obtengo la fecha actual para asignarla al nombre del pdf
	fecha=datetime.datetime.now()
	fecha=fecha.strftime("%d/%m/%Y")
	#Renderizo la vista que sera devuelta
	html_string = render_to_string('reportes/pasaje.html', {'pasaje': pasaje})
	#Agrego el 'base_url' para poder cargar imagenes en el pdf
	html = HTML(string=html_string,base_url=request.build_absolute_uri())
	result = html.write_pdf()
	#Indico el tipo de contenido en la respuesta,en este caso un PDF
	response = HttpResponse(content_type='application/pdf;')
	#Indico el nombre del nuevo pdf
	response['Content-Disposition'] = 'inline; filename=Reporte_Pasaje_Nro'+str(pasaje.id)+'_'+str(fecha)+'.pdf'
	response['Content-Transfer-Encoding'] = 'binary'

	#Creo un archivo temporal que va a contener el PDF generado
	with tempfile.NamedTemporaryFile(delete=True) as output:
		output.write(result)
		output.flush()
		output = open(output.name, 'rb')
		response.write(output.read())

	return response
########FIN REPORTES##############

##########Formulario pasajes######################
def altaPasaje(request,idPasajero):
	pasajero=Pasajero.objects.get(id=idPasajero)
	#form=formularioPasaje()
	#Si se recibe por POST creo una nueva instancia de Pasaje()
	if(request.method == 'POST'):
		form=formularioPasaje(request.POST)
		
		pasaje=Pasaje()
		
		#Obtengo la fecha del formulario y le cambio el formato para poder guardarlo en el campor "fecha_viaje"
		fecha=request.POST.get('fecha_viaje')
		fecha = datetime.datetime.strptime(fecha,"%d/%m/%Y").strftime("%Y-%m-%d") 
		pasaje.fecha_viaje=fecha
		
		#Obtengo el id de la empresa desde el formulario(busco ese objeto empresa) y se lo asigno al campo "id_empresa" del objeto pasaje
		id_empresa=request.POST.get('id_empresa')
		empresa=Empresa.objects.get(id=id_empresa)
		pasaje.id_empresa=empresa

		#Valido si es un familiar o un agente
		if(pasajero.id_familiar):
			pasaje.id_agente=pasajero.id_agente
			pasaje.id_familiar=pasajero.id_familiar
		else:
			pasaje.id_agente=pasajero.id_agente

		#Indico la fecha de emision
		pasaje.fecha_emision=datetime.datetime.now()-datetime.timedelta(hours=3)

		#Obtengo la via,origen,y destino desde el formulario y se lo asigno al objeto pasaje
		pasaje.via=request.POST.get('via')
		pasaje.origen=request.POST.get('origen')
		pasaje.destino=request.POST.get('destino')

		#Guardo el nuevo pasaje y retorno al metodo que genera el reporte en pdf,pasandole el id del pasaje nuevo
		pasaje.save()
		
		return reportePasaje(request,pasaje.id)
	#Si el request no es POST(GET) creo el formulario y lo renderizo en una vista
	else:
		form=formularioPasaje()
		
	titulo="Generar nuevo pasaje"

	return render(request,'formularios/pasaje.html',{'form':form,'titulo':titulo,'pasajero':pasajero})

#*************FIN formulario pasajes*************#

def loginView(request):
	return render(request,'registration/login.html')

def indexProyecto(request):
	return render(request,'proyecto/indexProyecto.html')