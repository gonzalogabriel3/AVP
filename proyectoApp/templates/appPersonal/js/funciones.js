var numeros="0123456789";
var letras="abcdefghyjklmnñopqrstuvwxyz";
var simbolos="¬|@·~½¬{[]}\¸°!#$%&/()=?¡¿'+-.,;:_<>*";
//--------------------------------------------------------------------------------------------------------------
//Evalua una cadena para ver si contiene caracteres numericos, en caso de tenerlos retorna 1, caso contrario 0
function tiene_numeros(texto){
	for(i=0; i<texto.length; i++){
		if (numeros.indexOf(texto.charAt(i),0)!=-1){
			return 1;
		}
	}
	return 0;
} 

//--------------------------------------------------------------------------------------------------------------
function tiene_no_valido(texto){
	texto = texto.toLowerCase();
	for(i=0; i<texto.length; i++){
		if (letras.indexOf(texto.charAt(i),0)!=-1 || simbolos.indexOf(texto.charAt(i),0)!=-1){
			return 1;
		}
	}
	return 0;
}

//--------------------------------------------------------------------------------------------------------------
/***
Recibe el mes que parseo validarFecha, y devuelve la cantidad de dias que trae el mes, caso erroneo retorna -1
***/
function validarMes(mes,anio){
	var dmax = -1;
	switch (mes){
		case 1:
			dmax=31;
			break;
		case 2:
			if (anio % 4 == 0) 
				dmax = 29; 
			else 
				dmax = 28;
			break;
		case 3:
			dmax = 31;
			break; 
		case 4:
			dmax = 30;
			break; 
		case 5:
			dmax = 31;
			break; 
		case 6:
			dmax = 30;
			break; 
		case 7:
			dmax = 31;
			break; 
		case 8:
			dmax = 31;
			break; 
		case 9:
			dmax = 30;
			break; 
		case 10:
			dmax = 31;
			break; 
		case 11:
			dmax = 30;
			break; 
		case 12:
			dmax = 31;
			break;
	}
	return dmax;
}

//--------------------------------------------------------------------------------------------------------------
/***
//Determina si la fecha en su totalidad es correcta o erronea, en caso de error indica en donde se encuentran el o los mismos
***/
function validarFecha(anio,mes,dia){
	var estado = -1;
	if (tiene_no_valido(anio) == 0){
	    var dmax = validarMes(parseInt(mes),parseInt(anio));
	    if (dmax != -1){
		if (parseInt(dia)>=1 || parseInt(dia)<= dmax){
		    estado = 1;
		}
		else{
		    alert("Error en la entrada de dia");
		}
	    }
	    else{
		alert("Error en la entrada de mes");
	    }
	}
	else{
	  alert("Error en la entrada de AÑO");
	}
	return estado;
}

//--------------------------------------------------------------------------------------------------------------
/***
/
***/
function validaAnio(anio){
    if (tiene_numeros(anio)!=0){
	if ((anio.length)!=4){
	    alert ("Ingrese un periodo valido AAAA (ej:2007)");
	    return 0;
	}else{
	    return 1;
	}
    }else{
      alert ("Ingrese un periodo valido (numeros)");
      return 0;
    }
    return 0;
}

function validaMes(mes){
    if (tiene_numeros(mes)!=0){
	if ((mes.length)!=2 && mes<=12 && mes>=1){
	    alert ("Ingrese un periodo valido MM (ej:07)");
	    return 0;
	}else{
	    return 1;
	}
    }else{
      alert ("Ingrese un periodo valido (numeros)");
      return 0;
    }
    return 0;
}



//--------------------------------------------------------------------------------------------------------------
/***
/
***/
function reporteAnual(){
  if (validaAnio(document.getElementById('anio').value) ==1){
      //open("/ausReport/"+$F('anio')+"/","_self");
      open("/personal/ausReport/?anio="+document.getElementById('anio').value,"_self");   
  }
  return false;
}


function reporteMensual(path){
  if (validaAnio(document.getElementById('anio').value) ==1){
      if (validaMes(document.getElementById('mes').value) ==1){
      //open("/ausReport/"+$F('anio')+"/","_self");
	  open(path+"?anio="+document.getElementById('anio').value+"&mes="+document.getElementById('mes').value,"_self");   
      }
  }
  return false;
}
function reporteMensualCMO(){
  if (validaAnio(document.getElementById('anio').value) ==1){
      if (validaMes(document.getElementById('mes').value) ==1){
      //open("/ausReport/"+$F('anio')+"/","_self");
	  open("/personal/ausReportMensualCMO/?anio="+document.getElementById('anio').value+"&mes="+document.getElementById('mes').value,"_self");   
      }
  }
  return false;
}


function reportePresentismo(){
  if (validaAnio(document.getElementById('anio').value) ==1){
      if (validaMes(document.getElementById('mes').value) ==1){
      //open("/ausReport/"+$F('anio')+"/","_self");
	  open("/personal/presentReport/?anio="+document.getElementById('anio').value+"&mes="+document.getElementById('mes').value,"_self");   
      }
  }
  return false;  
}

function reporteAnualDir(path){
  
  if (validaAnio(document.getElementById('anio').value) ==1){
      open(path+"?anio="+document.getElementById('anio').value+"&direc"+document.getElementById('dir').value,"_self");   
  }
  return false;
}

function reportePartDiario(path){
  if (validarFecha(document.getElementById('anio').value, document.getElementById('mes').value, document.getElementById('dia').value) ==1){
      open(path+"?anio="+document.getElementById('anio').value+"&mes="+document.getElementById('mes').value+"&dia="+document.getElementById('dia').value,"_self");
  }
  return false;
}

function auspartediarioexcel(path){
  if (validarFecha(document.getElementById('anio').value, document.getElementById('mes').value, document.getElementById('dia').value) ==1){
      //fechain = $F('anio') + "-" + $F('mes') +"-"+ $F('dia');
      open(path+"?anio="+document.getElementById('anio').value+"&mes="+document.getElementById('mes').value+"&dia="+document.getElementById('dia').value,"_self");
  }
  return false;
}

function listadoAltasBajas2(){
  
  if (validaAnio(document.getElementById('anio').value) ==1){
      open("listaltasbajas?periodo="+document.getElementById('anio').value,"_self");   
  }
  return false;
}

//--------------------------------------------------------------------------------------------------------------
/***
/
***/
function reporteAus(){
	//if (validarFecha(escape(anio.value),escape(mes.value),escape(dia.value)) == 1){
	if (validarFecha(document.getElementById('anio').value, document.getElementById('mes').value, document.getElementById('dia').value) ==1){
	    alert("Fecha OK");
	}
	else{
	    alert("Ingrese una fecha correcta!");
	}
	//var url="http://172.155.0.6:7000/ausentismos/"+escape(anio.value)+"/"+escape(mes.value)+"/"+escape(dia.value);
//	var url="http://172.155.0.6:7000/ausentismos/"+$F('anio')+"/"+$F('mes')+"/"+$F('dia');
	var url="http://172.155.0.9:7000/reporteausentismos/"+$F('anio')+"/"+$F('mes')+"/"+$F('dia');
	open(url,"_self");
	return false;
}

//--------------------------------------------------------------------------------------------------------------
/***
/
***/
function llamaPdf(){
	//if (validarFecha(escape(anio.value),escape(mes.value),escape(dia.value)) == 1){
	if (validarFecha(document.getElementById('anio').value, document.getElementById('mes').value, document.getElementById('dia').value) ==1){
	    alert("Fecha OK");
	}
	else{
	    alert("Ingrese una fecha correcta!");
	}
	//var url="http://172.155.0.6:7000/ausentismos/"+escape(anio.value)+"/"+escape(mes.value)+"/"+escape(dia.value);
	var url="http://172.155.0.9:7000/ausentismos/"+$F('anio')+"/"+$F('mes')+"/"+$F('dia');

	open(url,"_self");
	return false;
}

//--------------------------------------------------------------------------------------------------------------
/***
/
***/
function infoAgente(nroDoc){
    //parseInt('') 
    var url="http://172.155.0.9:7000/agente/"+nroDoc;
    open(url,"_self");
    return false;
}
//--------------------------------------------------------------------------------------------------------------
/***
/
***/
function listaAgentesAll(){
	var url="http://172.155.0.9:7000/agentesAll/";
	open(url,"_self");
	return false;
}
//--------------------------------------------------------------------------------------------------------------
/***
/
***/
function buscaAgentes(){
	var url="http://172.155.0.9:7000/agentesBusc/"+$F('apellido');
	open(url,"_self");
	return false;
}
//--------------------------------------------------------------------------------------------------------------
/***
/
***/
function fliaAgente(nroDoc){
    //parseInt('') 
    var url="http://172.155.0.9:7000/familiares/"+nroDoc;
    open(url,"_self");
    return false;
}


//--------------------------------------------------------------------------------------------------------------
/***
/
***/


function reporteVacasAgent(){
  
  var num=document.getElementById('id');
  //alert(num.value);
  
  open("/personal/vacas/"+num.value+"/","_self");   
  //open("/vacas/"+id+"/","_self");   
  
  return false;
}



function Eliminar(path) {

    if(confirm("¿Desea eliminar?")) {

        document.location.href= path;

    }

}


function doOperation(path) {

    if(confirm("¿Desea realizar la operación?")) {

        document.location.href= path;

    }

}

function buscaragentes(path){

	var busc = document.getElementById('busqueda').value ;
	
	open(path+"?busc="+busc,"_self");

  return false;
}

function buscargenerico(path,param){

	var busc = document.getElementById('busqueda').value ;
	
	open(path+"?busc="+busc+param,"_self");

  return false;
}


function Open(path) {

    open(path,"_self");
    
}

