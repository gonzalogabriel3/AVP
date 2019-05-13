# -*- coding: utf-8 -*-
from django import forms
from personal.models import *
from django.contrib.admin import widgets
from django.forms.widgets import *
from django.forms.fields import DateField
from django.forms.fields import TimeField
#from django.forms import *
from datetime import date
from django.forms.widgets import SplitDateTimeWidget
from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import SelectDateWidget
from .models import *
  
#CALENDARIO = widgets.AdminDateWidget()

TIEMPO = SplitDateTimeWidget()
fecha = date.today()
#widget1 = forms.extras.widgets.SelectDateWidget(years=range(1920, (fecha.year - 17)).reverse())
widget1 = SelectDateWidget(years=range(1920, (fecha.year + 1)))
#widget2 = forms.extras.widgets.SelectDateWidget(years=range(1970, (fecha.year + 1)).reverse())
widget2 = SelectDateWidget(years=range((fecha.year+1),1970,-1))
#widget3 = forms.extras.widgets.SelectDateWidget(years=range(1990, (fecha.year + 1)).reverse())
widget3 = SelectDateWidget(years=range(1990, (fecha.year + 2)))
widget4 = SelectDateWidget(years=range(1990, (fecha.year + 1)))
        

class IngresarArticulo(forms.ModelForm):
    
    class Meta:
        model=Articulo
        fields = ('idarticulo','descripcion', 'eslicencia', 'maxanual', 'maxmensual')
        
class formAusentismo(forms.ModelForm):
    
    cantdias = forms.IntegerField()
    class Meta:
        model  = Ausentismo
        fields = ('idagente', 'idarticulo', 'fecha', 'tiempolltarde', 'direccion', 'observaciones')
    def __init__(self, *args, **kwargs):
        super(formAusentismo, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['fecha'].widget = widget2
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'
        self.fields['direccion'].widget.attrs['disabled'] = 'disabled'
        self.fields['idarticulo'].queryset = Articulo.objects.order_by('descripcion')

class formAusent(forms.ModelForm):
    
    cantdias = forms.IntegerField()
    fechainicio = forms.DateField(label="Fecha Inicio",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'datepickerAusentismo','data-date-format':'dd/mm/yyyy'}))
    #fechafin = forms.DateField(label="Fecha Fin",widget=forms.TextInput(attrs={'id':'dp2','class':'datepicker','data-date-format':'yyyy-mm-dd'}))
    class Meta:
        model  = Ausent
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(formAusent, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'
        self.fields['direccion'].widget.attrs['disabled'] = 'disabled'
        self.fields['fechafin'].widget.attrs['disabled'] = 'disabled'
        self.fields['cantdias'].widget.attrs['min']=1
        #self.fields['idarticulo'].queryset = Articulo.objects.filter(~Q(descripcion = 'L. A. R.')).order_by('descripcion')#Articulo.objects.order_by('descripcion')



class formAgente(forms.ModelForm):
    fechaalta = forms.DateField(label="Fecha Alta",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    fechabaja = forms.DateField(required=False,label="Fecha Baja",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp3','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    fechanacimiento=forms.DateField(label="Fecha de nacimiento",widget=forms.DateInput(attrs=
                                {
                                    'class':'datepicker',
                                    'placeholder':'Fecha de nacimiento'

                                }))
    nrolegajo = forms.IntegerField(label="N° legajo",min_value=0,widget = forms.NumberInput())
    apellido = forms.CharField(min_length=3,max_length=100,label="Apellido",widget = forms.TextInput())
    nombres = forms.CharField(min_length=3,max_length=100,label="Nombres",widget = forms.TextInput())
    tipodoc = forms.ChoiceField(choices=TIPO_DOC,label="Tipo de documento")
    nrodocumento = forms.IntegerField(label="Documento",widget = forms.NumberInput())
    sexo = forms.ChoiceField(choices=TIPO_SEXO)
    nacionalidad = forms.ModelChoiceField(queryset=Nacionalidad.objects.all(),label="Nacionalidad")
    estadocivil = forms.ChoiceField(required=False,choices=TIPO_ECIVIL)
    codigopostal = forms.ModelChoiceField(queryset=Codigopostal.objects.all(),label="Codigo postal")
    domicilio = forms.CharField(required=False,min_length=3,max_length=100,label="Domicilio",widget = forms.TextInput())
    telefono = forms.CharField(required=False,min_length=3,max_length=100,label="Telefono",widget = forms.TextInput())
    cargo = forms.ChoiceField(choices=TIPO_CARGO)
    antigranios = forms.IntegerField(required=False,label="Antigüedad R. en Años",min_value=0,widget = forms.NumberInput())
    antigrmeses = forms.IntegerField(required=False,label="Antigüedad R. en Meses",min_value=0,widget = forms.NumberInput())
    antigrvanios = forms.IntegerField(required=False,label="Antigüedad R. V. en Años",min_value=0,widget = forms.NumberInput())
    antigrvmeses = forms.IntegerField(required=False,label="Antigüedad R. V. en Meses",min_value=0,widget = forms.NumberInput())
    antigravpanios = forms.IntegerField(required=False,label="Antigüedad R. AVP en Años",min_value=0,widget = forms.NumberInput())
    antigravpmeses = forms.IntegerField(required=False,label="Antigüedad R. AVP en Meses",min_value=0,widget = forms.NumberInput())
    situacion = forms.ChoiceField(choices=TIPO_SITUACION)
    razonbaja = forms.CharField(required=False,min_length=3,max_length=100,label="Razon baja")
    clase = forms.ModelChoiceField(queryset=Clase.objects.all(),label="Clase")
    categoria = forms.ChoiceField(choices=TIPO_CATEGORIA)
    titulo = forms.ChoiceField(required=False,choices=TIPO_TITULO)
    planta = forms.ChoiceField(required=False,choices=TIPO_PLANTA)
    agrupamiento = forms.ModelChoiceField(required=False,queryset=Agrupamiento.objects.all(),label="Agrupamiento")
    iddireccion = forms.ModelChoiceField(queryset=Direccion.objects.all(),label="Direccion")
    iddireccionreal = forms.ModelChoiceField(queryset=Direccion.objects.all(),label="Direccion real")
    nrocuenta = forms.CharField(required=False,max_length=100,label="N° cuenta",widget = forms.TextInput())
    nrocontrato = forms.CharField(required=False,max_length=100,label="N° contrato",widget = forms.TextInput())
    nrolegajosueldos = forms.CharField(required=False,max_length=100,label="N° Legajos Sueldos",widget = forms.TextInput())
    observaciones = forms.CharField(required=False,max_length=100,label="Observaciones",widget = forms.TextInput())
    total102 = forms.IntegerField(required=False,label="Total art. 102",min_value=0,widget = forms.NumberInput(attrs={'readonly':True}))
    seccion = forms.CharField(required=False,max_length=100,label="Seccion",widget = forms.TextInput())
    dexc = forms.BooleanField(required=False,label="Dedicacion intesiva")
    defun = forms.BooleanField(required=False,label="Defun")
    funcion = forms.ModelChoiceField(required=False,queryset=Funcion.objects.all(),label="Funcion")
    idcargof = forms.ModelChoiceField(queryset=CargoFuncion.objects.all(),label="Cargo Funcion")
    idzona = forms.ModelChoiceField(queryset=Zona.objects.all(),label="Zona")
    idzonareal = forms.ModelChoiceField(queryset=Zona.objects.all(),label="Zona real")
    claseac = forms.ModelChoiceField(queryset=Clase.objects.all(),label="Clase a cargo")

    class Meta:
        model  = Agente
        exclude=['idagente']
        
        
class formFamiliaresac(forms.ModelForm):
    fechanacimiento = forms.DateField(label="Fecha Nacimiento",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    fechaacontecimiento = forms.DateField(label="Fecha Acontecimiento",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    
    class Meta:
        model  = Asignacionfamiliar
        fields = ('idagente', 'tipodocumento', 'nrodocumento', 'apellidoynombre','sexo','vinculo','fechanacimiento','discapacidad','fechaacontecimiento','codflia','observaciones','pagasalario','pagasalario','pagaflianrosa')
    def __init__(self, *args, **kwargs):
        super(formFamiliaresac, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'
        
      
class formAccdetrabajo(forms.ModelForm):
    fecha = forms.DateField(label="Fecha",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    fechaalta = forms.DateField(label="Fecha Alta",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    
    class Meta:
        model  = Accidentetrabajo
        fields = ('idagente', 'nroexpediente', 'fecha', 'hora', 'testigos', 'detallelesion', 'circunstancia', 'nrosiniestroart', 'nroexposicion', 'comisaria', 'edad', 'horario', 'funcion', 'funcioncircunstancial', 'fechaalta', 'consecuelas', 'porcincapacid', 'zona', 'resolucion', 'resolucionsumario', 'observaciones', 'secuelas')#'tipolesion',
    def __init__(self, *args, **kwargs):
        super(formAccdetrabajo, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'

class formCertificadoaccidente(forms.ModelForm):
    fechadesde = forms.DateField(label="Fecha Desde",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    fechahasta = forms.DateField(label="Fecha Hasta",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    class Meta:
        model  = Certificadoaccidente
        fields = ('idagente', 'fechadesde', 'detalle', 'fechahasta', 'idaccidentetrabajo')
    def __init__(self, *args, **kwargs):
        super(formCertificadoaccidente, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'
        self.fields['idaccidentetrabajo'].widget.attrs['disabled'] = 'disabled'
        
class formSalida(forms.ModelForm):
    fecha = forms.DateField(label="Fecha ",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    class Meta:
        model  = Salida
        fields = ('idagente', 'fecha', 'horasalida', 'horaregreso', 'oficial', 'observaciones')
    def __init__(self, *args, **kwargs):
        super(formSalida, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        #if instance and instance.pk:
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'


class formTraslado(forms.ModelForm):
    fechad = forms.DateField(label="Fecha Desde",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    fechahasta = forms.DateField(label="Fecha Hasta",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp3','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    class Meta:
        model  = Traslado
        fields = ('idtraslado', 'idagente', 'agrupamiento', 'clase', 'categoria', 'claseac','zona','nuevoagrupamiento','nuevaclase','nuevacategoria','nuevaclaseac','nuevazona','nuevadireccion','direccion','observacion','fechad','fechahasta')
    def __init__(self, *args, **kwargs):
        super(formTraslado, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'

class formSeguro(forms.ModelForm):
    class Meta:
        model  = Seguro
        fields = ('idseguro', 'idagente', 'nropoliza', 'observaciones', 'obligatorio', 'colectivoflia','adicional','adicionalxco')     
        

class formServicioprestado(forms.ModelForm):
    fechadesde = forms.DateField(label="Fecha Desde",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    fechahasta = forms.DateField(label="Fecha Hasta",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp3','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    class Meta:
        model  = Servicioprestado
        fields = ('idservprest', 'idagente', 'fechadesde', 'fechahasta', 'empresa', 'estatal','cajaaporte','nroafiliacion','observaciones','tarea')
    def __init__(self, *args, **kwargs):
        super(formServicioprestado, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        #if instance and instance.pk:
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'

class formLicenciaanualagente(forms.ModelForm):
    class Meta:
        model  = Licenciaanualagente
        fields = ('idlicanualagen', 'idagente', 'anio', 'cantidaddias', 'diastomados', 'resta')                        

  
class formLicencia(forms.ModelForm):
    class Meta:
        model  = Licencia
        fields = ('idlicencia', 'idagente', 'anio', 'idarticulo', 'diastomados')                                                

class formSancion(forms.ModelForm):
    fecha = forms.DateField(label="Fecha",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    tiposancion = forms.ChoiceField(label="Tipo de sancion",choices=TIPO_SANCION)
    observaciones = forms.CharField(min_length=3,max_length=100,label="Observaciones",widget = forms.TextInput())
    cantidaddias = forms.IntegerField(label="Cantidad de dias",min_value=0,widget = forms.NumberInput())

    class Meta:
        model  = Sancion
        exclude = ['idsancion']

    def __init__(self, *args, **kwargs):
        super(formSancion, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'

class formAdscriptos(forms.ModelForm):
    fecha = forms.DateField(label="Fecha",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    class Meta:
        model  = Adscripcion
        fields = ('idagente', 'fecha', 'lugar', 'nroresolucion','funcion','observacion')
    def __init__(self, *args, **kwargs):
        super(formAdscriptos, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'

class formEstudiosCursados(forms.ModelForm):
    class Meta:
        model  = Estudiocursado
        fields = ('idagente', 'ciclo', 'establecimiento', 'titulo','duracion','observaciones')

class formArticulos(forms.ModelForm):
    class Meta:
        model  = Articulo
        fields = ('descripcion', 'eslicencia', 'maxanual', 'maxmensual')

class formLicenciaanual(forms.ModelForm):
    fechadesde = forms.DateField(required=True,label="Fecha Desde",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'datepickerAusentismo','data-date-format':'dd/mm/yyyy'}))
    fechahasta = forms.DateField(required=False,label="Fecha Hasta",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'datepickerAusentismo','data-date-format':'dd/mm/yyyy'}))
    
    class Meta:
        model  = Licenciaanual
        fields = ('idagente','anio','fechadesde','idausent','cantdias','tipo','observaciones')
        exclude=['idausent']

    def __init__(self, *args, **kwargs):
        super(formLicenciaanual, self).__init__(*args, **kwargs,)
        instance = getattr(self, 'instance', None)
        
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'
        #self.fields['idausent'].widget.attrs['disabled'] = 'disabled'
        self.fields['fechahasta'].widget.attrs['disabled'] = 'disabled'
        self.fields['anio'].widget.attrs['disabled'] = 'disabled'
        self.fields['cantdias'].widget.attrs['min']=1
        self.fields['tipo'].required=True
              
class formEscolaridad(forms.ModelForm):
    #idasigfam = forms.CharField(required=False,label="Apellido y Nombres",widget = forms.TextInput(attrs={'readonly':True}))
    anio = forms.IntegerField(label="Año",min_value=0,)
    establecimiento = forms.CharField(max_length=100,label="Establecimiento",widget = forms.TextInput())
    tipoescolaridad = forms.ChoiceField(label="Tipo",choices=TIPO_ESCO)
    periodoescolar = forms.CharField(max_length=100,label="Periodo escolar",widget = forms.TextInput())
    gradocrusado = forms.CharField(max_length=100,label="Grado cursado",widget = forms.TextInput())


    class Meta:
        model  = Escolaridad
        exclude =['idescolaridad','idasigfam']

    def __init__(self, *args, **kwargs):
        super(formEscolaridad, self).__init__(*args, **kwargs,)
        instance = getattr(self, 'instance', None)

        '''self.fields['idasigfam'].widget.attrs['required']=False
        self.fields['idasigfam'].widget.attrs['disabled']=True
        self.fields['idasigfam'].queryset=Escolaridad.objects.filter(idescolaridad=idescolaridad)'''


class formMedica(forms.ModelForm):
    fechaalta=forms.DateField(widget=forms.DateInput(attrs=
                                {
                                    'class':'datepicker',
                                    
                                }))

    class Meta:
        model  = Medica
        fields = ('agente', 'expediente', 'diagnostico', 'funcion','tipoalta','observaciones','fliaratendido','resolucion')
    def __init__(self, *args, **kwargs):
        super(formMedica, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        #self.fields['fechaalta'].widget = widget2
        #self.fields['agente'].widget.attrs['disabled'] = 'disabled'
        #self.fields['idausent'].widget.attrs['disabled'] = 'disabled'

        
class formJuntaMedica(forms.ModelForm):
    fecha = forms.DateField(label="Fecha",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'datepicker','data-date-format':'dd/mm/yyyy'}))
    class Meta:
        model  = Juntamedica
        fields = ('idagente','fecha', 'resultado', 'medica')
    def __init__(self, *args, **kwargs):
        super(formJuntaMedica, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        #if instance and instance.pk:
        self.fields['idagente'].widget.attrs['disabled'] = 'disabled'
        self.fields['medica'].widget.attrs['disabled'] = 'disabled'

class formJuntamedicavieja(forms.ModelForm):
    class Meta:
        model  = Juntamedicavieja
        fields = "__all__"
        
class formMedicavieja(forms.ModelForm):
    class Meta:
        model  = Medicavieja
        fields = "__all__"

class formLicenciaanualvieja(forms.ModelForm):
    class Meta:
        model  = Licenciaanualvieja
        fields = "__all__"


class formFeriado(forms.ModelForm):
    Fecha=forms.DateField(label="Fecha",widget=forms.DateInput(format='%d/%m/%Y',attrs={'class':'datepickerFeriado','data-date-format':'dd/mm/yyyy'}))
    #Fecha = forms.DateField(required=True,label="Fecha",widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'datepickerFeriado','data-date-format':'dd/mm/yyyy'}))
    lugar=forms.ModelChoiceField(required=True,label="Lugar",queryset=Zona.objects.all().order_by('-idzona'))
    class Meta:
        model = Feriado
        fields=('Fecha','descripcion','lugar')
        exclude=['idferiado']
    def __init__(self, *args, **kwargs):
        super(formFeriado, self).__init__(*args, **kwargs,)
        instance = getattr(self, 'instance', None)
        