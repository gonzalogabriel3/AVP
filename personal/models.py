# -*- coding: utf-8 -*-
from django.db import models
from django import forms
#from django.utils.encoding import force_unicode
from django.contrib.admin import widgets  
from datetime import *

#from personal.forms import *

TIPO_DOC = (
	("5","DNI"),
	("2","LE"), 
	("1","LC"),
	("4","CI"),
)

l = list()
for i in range(0,23+1):
    l.append((i,str(i)),)
TIPO_CATEGORIA = (
    tuple(l)
)

TIPO_ECIVIL = (
	("S","Soltero/a"), 
	("C","Casado/a"), 
	("V","Viudo/a"), 
	("D","Divorciado/a"), 
)

TIPO_ESCO = (
	("Pre-escolar","Pre-escolar"),
	("Primer ciclo EGB","Primer ciclo EGB"), 
	("Segundo ciclo EGB","Segundo ciclo EGB"), 
	("Tercer ciclo EGB","Tercer ciclo EGB"), 
	("Polimodal","Polimodal"), 
	("Superior","Superior"), 
)

TIPO_LICANUAL = (
	("LIC","LIC"), 
	("INT","INT"), 
	("DES","DES"), 
)

TIPO_SEXO = (
	("F","F"), 
	("M","M"), 
)

TIPO_PLANTA = (
	("Temporaria","Temporaria"),
	("Contrato Serv.","Contrato Serv."),
	("Contrato Obr.","Contrato Obr."),
	("Planta permanente","Planta permantene"),
	("Aprendiz","Aprendiz"),
	("Pasante","Pasante"),
)

TIPO_SITUACION = (
	(0,"Baja"),
	(1,"Inactivo"),
	(2,"Activo"),
)

TIPO_TITULO = (
	("Primario","Primario"),
	("Ciclo Basico Secundario","Ciclo Basico Secundario"),
	("Secundario","Secundario"),
	("Tecnico","Tecnico"),
	("Ciclo Basico Terciario","Ciclo Basico Terciario"),
	("Profesional","Profesional"),
)
TIPO_ARTICULO = (
	
)

TIPO_SANCION = (
	('S',"Suspencion"),
	('A',"Apercivimiento"),
	('L',"LLamando Atencion"),
	('Z',"Sumario"),
)

TIPO_CARGO = (
        ("X","SIN ESPECIFICAR"),
	("CG1","Capataz Gral - Carpinteria Central"),
	("CG2","Capataz Gral - Central Zonas"),
	("CG3","Capataz Gral - Diesel y Ajuste equipos pesados central y zonas"),
)
# Create your models here.


#··························································································································································        
class Inicio(models.Model):
    idinicio = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50, blank=True)
    mensaje = models.TextField(max_length=5000, blank=True)
    class Meta:
        db_table = u'inicio'
    def __str__(self):
        return self.titulo 
            
#··························································································································································        
class Nacionalidad(models.Model):
    idnacionalidad = models.IntegerField(primary_key=True)
    nacionalidad = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'nacionalidad' 
    def __str__(self):
        return self.nacionalidad      
#··························································································································································        
class Funcion(models.Model):
    idfuncion = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=200, blank=True)
    observacion = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'funcion'
            
    def __str__(self):
        return self.descripcion    
#··························································································································································        
class CargoFuncion(models.Model):
    idcargof = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=200, blank=True)
    observacion = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'cargo_funcion'
    def __str__(self):
        return self.descripcion            
                
#··························································································································································
class Clase(models.Model):
    idclase = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'clase'
    
    def __str__(self):
        return self.descripcion 
              
#··························································································································································        
class Direccion(models.Model):
    iddireccion = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'direccion'

    def __str__(self):
        return self.descripcion        
#··························································································································································                
class Zona(models.Model):
    idzona = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'zona'
    
    def __str__(self):
        return self.descripcion

#··························································································································································        
class Codigopostal(models.Model):
    idcodpos = models.IntegerField(primary_key=True)
    codigopostal = models.IntegerField(null=True, blank=True)
    descripcion = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'codigopostal'
    
    def __str__(self):
        return str(self.descripcion) + " -- " + str(self.codigopostal)       
#··························································································································································        
class Articulo(models.Model):
    idarticulo = models.IntegerField(primary_key=True, verbose_name= "Articulo")
    descripcion = models.CharField(max_length=200, blank=True)
    eslicencia = models.BooleanField(blank=True, verbose_name = "Es Licencia")
    maxanual = models.IntegerField(null=True, blank=True, verbose_name = "Maximo Anual")
    maxmensual = models.IntegerField(null=True, blank=True, verbose_name = "Maximo Mensual")
    class Meta:
        db_table = u'articulo'
    
    def __str__(self):
        return self.descripcion            
        
#··························································································································································        
class Agrupamiento(models.Model):
    idagrupamiento = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'agrupamiento'

    def __str__(self):
        return self.descripcion        

#··························································································································································        
class Agente(models.Model):
    idagente = models.AutoField(primary_key=True)
    nrolegajo = models.IntegerField(null=True, blank=True, verbose_name = "Nro Legajo")
    apellido = models.CharField(max_length=200, blank=True)
    nombres = models.CharField(max_length=200)
    tipodoc = models.CharField(max_length=200, blank=True, choices=TIPO_DOC, verbose_name = "Tipo Documento")
    nrodocumento = models.SmallIntegerField(unique=True, verbose_name = "Nro Documento")
    sexo = models.CharField(max_length=1, choices=TIPO_SEXO)
    fechanacimiento = models.DateField(verbose_name = "Fecha de Nacimiento")
    nacionalidad = models.ForeignKey(Nacionalidad, db_column="nacionalidad", verbose_name="Nacionalidad",on_delete=models.CASCADE)
    estadocivil = models.CharField(max_length=200, choices=TIPO_ECIVIL, verbose_name = "Estado Civil")
    codigopostal = models.ForeignKey(Codigopostal, null=True, db_column='codigopostal', blank=True, verbose_name = "Código Postal",on_delete=models.CASCADE)
    domicilio = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200, blank=True)
    fechaalta = models.DateField(null=True, blank=True, verbose_name = "Fecha Alta")
    cargo = models.CharField(max_length=200,blank=True, verbose_name = "Cargo", choices=TIPO_CARGO)
    antigranios = models.SmallIntegerField(null=True, blank=True, verbose_name = "Antigüedad R. en Años")
    antigrmeses = models.SmallIntegerField(null=True, blank=True, verbose_name = "Antigüedad R. en Meses")
    antigrvanios = models.SmallIntegerField(null=True, blank=True, verbose_name = "Antigüedad R. V. en Años")
    antigrvmeses = models.SmallIntegerField(null=True, blank=True, verbose_name = "Antigüedad R. V. en Meses")
    antigravpanios = models.SmallIntegerField(null=True, db_column='antigravpanio', blank=True, verbose_name = "Antigüedad R. AVP en Años")
    antigravpmeses = models.SmallIntegerField(null=True, db_column='antigravpmeses', blank=True, verbose_name = "Antigüedad R AVP en Meses")
    situacion = models.SmallIntegerField(null=False, choices=TIPO_SITUACION)
    fechabaja = models.DateField(null=True, blank=True, verbose_name = "Fecha Baja")
    razonbaja = models.CharField(max_length=400, blank=True, verbose_name = "Razon Baja")
    clase = models.ForeignKey(Clase, related_name="clase", null=True, db_column='clase', blank=True,on_delete=models.CASCADE)
    categoria = models.SmallIntegerField(null=True, choices = TIPO_CATEGORIA ,blank=True)
    titulo = models.CharField(max_length=200, blank=True, choices=TIPO_TITULO)
    planta = models.CharField(max_length=200, blank=True, choices=TIPO_PLANTA)
    agrupamiento = models.ForeignKey(Agrupamiento,null=True, blank=True,db_column='agrupamiento',on_delete=models.CASCADE)
    iddireccion = models.ForeignKey(Direccion, null=True, db_column='iddireccion', blank=True, verbose_name = "Dirección",on_delete=models.CASCADE)
    iddireccionreal = models.ForeignKey(Direccion, related_name="iddireccionreal", null=True, db_column='iddireccionreal', blank=True, verbose_name = "Dir. Real",on_delete=models.CASCADE)
    #sucursal = models.ForeignKey(Direccion, null=True, db_column='sucursal', blank=True)
    nrocuenta = models.CharField(max_length=200, blank=True, verbose_name = "Nro Cuenta")
    nrocontrato = models.CharField(max_length=200, blank=True, verbose_name = "Nro Contrato")
    nrolegajosueldos = models.CharField(max_length=200, blank=True, verbose_name = "Nro Legajos Sueldos")
    observaciones = models.CharField(max_length=400, blank=True)
    total102 = models.SmallIntegerField(null=True, blank=True, verbose_name = "Total Art. 102")
    seccion = models.CharField(max_length=200, blank=True)
    dexc = models.BooleanField(blank=True , verbose_name = "Dedicación Intensiva")
    defun = models.BooleanField(blank=True)
    funcion = models.ForeignKey(Funcion, null=True,db_column='funcion', blank=True,on_delete=models.CASCADE)
    idcargof =  models.ForeignKey(CargoFuncion, null=True,db_column='idcargof', blank=True, verbose_name='Cargo Funcion',on_delete=models.CASCADE)
    idzona = models.ForeignKey(Zona, null=True, db_column='idzona', blank=True, verbose_name = "Zona",on_delete=models.CASCADE)
    idzonareal = models.ForeignKey(Zona, related_name="idzonareal", null=True, db_column='idzonareal', blank=True, verbose_name = "Zona Real",on_delete=models.CASCADE)
    claseac = models.ForeignKey(Clase, related_name="claseac", null=True, db_column='claseac', blank=True, verbose_name='Clase a Cargo',on_delete=models.CASCADE)
    class Meta:
        db_table = u'agente'

    def __str__(self):
        return self.apellido +" " +self.nombres    
#··························································································································································     
class Tipolesion(models.Model):
    idtipolesion = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'tipolesion'
    
    def __str__(self):
        return self.descripcion        

#··························································································································································        
class Adscripcion(models.Model):
    idadscripcion = models.AutoField(primary_key=True,verbose_name='Adscripcion')
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,verbose_name='Agente',on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True,verbose_name='Fecha')
    lugar = models.CharField(max_length=200, blank=True,verbose_name='Lugar')
    nroresolucion = models.CharField(max_length=200, blank=True,verbose_name='Nro Resolución')
    funcion = models.CharField(max_length=200, blank=True,verbose_name='Función')
    observacion = models.CharField(max_length=200, blank=True,verbose_name='Observaciones')
    class Meta:
        db_table = u'adscripcion'

    def __str__(self):
        return self.descripcion
        
#··························································································································································        
class Vinculo(models.Model):
    idvinculo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'vinculo'
    
    def __str__(self):
        return self.descripcion        
#··························································································································································        
class Asignacionfamiliar(models.Model):
    idasigfam = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,verbose_name='Apellido y Nombre',on_delete=models.CASCADE)
    tipodocumento = models.CharField(max_length=200, blank=True, choices = TIPO_DOC,verbose_name='Tipo Documento')
    nrodocumento = models.IntegerField(null=True, blank=True,verbose_name='Número de Documento')
    apellidoynombre = models.CharField(max_length=200, blank=True,verbose_name='Apellido y Nombre de Familiar')
    sexo = models.CharField(max_length=200, blank=True,choices=TIPO_SEXO)
    vinculo = models.ForeignKey(Vinculo, null=True, db_column='vinculo', blank=True,verbose_name='Vínculo',on_delete=models.CASCADE)
    fechanacimiento = models.DateField(null=True, blank=True,verbose_name='Fecha de Nacimiento')
    discapacidad = models.BooleanField(blank=True)
    fechaacontecimiento = models.DateField(null=True, blank=True,verbose_name='Fecha del Acotencimiento')
    codflia = models.CharField(max_length=200, blank=True)
    observaciones = models.CharField(max_length=200, blank=True)
    pagasalario = models.BooleanField(blank=True,verbose_name='Paga de Salario')
    pagaflianrosa = models.BooleanField(blank=True,verbose_name='Paga por Familia Numerosa')
    
    class Meta:
        db_table = u'asignacionfamiliar'
        unique_together = ("nrodocumento","idagente")
     
    def __str__(self):
        return self.apellidoynombre       

#··························································································································································        
class Traslado(models.Model):
    idtraslado = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, db_column='idagente',blank=True,null=True,on_delete=models.CASCADE)
    agrupamiento = models.ForeignKey(Agrupamiento,related_name='agrupamiento', db_column='agrupamiento',null=True, blank=True,on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, related_name='Clase' ,db_column='clase',null=True, blank=True,on_delete=models.CASCADE)
    categoria = models.IntegerField(null=True, blank=True)
    claseac = models.ForeignKey(Clase, related_name='clase_ac' ,db_column='claseac',null=True, blank=True,on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, related_name='zona' ,db_column='zona',null=True, blank=True,on_delete=models.CASCADE)
    nuevoagrupamiento = models.ForeignKey(Agrupamiento, related_name='nuevoagrupamiento', db_column='nuevoagrupamiento',null=True, blank=True,on_delete=models.CASCADE)
    nuevaclase = models.ForeignKey(Clase, related_name='nuevaclase' ,db_column='nuevaclase',null=True, blank=True,on_delete=models.CASCADE)
    nuevacategoria = models.IntegerField(null=True, blank=True)
    nuevaclaseac = models.ForeignKey(Clase, related_name='nuevaclaseac' ,db_column='nuevaclaseac',null=True, blank=True,on_delete=models.CASCADE)
    nuevazona = models.ForeignKey(Zona, related_name='nuevazona' ,db_column='nuevazona',null=True, blank=True,on_delete=models.CASCADE)
    nuevadireccion = models.ForeignKey(Direccion, related_name='nuevadireccion' ,db_column='nuevadireccion',null=True, blank=True,on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, related_name='direccion' ,db_column='direccion',null=True, blank=True,on_delete=models.CASCADE)
    observacion = models.CharField(max_length=200, blank=True)
    fechahasta = models.DateField(null=True, blank=True)
    fechad = models.DateField(db_column='fechadesde', null=True, blank=True)
    class Meta:
        db_table = u'traslado'
     
    def __str__(self):
        return self.apellidoynombre     
#··························································································································································        
class Licenciaanualagente(models.Model):
    idlicanualagen = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,on_delete=models.CASCADE)
    anio = models.IntegerField(null=True, blank=True)
    cantidaddias = models.SmallIntegerField(null=True, blank=True)
    diastomados = models.SmallIntegerField(null=True, blank=True)
    resta = models.BooleanField()
    class Meta:
        db_table = u'licenciaanualagente'
    
    def __str__(self):
        return self.apellidoynombre        
#··························································································································································
class Sancion(models.Model):
    idsancion = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,verbose_name='Agente',on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True,verbose_name='Fecha')
    tiposancion = models.CharField(max_length=200, choices=TIPO_SANCION, blank=True,verbose_name='Tipo Sanción')
    observaciones = models.CharField(max_length=200, blank=True,verbose_name='Observaciones')
    cantidaddias = models.SmallIntegerField(null=True, blank=True,verbose_name='Cantidad de Dias')
    class Meta:
        db_table = u'sancion'
 
    def __str__(self):
        return self.apellidoynombre             

#··························································································································································

class Ausentismo(models.Model):
    idausentismo = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    idarticulo = models.ForeignKey(Articulo, null=True, db_column='idarticulo', blank=True,on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=200, blank=True)
    tiempolltarde = models.TimeField(blank=True) # This field type is a guess.
    #medica = models.ForeignKey(Medica, null=True, db_column='medica', blank=True)
    direccion = models.ForeignKey(Direccion, null=True, db_column='direccion', blank=True, default = 0,on_delete=models.CASCADE)
    class Meta:
        db_table = u'ausentismo'
        unique_together = ("idagente","fecha")
    
    def __str__(self):
        return self.apellidoynombre        

#··························································································································································        


class Ausent(models.Model):
    idausent = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True, verbose_name= "Agente",on_delete=models.CASCADE)
    fechainicio = models.DateField(verbose_name= "Fecha Inicio")
    cantdias = models.SmallIntegerField()
    fechafin = models.DateField(blank=True, verbose_name= "Fecha Fin")
    idarticulo = models.ForeignKey(Articulo, db_column='idarticulo', verbose_name= "Artìculo",on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=200, blank=True)
    tiempolltarde = models.TimeField(blank=True) # This field type is a guess.
    direccion = models.ForeignKey(Direccion, null=True, db_column='direccion', blank=True, default = 0,on_delete=models.CASCADE)
    class Meta:
        db_table = u'ausent'
        #unique_together = ("idagente","fecha")
    def __str__(self):
        return str(self.fechafin)
        
    def save(self, *args, **kwargs):
        inicio = self.fechainicio
        dias = self.cantdias -1
        self.fechafin = inicio+timedelta(days=dias)
        super(Ausent, self).save(*args, **kwargs)

#··························································································································································        
class Accidentetrabajo(models.Model):
    idaccidente = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,verbose_name='Apellido y Nombre',on_delete=models.CASCADE)
    nroexpediente = models.CharField(max_length=200, null=True, blank=True,verbose_name='Número Expendiente')
    fecha = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    testigos = models.CharField(max_length=200, blank=True)
    #tipolesion = models.ForeignKey(Tipolesion, null=True, db_column='tipolesion', blank=True)
    detallelesion = models.CharField(max_length=200, blank=True,verbose_name='Detalle Lesión')
    circunstancia = models.CharField(max_length=200, blank=True)
    nrosiniestroart = models.CharField(max_length=200, blank=True,verbose_name='Número Siniestro')
    nroexposicion = models.CharField(max_length=200, blank=True,verbose_name='Número Exposición')
    comisaria = models.CharField(max_length=200, blank=True)
    edad = models.SmallIntegerField(null=True, blank=True)
    horario = models.CharField(max_length=200, blank=True)
    funcion = models.CharField(max_length=200, blank=True,verbose_name='Función')
    funcioncircunstancial = models.CharField(max_length=200, blank=True,verbose_name='Función Circunstancial')
    fechaalta = models.DateField(null=True, blank=True,verbose_name='Fecha Alta')
    consecuelas = models.BooleanField(blank=True)
    porcincapacid = models.SmallIntegerField(null=True, blank=True)
    zona = models.CharField(max_length=200, blank=True)
    resolucion = models.CharField(max_length=200, blank=True)
    resolucionsumario = models.CharField(max_length=200, blank=True,verbose_name='Resolución Sumario')
    observaciones = models.CharField(max_length=200, blank=True)
    secuelas = models.CharField(max_length=200, blank=True)
    idausent = models.ForeignKey(Ausent, null=True, db_column='idausent', blank=True,on_delete=models.CASCADE)
    class Meta:
        db_table = u'accidentetrabajo'
    
    def __str__(self):
        return self.nroexpediente        
        
#··························································································································································        
class Certificadoaccidente(models.Model):
    idcertif = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,on_delete=models.CASCADE)
    fechadesde = models.DateField(null=True, blank=True)
    detalle = models.CharField(max_length=200, blank=True)
    fechahasta = models.DateField(null=True, blank=True)
    nroexpediente = models.CharField(null=True, blank=True,max_length=20)
    idaccidentetrabajo = models.ForeignKey(Accidentetrabajo, null=True, db_column='idaccidentetrabajo', blank=True,on_delete=models.CASCADE)
    
    class Meta:
        db_table = u'certificadoaccidente'
    
    def __str__(self):
        return self.nroexpediente        
        
#··························································································································································
class Licenciaanual(models.Model):
    idlicanual = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True, verbose_name='Agente',on_delete=models.CASCADE)
    idausent = models.ForeignKey(Ausent, null=True, db_column='idausent', blank=True, verbose_name='Fecha Hasta',on_delete=models.CASCADE)
    anio = models.IntegerField(null=True, blank=True, verbose_name="Año")
    tipo = models.CharField(max_length=200, blank=True,choices=TIPO_LICANUAL)
    fechadesde = models.DateField(null=True, blank=True)
    cantdias = models.SmallIntegerField(null=True, blank=True)
    observaciones = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'licenciaanual'
        unique_together = ("fechadesde", "idagente", "tipo")
    #def __str__(self):
     #   return tipo
        
#··························································································································································        
TIPO_MEDICA = (
	(18,"Atención de familiar - Artículo 18"),
	(101,"Enfermedad - Artículo 10-1"),
	(102,"Enfermedad - Artículo 10-2"),
)

TIPO_ALTA_MEDICA = (
	(0,"Sin alta"),
	(1,"Alta normal"),
	(2,"Tareas pasivas"),
	(3,"Alta transitoria"),
)
class Medica(models.Model):
    id_medica = models.AutoField(primary_key=True,verbose_name='Medica')
    agente = models.ForeignKey(Agente, null=True, db_column='agente', blank=True,verbose_name='Agente',on_delete=models.CASCADE)
    idausent = models.ForeignKey(Ausent, null=True, db_column='idausent', blank=True,on_delete=models.CASCADE)
    expediente = models.CharField(max_length=200, blank=False,verbose_name='Expediente')
    diagnostico = models.CharField(max_length=200, blank=False,verbose_name='Diagnostico')
    funcion = models.CharField(max_length=200, blank=True,verbose_name='Función')
    tipoalta = models.IntegerField(null=True, blank=True, choices=TIPO_ALTA_MEDICA, verbose_name='Tipo Alta')
    fechaalta = models.DateField(null=True, blank=True,verbose_name='Fecha Alta')
    observaciones = models.CharField(max_length=200, blank=True,verbose_name='Observaciones')
    fliaratendido = models.CharField(max_length=200, blank=True,verbose_name='Familiar Atendido')
    resolucion = models.CharField(max_length=200, blank=True,verbose_name='Resolución')

    class Meta:
        db_table = u'medica'
    
    def __str__(self):
        return self.expediente

#··························································································································································        


class Juntamedica(models.Model):
    idjuntamedica = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    resultado = models.CharField(max_length=200, blank=True)
    medica = models.ForeignKey(Medica, null=True, db_column='medica', blank=True,on_delete=models.CASCADE)
    class Meta:
        db_table = u'juntamedica'
    
    def __str__(self):
        return self.idagente
        
#··························································································································································

class Licenciamedica(models.Model):
    idlicmedica = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,on_delete=models.CASCADE)
    idarticulo = models.ForeignKey(Articulo, null=True, db_column='idarticulo', blank=True,on_delete=models.CASCADE)
    anio = models.IntegerField(null=True, blank=True)
    tipo = models.CharField(max_length=200, blank=True)
    fechadesde = models.DateField(null=True, blank=True)
    cantdias = models.SmallIntegerField(null=True, blank=True)
    observaciones = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'licenciamedica'
    
    def __str__(self):
        return self.idagente        

#··························································································································································        
class Estudiocursado(models.Model):
    idestcur = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,on_delete=models.CASCADE)
    ciclo = models.CharField(max_length=200, blank=True)
    establecimiento = models.CharField(max_length=200, blank=True)
    titulo = models.CharField(max_length=200, blank=True)
    duracion = models.CharField(max_length=200, blank=True)
    observaciones = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'estudiocursado'
    
    def __str__(self):
        return self.idagente        
#··························································································································································        
class Servicioprestado(models.Model):
    idservprest = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,verbose_name='Agente',on_delete=models.CASCADE)
    fechadesde = models.DateField(null=True, blank=True,verbose_name='Fecha Desde')
    fechahasta = models.DateField(null=True, blank=True,verbose_name='Fecha Hasta')
    empresa = models.CharField(max_length=200, blank=True,verbose_name='Empresa')
    estatal = models.BooleanField(blank=True,verbose_name='Estatal')
    cajaaporte = models.CharField(max_length=200, blank=True,verbose_name='Caja Aporte')
    nroafiliacion = models.CharField(max_length=200, blank=True,verbose_name='Nro Afiliación')
    observaciones = models.CharField(max_length=200, blank=True,verbose_name='Observaciones')
    tarea = models.CharField(max_length=200, blank=True,verbose_name='Tarea')
    class Meta:
        db_table = u'servicioprestado'
    
    def __str__(self):
        return self.idagente        
#··························································································································································        
class Licencia(models.Model):
    idlicencia = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,on_delete=models.CASCADE)
    anio = models.IntegerField(null=True, blank=True)
    idarticulo = models.ForeignKey(Articulo, null=True, db_column='idarticulo', blank=True,on_delete=models.CASCADE)
    diastomados = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'licencia'
    
    def __str__(self):
        return self.idagente        
#··························································································································································        
class Seguro(models.Model):
    idseguro = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,verbose_name='Apellido y Nombre',on_delete=models.CASCADE)
    nropoliza = models.CharField(max_length=200, blank=True,verbose_name='Número de Poliza')
    observaciones = models.CharField(max_length=200, blank=True,verbose_name='Observaciones')
    obligatorio = models.BooleanField(blank=True,verbose_name='Obligatiorio')
    colectivoflia = models.BooleanField(blank=True)
    adicional = models.BooleanField(blank=True,verbose_name='Adicional')
    adicionalxco = models.BooleanField(blank=True)
    class Meta:
        db_table = u'seguro'
    
    def __str__(self):
        return self.idagente        
#··························································································································································        
class Salida(models.Model):
    idsalida = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,verbose_name='Apellido y Nombre',on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True,verbose_name='Fecha')
    horasalida = models.TimeField(blank=True,verbose_name='Hora Salida')
    horaregreso = models.TimeField(blank=True,verbose_name='Hora Regreso')
    oficial = models.BooleanField(blank=True,verbose_name='Oficial')
    observaciones = models.CharField(max_length=200, blank=True,verbose_name='Observaciones')
    class Meta:
        db_table = u'salida'
        unique_together = ("idagente","horasalida","fecha")
    
    def __str__(self):
        return self.idagente       

#··························································································································································        
class Escolaridad(models.Model):
    idescolaridad = models.AutoField(primary_key=True)
    anio = models.IntegerField(db_column='anio', blank=True,verbose_name='Año') # This field type is a guess.
    establecimiento = models.CharField(max_length=200, blank=True,verbose_name='Establecimiento')
    tipoescolaridad = models.CharField(max_length=200, blank=True, choices=TIPO_ESCO,verbose_name='Nivel')
    periodoescolar = models.CharField(max_length=200, blank=True,verbose_name='Período Escolar')
    gradocrusado = models.CharField(max_length=200, blank=True,verbose_name='Grado Cursado')
    idasigfam = models.ForeignKey(Asignacionfamiliar, db_column='idasigfam',verbose_name='Apellido y Nombre', null=True,on_delete=models.CASCADE)
    
    
    class Meta:
        db_table = u'escolaridad'
        unique_together = ("idasigfam","anio")
    
    def __str__(self):
        return self.gradocrusado       

#··························································································································································        
class ArtiTomados(models.Model):
    idartitom = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,verbose_name='Apellido y Nombre',on_delete=models.CASCADE)
    anio = models.IntegerField(db_column='anio', blank=True,verbose_name='Año') # This field type is a guess.
    mes = models.IntegerField(db_column='mes', blank=True,verbose_name='Mes') # This field type is a guess.
    idarticulo = models.ForeignKey(Articulo, null=True, db_column='idarticulo', blank=True,on_delete=models.CASCADE)
    diastomados = models.IntegerField(db_column='diastomados', verbose_name='Dias tomados') # This field type is a guess.
    tiempolltarde = models.TimeField(blank=True)
    class Meta:
        db_table = u'articulos_tomados'
    #def __unicode__(self):
    #    return force_unicode()
    
    
class Evaluador(models.Model):
    idevalua = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,verbose_name='Apellido y Nombre',on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200, blank=True,verbose_name='Descripción')
    
    class Meta:
        db_table = u'evaluador'
        
class Calificacion(models.Model):
     idcalificacion = models.AutoField(primary_key=True)
     periodo = models.IntegerField(db_column='periodo',verbose_name='Periodo')
     fecha = models.DateField(null=True, blank=True,verbose_name='Fecha')
     evaluador = models.ForeignKey(Evaluador, db_column='evaluador',verbose_name='Evaluador',on_delete=models.CASCADE)
     observaciones = models.CharField(max_length=200, blank=True,verbose_name='Observaciones')
     ultimoAscenso = models.DateField(null=True, blank=True,verbose_name='Ultimo ascenso')
     proximoAscenso = models.DateField(null=True, blank=True,verbose_name='Proximo ascenso')
     agente = models.ForeignKey(Agente, db_column='agente',verbose_name='Agente evaluado',on_delete=models.CASCADE)
     puntaje = models.IntegerField(db_column='puntaje',verbose_name='Puntaje')
     
     class Meta:
         db_table = u'calificacion'
#***********************************************************************************************$
#***MODELOS-DJANGO******************************************************************************$
#***********************************************************************************************$

class UserPerso(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    is_superuser = models.BooleanField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = u'auth_user'
    
    def __str__(self):
        return self.username

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        db_table = u'django_content_type'
    
    def __str__(self):
        return self.name

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = u'django_session'
    
    def __str__(self):
        return self.session_data

class Log(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(UserPerso,on_delete=models.CASCADE)
    content_type = models.ForeignKey(DjangoContentType,on_delete=models.CASCADE)
    object_id = models.TextField()
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = u'django_admin_log'
    
    def __str__(self):
        return self.user

class Cambios(models.Model):
    idcambio = models.AutoField(primary_key=True)
    #usuario = models.ForeignKey(UserPerso)
    usuario = models.CharField(max_length=100, db_column='usuario_id')
    modelo = models.CharField(max_length=100)
    tipocambio = models.CharField(max_length=200)
    horario = models.DateTimeField(auto_now_add=True, blank=True)
    valorold = models.CharField(max_length=200)
    valornew = models.CharField(max_length=200)

    class Meta:
        db_table = u'cambios'
    
    def __str__(self):
        return self.usuario


class HistorialDireccion(models.Model):
    idhistdir = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,verbose_name='Apellido y Nombre',on_delete=models.CASCADE)
    iddireccion = models.ForeignKey(Direccion, null=True, db_column='iddireccion', blank=True, verbose_name = "Dirección",on_delete=models.CASCADE)
    fechacambio = models.DateTimeField(auto_now_add=True, blank=True)
    
    class Meta:
        db_table = u'historialdireccion'
    
    def __str__(self):
        return self.idagente
        
#------------------------------------------ Tablas Viejas -----------------------------------------------------------------        

class Licenciaanualvieja(models.Model):
    id_licenciaanualvieja = models.AutoField(primary_key=True)
    id_agente = models.ForeignKey(Agente, null=True, db_column='id_agente', blank=True,on_delete=models.CASCADE)
    nrolegajo = models.IntegerField()
    anio = models.IntegerField(null=True, blank=True)
    tipo = models.CharField(max_length=200, blank=True,choices=TIPO_LICANUAL)
    fechadesde = models.DateField(null=True, blank=True)
    cantdias = models.SmallIntegerField(null=True, blank=True)
    observaciones = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'licenciaanualvieja'
        unique_together = ("fechadesde", "id_agente", "tipo")
    
    def __str__(self):
        return str(self.fechadesde)   
#··························································································································································        


class Juntamedicavieja(models.Model):
    idjuntamedicavieja = models.AutoField(primary_key=True)
    idagente = models.ForeignKey(Agente, null=True, db_column='idagente', blank=True,on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    resultado = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'juntamedicavieja'
    
    def __str__(self):
        return self.idagente
        
        
class Medicavieja(models.Model):
    id_medicavieja = models.AutoField(primary_key=True,verbose_name='Medica Vieja')
    nrolegajo = models.IntegerField()
    id_articulo = models.ForeignKey(Articulo, null=True, db_column='id_articulo', blank=True,on_delete=models.CASCADE)
    fechadesde = models.DateField()
    fechahasta = models.DateField()
    expediente = models.CharField(max_length=200, verbose_name='Expediente')
    diagnostico = models.CharField(max_length=200, verbose_name='Diagnostico')
    funcion = models.CharField(max_length=200, verbose_name='Función')
    tipoalta = models.IntegerField(null=True, blank=True,verbose_name='Tipo Alta')
    observaciones = models.CharField(max_length=200, blank=True,verbose_name='Observaciones')
    fliaratendido = models.CharField(max_length=200, blank=True,verbose_name='Familiar Atendido')
    resolucion = models.CharField(max_length=200, blank=True,verbose_name='Resolución')    
    agente = models.ForeignKey(Agente, null=True, db_column='agente', blank=True,verbose_name='Agente',on_delete=models.CASCADE)
    juntamedicavieja = models.ForeignKey(Juntamedicavieja, null=True, db_column='juntamedica', blank=True,on_delete=models.CASCADE)

    class Meta:
        db_table = u'medicavieja'
    
    def __str__(self):
        return self.expediente
