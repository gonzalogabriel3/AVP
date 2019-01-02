# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.utils.encoding import force_unicode

# Create your models here.

#def prueba():
#	return

TEST = (
	("Uno","1"), 
	("Dos","2"), 
	("Tres","3"),
)


#----------------------------------------------------------------------------------------------------------------------------------

class MinMaxFloat(models.FloatField):
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super(MinMaxFloat, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value' : self.max_value}
        defaults.update(kwargs)
        return super(MinMaxFloat, self).formfield(**defaults)

#----------------------------------------------------------------------------------------------------

class Barras(models.Model):
     idbarra = models.IntegerField("Código de barras",primary_key=True, db_column='idBarra')
     codigo = models.CharField("Descripción",max_length=200)
     class Meta:
        db_table = u'barras'
        verbose_name_plural = "Código de Barra"
	verbose_name='Código de Barra'
#	help_text = u"Holaaaaaaa"
        
     def __unicode__(self):
        return force_unicode(self.codigo)

#----------------------------------------------------------------------------------------------------
class Cuentaspatrimoniales(models.Model):
     codigocuenta = models.SmallIntegerField("Código C. Patrimonial",primary_key=True, db_column='codigoCuenta') 
     descripcioncuenta = models.CharField("Desc C. Patrimonial",max_length=200, db_column='descripcionCuenta') 
     class Meta:
        db_table = u'cuentasPatrimoniales'
        verbose_name_plural ="Cuentas Patrimoniales"
     def __unicode__(self):
        return force_unicode(self.descripcioncuenta)
        
#----------------------------------------------------------------------------------------------------
class Unidadesmedidas(models.Model):
    descripcionunidad = models.CharField(max_length=4, db_column='descripcionUnidad') 
    idunidadmedida = models.IntegerField(primary_key=True, db_column='idUnidadMedida') 
    class Meta:
        db_table = u'unidadesMedidas'
        verbose_name_plural ="Unidad de Medida"        
    def __unicode__(self):
        return force_unicode(self.descripcionunidad)


class ArticuloDepositoAd(models.Model):
     idarticulodeposito = models.AutoField(primary_key=True, db_column='idArticuloDeposito')
     idarticulo = models.SmallIntegerField(db_column='idArticulo')
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem',verbose_name='Articulo') 
     direccion = models.CharField(max_length=200, db_column='direccion',verbose_name='Deposito')
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida',verbose_name='Unidad Medida')
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial', verbose_name='Nro Cta.Patrim')
     nroficha = models.SmallIntegerField(db_column='nroFicha',verbose_name='Nro Ficha')
     mueble = models.CharField(max_length=200,verbose_name='Mueble')
     casillero = models.CharField(max_length=200,verbose_name='Casillero')
     stmin = MinMaxFloat(db_column='stmin',max_value=1000000000000, min_value=0.0, verbose_name='Stock Min')
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Cod Barra')
     stock = models.FloatField()
     stockentrante = models.FloatField(db_column='stockEntrante',verbose_name='Stock Entrada')
     stocksaliente = models.FloatField(db_column='stockSaliente',verbose_name='Stock Salida')

     class Meta:
         db_table = u'depoAdmin'
         verbose_name_plural ="Listado Articulos (Stock depositos)"
     def __unicode__(self):
         return force_unicode(self.idarticulo)

#----------------------------------------------------------------------------------------------------

#--------------------------------------Movimiento de Articulos---------------------------------------

class ArticuloMov(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') 
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Código de barra', blank=True, default = 0) 
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida', verbose_name='Unidad Medida', blank=True) 
     class Meta:
        db_table = u'articulo'
        verbose_name_plural ="Movimiento de Artículos"
     def __unicode__(self):
        return force_unicode(self.descripcionitem)


#----------------------------------------------------------------------------------------------------

class MovArt(models.Model):
     idarticulo = models.ForeignKey(ArticuloMov, db_column='idArticulo', primary_key=True, verbose_name='Artículo')
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     fecha = models.DateField(db_column='fecha',verbose_name='Fecha') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     descripcion = models.CharField(max_length=200, db_column='descripcion', verbose_name=u'Acción') 
     direccion = models.CharField(max_length=200,verbose_name='Depósito')
     origdest = models.CharField(max_length=200, db_column='origdest') 
     deposito = models.CharField(max_length=200, db_column='deposito') 
     idaccion = models.CharField(max_length=200, db_column='id')
     nrocuentapatrimonial = models.CharField(max_length=200, db_column='nroCuentaPatrimonial')
     class Meta:
        db_table = u'movArt'
        verbose_name_plural ="Movimiento de Artículos"
     def __unicode__(self):
        return force_unicode(' ')


#----------------------------------------------------------------------------------------------------
class ArticuloMovRw(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') 
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Código de barra', blank=True, default = 0) 
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida', verbose_name='Unidad Medida', blank=True) 
     class Meta:
        db_table = u'articulo'
        verbose_name_plural ="Movimiento de Artículos Rawson"
     def __unicode__(self):
        return force_unicode(self.descripcionitem)


#----------------------------------------------------------------------------------------------------

class MovArtRw(models.Model):
     idarticulo = models.ForeignKey(ArticuloMovRw, db_column='idArticulo', primary_key=True, verbose_name='Artículo')
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     fecha = models.DateField(db_column='fecha',verbose_name='Fecha') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     descripcion = models.CharField(max_length=200, db_column='descripcion', verbose_name=u'Acción') 
     class Meta:
        db_table = u'movArtRw'
        verbose_name_plural ="Movimiento de Artículos"
     def __unicode__(self):
        return force_unicode(' ')

#----------------------------------------------------------------------------------------------------
class ArticuloMovTrevelin(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') 
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Código de barra', blank=True, default = 0) 
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida', verbose_name='Unidad Medida', blank=True) 
     class Meta:
        db_table = u'articulo'
        verbose_name_plural ="Movimiento de Artículos Trevelin"
     def __unicode__(self):
        return force_unicode(self.descripcionitem)


#----------------------------------------------------------------------------------------------------

class MovArtTrevelin(models.Model):
     idarticulo = models.ForeignKey(ArticuloMovTrevelin, db_column='idArticulo', primary_key=True, verbose_name='Artículo')
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     fecha = models.DateField(db_column='fecha',verbose_name='Fecha') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     descripcion = models.CharField(max_length=200, db_column='descripcion', verbose_name=u'Acción') 
     class Meta:
        db_table = u'movArtTrevelin'
        verbose_name_plural ="Movimiento de Artículos"
     def __unicode__(self):
        return force_unicode(' ')
#----------------------------------------------------------------------------------------------------

class ArticuloMovGaiman(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') 
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Código de barra', blank=True, default = 0) 
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida', verbose_name='Unidad Medida', blank=True) 
     class Meta:
        db_table = u'articulo'
        verbose_name_plural ="Movimiento de Artículos Gaiman"
     def __unicode__(self):
        return force_unicode(self.descripcionitem)


#----------------------------------------------------------------------------------------------------

class MovArtGaiman(models.Model):
     idarticulo = models.ForeignKey(ArticuloMovGaiman, db_column='idArticulo', primary_key=True, verbose_name='Artículo')
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     fecha = models.DateField(db_column='fecha',verbose_name='Fecha') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     descripcion = models.CharField(max_length=200, db_column='descripcion', verbose_name=u'Acción') 
     class Meta:
        db_table = u'movArtGaiman'
        verbose_name_plural ="Movimiento de Artículos"
     def __unicode__(self):
        return force_unicode(' ')


#----------------------------------------------------------------------------------------------------
class ArticuloMovEsquel(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') 
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Código de barra', blank=True, default = 0) 
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida', verbose_name='Unidad Medida', blank=True) 
     class Meta:
        db_table = u'articulo'
        verbose_name_plural ="Movimiento de Artículos Esquel"
     def __unicode__(self):
        return force_unicode(self.descripcionitem)


#----------------------------------------------------------------------------------------------------

class MovArtEsquel(models.Model):
     idarticulo = models.ForeignKey(ArticuloMovEsquel, db_column='idArticulo', primary_key=True, verbose_name='Artículo')
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     fecha = models.DateField(db_column='fecha',verbose_name='Fecha') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     descripcion = models.CharField(max_length=200, db_column='descripcion', verbose_name=u'Acción') 
     class Meta:
        db_table = u'movArtEsquel'
        verbose_name_plural ="Movimiento de Artículos"
     def __unicode__(self):
        return force_unicode(' ')


#----------------------------------------------------------------------------------------------------
class ArticuloMovMadryn(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') 
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Código de barra', blank=True, default = 0) 
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida', verbose_name='Unidad Medida', blank=True) 
     class Meta:
        db_table = u'articulo'
        verbose_name_plural ="Movimiento de Artículos Madryn"
     def __unicode__(self):
        return force_unicode(self.descripcionitem)


#----------------------------------------------------------------------------------------------------

class MovArtMadryn(models.Model):
     idarticulo = models.ForeignKey(ArticuloMovMadryn, db_column='idArticulo', primary_key=True, verbose_name='Artículo')
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     fecha = models.DateField(db_column='fecha',verbose_name='Fecha') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     descripcion = models.CharField(max_length=200, db_column='descripcion', verbose_name=u'Acción') 
     class Meta:
        db_table = u'movArtMadryn'
        verbose_name_plural ="Movimiento de Artículos"
     def __unicode__(self):
        return force_unicode(' ')


#----------------------------------------------------------------------------------------------------
class ArticuloMovSarmiento(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') 
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Código de barra', blank=True, default = 0) 
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida', verbose_name='Unidad Medida', blank=True) 
     class Meta:
        db_table = u'articulo'
        verbose_name_plural ="Movimiento de Artículos Sarmiento"
     def __unicode__(self):
        return force_unicode(self.descripcionitem)


#----------------------------------------------------------------------------------------------------

class MovArtSarmiento(models.Model):
     idarticulo = models.ForeignKey(ArticuloMovSarmiento, db_column='idArticulo', primary_key=True, verbose_name='Artículo')
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     fecha = models.DateField(db_column='fecha',verbose_name='Fecha') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     descripcion = models.CharField(max_length=200, db_column='descripcion', verbose_name=u'Acción') 
     class Meta:
        db_table = u'movArtSarmiento'
        verbose_name_plural ="Movimiento de Artículos"
     def __unicode__(self):
        return force_unicode(' ')



#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------
class Articulo(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') 
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Código de barra', blank=True) 
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida', verbose_name='Unidad Medida', blank=True) 
     equivalencia = models.CharField(max_length=200, db_column='equivalencia', blank=True, verbose_name=u'Equivalencia')
     class Meta:
        db_table = u'articulo'
        verbose_name_plural ="Listado de Artículos"
     def __unicode__(self):
        return force_unicode(self.descripcionitem)
     def get_unidadmedida(self):
	return '%s'%(self.unidadmedida)
     get_unidadmedida.short_description = 'Unidad Medida'

class VwArticulos(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') 
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem', verbose_name=u'Descripción') 
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Código de barra', blank=True, default = 0, null=True) 
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida', verbose_name='Unidad Medida')
     equivalencia = models.CharField(max_length=200, db_column='equivalencia', verbose_name=u'Equivalencia', blank=True)
     class Meta:
        db_table = u'VW_articulos'
        verbose_name_plural ="Artículo - (Altas, Bajas, Modificaciones)"
        verbose_name = "Artículo"
     def __unicode__(self):
        return force_unicode(self.descripcionitem)

#----------------------------------------------------------------------------------------------------
class Ciudad(models.Model):
     idciudad = models.AutoField(primary_key=True, db_column='idCiudad',verbose_name='Ciudad')
     codigopostal = models.SmallIntegerField(db_column='codigoPostal',verbose_name='Cód.Postal')
     nombre = models.CharField(max_length=200)

     class Meta:
        db_table = u'ciudad'
	verbose_name_plural ="Ciudad"
	verbose_name='Ciudad'
     def __unicode__(self):
        return force_unicode(self.nombre)
        
#----------------------------------------------------------------------------------------------------
class Deposito(models.Model):
     iddeposito = models.AutoField(primary_key=True, db_column='idDeposito', editable=False,verbose_name='Depósito')
     idciudad = models.ForeignKey(Ciudad, db_column='idCiudad',verbose_name='Ciudad') 
     telefono = models.CharField(max_length=200,verbose_name='Tel.')
     direccion = models.CharField(max_length=200,verbose_name='Dirección')

     class Meta:
        db_table = u'deposito'
	verbose_name_plural ="Depósito"
	verbose_name='Depósito'
     def __unicode__(self):
        return force_unicode(self.direccion)
        
#----------------------------------------------------------------------------------------------------------------------------------------------------
class Proveedor(models.Model):
     idproveedor = models.AutoField(primary_key=True, db_column='idProveedor') 
     razonsocial = models.CharField(max_length=200, db_column='razonSocial') 
     domicilio = models.CharField(max_length=200)
     ciudad =  models.ForeignKey(Ciudad, db_column='ciudad')
     telefono = models.CharField(max_length=200)

     class Meta:
         db_table = u'proveedor'
	 verbose_name_plural ="Proveedor"
     def __unicode__(self):
         return force_unicode(self.razonsocial)
     def get_fields(self):
         return [(field, field.value_to_string(self)) for field in Order._meta.fields]


#----------------------------------------------------------------------------------------------------------------------------------------------------
#===TRANSFERENCIAS==============================================================================================================================
#----------------------------------------------------------------------------------------------------------------------------------------------------
class Transferencia(models.Model):
     idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
     fechasalida = models.DateField(db_column='fechaSalida',verbose_name='FechaSalida') 
     fechaentrada = models.DateField(db_column='fechaEntrada', blank=True,verbose_name='FechaEntrada') 
     depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOut',verbose_name='DepoSalida') 
     confirmado = models.BooleanField(default=False)
     depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoIn',verbose_name='DepoEntrada') 
     entrega = models.CharField(max_length=200, db_column='entrega', blank=True, verbose_name='Entregado por')
     recibe  = models.CharField(max_length=200, db_column='recibe', blank=True, verbose_name='Recibido por')

     class Meta:
        db_table = u'transferencia'
	verbose_name_plural ="Transferencia"
     def __unicode__(self):
        return force_unicode(self.idtransferencia)

class Detalletrasferencia(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey(Transferencia, db_column='idTransferencia',verbose_name='Transferencia') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     cantidadconfirmada = MinMaxFloat(max_value=10000000000000, min_value=0.0, db_column='cantidadConfirmada',verbose_name='Cant.Confirmada')
     confirmado = models.BooleanField()
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')
     
     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia"
	 verbose_name='Detalle Transferencia'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
         return force_unicode('')

class VwTransfEntRw(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',editable=False,verbose_name='FechaSalida') 
    fechaentrada = models.DateField(db_column='fechaEntrada',verbose_name='FechaEntrada') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfEntRw',editable=False,verbose_name='Depo.Salida') 
    confirmado = models.BooleanField(default=False)
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfEntRw',editable=False,verbose_name='Depo.Entrada') 
    entrega = models.CharField(max_length=200, db_column='entrega', blank=True, verbose_name='Entregado por', default='-')
    recibe  = models.CharField(max_length=200, db_column='recibe', blank=False, verbose_name='Recibido por' )
    class Meta:
        db_table = u'VW_transfEntRw'
        verbose_name_plural ="Transferencias Entrada Rawson"
        verbose_name = "Transferencia Entrada"
    def __unicode__(self):
        return force_unicode(self.idtransferencia)    

class VwTransfSalRw(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',verbose_name='FechaSalida') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfSalRw', default=5, editable=False,verbose_name='Depo.Salida') 
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfSalRw',verbose_name='Depo.Entrada') 
    confirmado = models.BooleanField(default=False)
    entrega = models.CharField(max_length=200, db_column='entrega', blank=False, verbose_name='Entregado por')
    #recibe  = models.CharField(max_length=200, db_column='recibe', blank=True, verbose_name='Recibido por', editable=False, default='-')
    class Meta:
        db_table = u'transfSalRw'
        verbose_name_plural ="Transferencias Salida Rawson"
        verbose_name = "Transferencia Salida"

    def __unicode__(self):
        return force_unicode(self.idtransferencia)

class DetalleTransfEntRw(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey(VwTransfEntRw, db_column='idTransferencia',verbose_name='Transferencia') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     cantidadconfirmada = MinMaxFloat(max_value=10000000000000, min_value=0.0, db_column='cantidadConfirmada',verbose_name='Cant.Confirmada')
     confirmado = models.BooleanField()
     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia Entrada Rawson"
	 verbose_name='Detalle Transferencia Entrada'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class DetalleTransfSalRw(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey( VwTransfSalRw, db_column='idTransferencia',verbose_name='Transferencia')
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia Salida Rawson"
	 verbose_name='Detalle Transferencia Salida'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class VwTransfEntTrevelin(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',editable=False,verbose_name='FechaSalida') 
    fechaentrada = models.DateField(db_column='fechaEntrada',verbose_name='FechaEntrada') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfEntTrevelin',editable=False,verbose_name='Depo.Salida') 
    confirmado = models.BooleanField(default=False)
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfEntTrevelin',editable=False,verbose_name='Depo.Entrada') 
    entrega = models.CharField(max_length=200, db_column='entrega', blank=True, verbose_name='Entregado por', default='-')
    recibe  = models.CharField(max_length=200, db_column='recibe', blank=False, verbose_name='Recibido por' )
    class Meta:
        db_table = u'VW_transfEntTrevelin'
        verbose_name_plural ="Transferencias Entrada Trevelin"
        verbose_name = "Transferencia Entrada"
    def __unicode__(self):
        return force_unicode(self.idtransferencia)    

class VwTransfSalTrevelin(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',verbose_name='FechaSalida') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfSalTrevelin', default=6, editable=False,verbose_name='Depo.Salida') 
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfSalTrevelin',verbose_name='Depo.Entrada') 
    confirmado = models.BooleanField(default=False)
    entrega = models.CharField(max_length=200, db_column='entrega', blank=False, verbose_name='Entregado por')
    #recibe  = models.CharField(max_length=200, db_column='recibe', blank=True, verbose_name='Recibido por', editable=False, default='-')
    class Meta:
        db_table = u'transfSalTrevelin'
        verbose_name_plural ="Transferencias Salida Trevelin"
        verbose_name = "Transferencia Salida"

    def __unicode__(self):
        return force_unicode(self.idtransferencia)

class DetalleTransfEntTrevelin(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey(VwTransfEntTrevelin, db_column='idTransferencia',verbose_name='Transferencia') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     cantidadconfirmada = MinMaxFloat(max_value=10000000000000, min_value=0.0, db_column='cantidadConfirmada',verbose_name='Cant.Confirmada')
     confirmado = models.BooleanField()
     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia Entrada Trevelin"
	 verbose_name='Detalle Transferencia Entrada'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class DetalleTransfSalTrevelin(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey( VwTransfSalTrevelin, db_column='idTransferencia',verbose_name='Transferencia')
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia Salida Trevelin"
	 verbose_name='Detalle Transferencia Salida'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
        return force_unicode('')

        
class VwTransfEntMadryn(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',editable=False,verbose_name='FechaSalida') 
    fechaentrada = models.DateField(db_column='fechaEntrada',verbose_name='FechaEntrada') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfEntMadryn',editable=False,verbose_name='Depo.Salida') 
    confirmado = models.BooleanField(default=False)
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfEntMadryn',editable=False,verbose_name='Depo.Entrada') 
    entrega = models.CharField(max_length=200, db_column='entrega', blank=True, verbose_name='Entregado por', default='-')
    recibe  = models.CharField(max_length=200, db_column='recibe', blank=False, verbose_name='Recibido por' )
    class Meta:
        db_table = u'VW_transfEntMadryn'
        verbose_name_plural ="Transferencias Entrada Madryn"
        verbose_name = "Transferencia Entrada"
    def __unicode__(self):
        return force_unicode(self.idtransferencia)    

class VwTransfSalMadryn(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',verbose_name='FechaSalida') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfSalMadryn',default=2, editable=False,verbose_name='Depo.Salida') 
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfSalMadryn',verbose_name='Depo.Entrada') 
    confirmado = models.BooleanField(default=False)
    entrega = models.CharField(max_length=200, db_column='entrega', blank=False, verbose_name='Entregado por')
    #recibe  = models.CharField(max_length=200, db_column='recibe', blank=True, verbose_name='Recibido por', editable=False, default='-')
    class Meta:
        db_table = u'transfSalMadryn'
        verbose_name_plural ="Transferencias Salida Madryn"
        verbose_name = "Transferencia Salida"

    def __unicode__(self):
        return force_unicode(self.idtransferencia)
    
    

class DetalleTransfEntMadryn(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey(VwTransfEntMadryn, db_column='idTransferencia',verbose_name='Transferencia') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     cantidadconfirmada = MinMaxFloat(max_value=10000000000000, min_value=0.0, db_column='cantidadConfirmada',verbose_name='Cant.Confirmada')
     confirmado = models.BooleanField()
     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia Entrada Madryn"
	 verbose_name='Detalle Transferencia Entrada'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class DetalleTransfSalMadryn(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey( VwTransfSalMadryn, db_column='idTransferencia',verbose_name='Transferencia')
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia Salida Madryn"
	 verbose_name='Detalle Transferencia Salida'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
        return force_unicode('')


class VwTransfEntGaiman(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',editable=False,verbose_name='FechaSalida') 
    fechaentrada = models.DateField("Fecha de Entrada",db_column='fechaEntrada') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfEntGaiman',editable=False,verbose_name='Depo.Salida') 
    confirmado = models.BooleanField(default=False)
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfEntGaiman',editable=False,verbose_name='Depo.Entrada') 
    entrega = models.CharField(max_length=200, db_column='entrega', blank=True, verbose_name='Entregado por', default='-')
    recibe  = models.CharField(max_length=200, db_column='recibe', blank=False, verbose_name='Recibido por' )

    class Meta:
        db_table = u'VW_transfEntGaiman'
        verbose_name_plural ="Transferencias Entrada Gaiman"
        verbose_name = "Transferencia Entrada"
    def __unicode__(self):
        return force_unicode(self.idtransferencia)    

class VwTransfSalGaiman(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',verbose_name='FechaSalida') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfSalGaiman',default=4, editable=False,verbose_name='Depo.Salida') 
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfSalGaiman',verbose_name='Depo.Entrada') 
    confirmado = models.BooleanField(default=False)
    entrega = models.CharField(max_length=200, db_column='entrega', blank=False, verbose_name='Entregado por')
    #recibe  = models.CharField(max_length=200, db_column='recibe', blank=True, verbose_name='Recibido por', editable=False, default='-')
    class Meta:
        db_table = u'transfSalGaiman'
        verbose_name_plural ="Transferencias Salida Gaiman"
        verbose_name = "Transferencia Salida"
    def __unicode__(self):
        return force_unicode(self.idtransferencia)    

class DetalleTransfEntGaiman(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey(VwTransfEntGaiman, db_column='idTransferencia',verbose_name='Transferencia') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     cantidadconfirmada = MinMaxFloat(max_value=10000000000000, min_value=0.0, db_column='cantidadConfirmada',verbose_name='Cant.Confirmada')
     confirmado = models.BooleanField()

     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia Entrada Gaiman"
	 verbose_name='Detalle Transferencia Entrada'
	 unique_together = ("idtransferencia","idarticulo")

     def __unicode__(self):
        return force_unicode('')


class DetalleTransfSalGaiman(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey( VwTransfSalGaiman, db_column='idTransferencia',verbose_name='Transferencia')
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia Salida Gaiman"
	 verbose_name='Detalle Transferencia Salida'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
        return force_unicode('')


class VwTransfEntSarmiento(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',editable=False,verbose_name='FechaSalida') 
    fechaentrada = models.DateField(db_column='fechaEntrada',verbose_name='FechaEntrada') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfEntSarmiento',editable=False,verbose_name='Depo.Salida') 
    confirmado = models.BooleanField(default=False)
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfEntSarmiento',editable=False,verbose_name='Depo.Entrada') 
    entrega = models.CharField(max_length=200, db_column='entrega', blank=True, verbose_name='Entregado por', default='-')
    recibe  = models.CharField(max_length=200, db_column='recibe', blank=False, verbose_name='Recibido por' )
    class Meta:
        db_table = u'VW_transfEntSarmiento'
        verbose_name_plural ="Transferencias Entrada Sarmiento"
        verbose_name = "Transferencia Entrada"
    def __unicode__(self):
        return force_unicode(self.idtransferencia)    

class VwTransfSalSarmiento(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',verbose_name='FechaSalida') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfSalSarmiento',default=1, editable=False,verbose_name='Depo.Salida') 
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfSalSarmiento',verbose_name='Depo.Entrada') 
    confirmado = models.BooleanField(default=False) 
    entrega = models.CharField(max_length=200, db_column='entrega', blank=False, verbose_name='Entregado por')
    #recibe  = models.CharField(max_length=200, db_column='recibe', blank=True, verbose_name='Recibido por', editable=False, default='-')
    class Meta:
        db_table = u'transfSalSarmiento'
        verbose_name_plural ="Transferencias Salida Sarmiento"
        verbose_name = "Transferencia Salida"
    def __unicode__(self):
        return force_unicode(self.idtransferencia)    

class DetalleTransfEntSarmiento(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey(VwTransfEntSarmiento, db_column='idTransferencia',verbose_name='Transferencia') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     cantidadconfirmada = MinMaxFloat(max_value=10000000000000, min_value=0.0, db_column='cantidadConfirmada',verbose_name='Cant.Confirmada')
     confirmado = models.BooleanField()

     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia Entrada Sarmiento"
	 verbose_name='Detalle Transferencia Entrada'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class DetalleTransfSalSarmiento(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey( VwTransfSalSarmiento, db_column='idTransferencia',verbose_name='Transferencia')
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia Salida Sarmiento"
	 verbose_name='Detalle Transferencia Salida'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class VwTransfEntEsquel(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',editable=False,verbose_name='FechaSalida') 
    fechaentrada = models.DateField(db_column='fechaEntrada',verbose_name='FechaEntrada') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfEntEsquel',editable=False,verbose_name='Depo.Salida') 
    confirmado = models.BooleanField(default=False)
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfEntEsquel',editable=False,verbose_name='Depo.Entrada') 
    entrega = models.CharField(max_length=200, db_column='entrega', blank=True, verbose_name='Entregado por', default='-')
    recibe  = models.CharField(max_length=200, db_column='recibe', blank=False, verbose_name='Recibido por' )

    class Meta:
        db_table = u'VW_transfEntEsquel'
        verbose_name_plural ="Transferencias Entrada Esquel"
        verbose_name = "Transferencia Entrada"
    def __unicode__(self):
        return force_unicode(self.idtransferencia)    

class VwTransfSalEsquel(models.Model):
    idtransferencia = models.AutoField(primary_key=True, db_column='idTransferencia',verbose_name='Transferencia')
    fechasalida = models.DateField(db_column='fechaSalida',verbose_name='FechaSalida') 
    depositoentrada = models.ForeignKey(Deposito,db_column='depositoEntrada', related_name = 'depoInTransfSalEsquel',verbose_name='Depo.Entrada') 
    depositosalida = models.ForeignKey(Deposito, db_column='depositoSalida', related_name = 'depoOutTransfSalEsquel',default=3, editable=False,verbose_name='Depo.Salida') 
    confirmado = models.BooleanField(default=False)
    entrega = models.CharField(max_length=200, db_column='entrega', blank=False, verbose_name='Entregado por')
    #recibe  = models.CharField(max_length=200, db_column='recibe', blank=True, verbose_name='Recibido por', editable=False, default='-')
    class Meta:
        db_table = u'transfSalEsquel'
        verbose_name_plural ="Transferencias Salida Esquel"
        verbose_name = "Transferencia Salida"
    def __unicode__(self):
        return force_unicode(self.idtransferencia)    

class DetalleTransfEntEsquel(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey(VwTransfEntEsquel, db_column='idTransferencia',verbose_name='Transferencia') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     cantidadconfirmada = MinMaxFloat(max_value=10000000000000, min_value=0.0, db_column='cantidadConfirmada',verbose_name='Cant.Confirmada')
     confirmado = models.BooleanField()
   
     class Meta:
         db_table = u'detalleTrasferencia'
	 verbose_name_plural ="Detalle Transferencia Entrada Esquel"
	 verbose_name='Detalle Transferencia Entrada'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class DetalleTransfSalEsquel(models.Model):
     iddettransferencia = models.AutoField(primary_key=True, db_column='idDetTransferencia',verbose_name='Det.Transferencia')
     idtransferencia = models.ForeignKey( VwTransfSalEsquel, db_column='idTransferencia',verbose_name='Transferencia')
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
         db_table = u'detalleTrasferencia'
         verbose_name_plural ="Detalle Transferencia Salida Esquel"
	 verbose_name='Detalle Transferencia Salida'
	 unique_together = ("idtransferencia","idarticulo")
     def __unicode__(self):
        return force_unicode('')


#----------------------------------------------------------------------------------------------------------------------------------------------------
#==COMPRAS===========================================================================================================================================
#----------------------------------------------------------------------------------------------------------------------------------------------------
TIPO_COMPRA = (
	("Caja Chica","Caja Chica"), 
	("Compra Directa","Compra Directa"), 
	("Concurso de Precios","Concurso de Precios"), 
	("Licitacion Privada","Licitacion Privada"), 
	("Licitacion Publica","Licitacion Publica"),
)

class Compra(models.Model):
     idcompra = models.AutoField(primary_key=True, db_column='idCompra',verbose_name='Compra')
     tipo = models.CharField(max_length=200, choices=TIPO_COMPRA)
     fecha = models.DateField()
     idproveedor = models.ForeignKey(Proveedor,db_column='idProveedor',verbose_name='Proveedor')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',verbose_name='Depósito')
     nroactuacion = models.CharField(max_length=200,db_column='nroActuacion',verbose_name='Nro.Actuación', blank=True)
     nroremito = models.CharField(max_length=200,db_column='nroRemito',verbose_name='Nro.Remito')
     nroordencompra = models.CharField(max_length=200,db_column='nroOrdenCompra',verbose_name='OrdenCompra', blank=True)
     nroexpediente = models.CharField(max_length=200,db_column='nroExpediente',verbose_name='Expediente', blank=True)
     observaciones = models.CharField(max_length=200, blank=True)
     class Meta:
         db_table = u'compra'
         verbose_name_plural ="Compra"
	 verbose_name='Compra'
     def __unicode__(self):
         return force_unicode(self.observaciones)

         
class VwComprasrw(models.Model):
    idcompra = models.AutoField(primary_key=True, db_column='idCompra',verbose_name='Compra')
    tipo = models.CharField(max_length=200, choices=TIPO_COMPRA)
    fecha = models.DateField()
    idproveedor = models.ForeignKey(Proveedor,db_column='idProveedor',verbose_name='Proveedor')
    iddeposito = models.ForeignKey(Deposito, db_column='idDeposito', default=5, editable=False,verbose_name='Depósito')
    nroactuacion = models.CharField(max_length=200,db_column='nroActuacion',verbose_name='Nro.Actuación', blank=True)
    nroremito = models.CharField(max_length=200,db_column='nroRemito',verbose_name='Nro.Remito')
    nroordencompra = models.CharField(max_length=200,db_column='nroOrdenCompra',verbose_name='OrdenCompra', blank=True)
    nroexpediente = models.CharField(max_length=200,db_column='nroExpediente',verbose_name='Expediente', blank=True)
    observaciones = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'VW_comprasRw'
        verbose_name_plural ="Compras Rawson"
        verbose_name = "Compra"
    def __unicode__(self):
        return force_unicode(self.observaciones)

class VwComprastrevelin(models.Model):
    idcompra = models.AutoField(primary_key=True, db_column='idCompra',verbose_name='Compra')
    tipo = models.CharField(max_length=200, choices=TIPO_COMPRA)
    fecha = models.DateField()
    idproveedor = models.ForeignKey(Proveedor,db_column='idProveedor',verbose_name='Proveedor')
    iddeposito = models.ForeignKey(Deposito, db_column='idDeposito', default=6, editable=False,verbose_name='Depósito')
    nroactuacion = models.CharField(max_length=200,db_column='nroActuacion',verbose_name='Nro.Actuación', blank=True)
    nroremito = models.CharField(max_length=200,db_column='nroRemito',verbose_name='Nro.Remito')
    nroordencompra = models.CharField(max_length=200,db_column='nroOrdenCompra',verbose_name='OrdenCompra', blank=True)
    nroexpediente = models.CharField(max_length=200,db_column='nroExpediente',verbose_name='Expediente', blank=True)
    observaciones = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'VW_comprasTrevelin'
        verbose_name_plural ="Compras Trevelin"
        verbose_name = "Compra"
    def __unicode__(self):
        return force_unicode(self.observaciones)  

class VwComprassarmiento(models.Model):
    idcompra = models.AutoField(primary_key=True, db_column='idCompra',verbose_name='Compra')
    tipo = models.CharField(max_length=200, choices=TIPO_COMPRA)
    fecha = models.DateField()
    idproveedor = models.ForeignKey(Proveedor,db_column='idProveedor',verbose_name='Proveedor')
    iddeposito = models.ForeignKey(Deposito, db_column='idDeposito', default=1, editable=False,verbose_name='Depósito')
    nroactuacion = models.CharField(max_length=200,db_column='nroActuacion',verbose_name='Nro.Actuación', blank=True)
    nroremito = models.CharField(max_length=200,db_column='nroRemito',verbose_name='NroRemito')
    nroordencompra = models.CharField(max_length=200,db_column='nroOrdenCompra',verbose_name='OrdenCompra', blank=True)
    nroexpediente = models.CharField(max_length=200,db_column='nroExpediente',verbose_name='Expediente', blank=True)
    observaciones = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'VW_comprasSarmiento'
        verbose_name_plural ="Compra Sarmiento"
        verbose_name = "Compra"
    def __unicode__(self):
        return force_unicode(self.observaciones)    


class VwCompraspmadryn(models.Model):
    idcompra = models.AutoField(primary_key=True, db_column='idCompra',verbose_name='Compra')
    tipo = models.CharField(max_length=200, choices=TIPO_COMPRA)
    fecha = models.DateField()
    idproveedor = models.ForeignKey(Proveedor,db_column='idProveedor',verbose_name='Proveedor')
    iddeposito = models.ForeignKey(Deposito, db_column='idDeposito', default=2, editable=False,verbose_name='Depósito')
    nroactuacion = models.CharField(max_length=200,db_column='nroActuacion',verbose_name='Nro.Actuación', blank=True)
    nroremito = models.CharField(max_length=200,db_column='nroRemito',verbose_name='Nro.Remito')
    nroordencompra = models.CharField(max_length=200,db_column='nroOrdenCompra',verbose_name='OrdenCompra', blank=True)
    nroexpediente = models.CharField(max_length=200,db_column='nroExpediente',verbose_name='Expediente', blank=True)
    observaciones = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'VW_comprasMadryn'
        verbose_name_plural ="Compra Madryn"
        verbose_name = "Compra"
    def __unicode__(self):
        return force_unicode(self.observaciones)

class VwComprasesquel(models.Model):
    idcompra = models.AutoField(primary_key=True, db_column='idCompra',verbose_name='Compra')
    tipo = models.CharField(max_length=200, choices=TIPO_COMPRA)
    fecha = models.DateField()
    idproveedor = models.ForeignKey(Proveedor,db_column='idProveedor',verbose_name='Proveedor')
    iddeposito = models.ForeignKey(Deposito, db_column='idDeposito', default=3, editable=False,verbose_name='Depósito')
    nroactuacion = models.CharField(max_length=200,db_column='nroActuacion',verbose_name='Nro.Actuación', blank=True)
    nroremito = models.CharField(max_length=200,db_column='nroRemito',verbose_name='Nro.Remito')
    nroordencompra = models.CharField(max_length=200,db_column='nroOrdenCompra',verbose_name='OrdenCompra', blank=True)
    nroexpediente = models.CharField(max_length=200,db_column='nroExpediente',verbose_name='Expediente', blank=True)
    observaciones = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'VW_comprasEsquel'
        verbose_name_plural ="Compra Esquel"
        verbose_name = "Compra"
    def __unicode__(self):
        return force_unicode(self.observaciones)

class VwComprasgaiman(models.Model):
    idcompra = models.AutoField(primary_key=True, db_column='idCompra',verbose_name='Compra')
    tipo = models.CharField(max_length=200, choices=TIPO_COMPRA)
    fecha = models.DateField()
    idproveedor = models.ForeignKey(Proveedor,db_column='idProveedor', verbose_name='Proveedor')
    iddeposito = models.ForeignKey(Deposito, db_column='idDeposito', default=4, editable=False,verbose_name='Depósito')
    nroactuacion = models.CharField(max_length=200,db_column='nroActuacion',verbose_name='Nro.Actuación', blank=True)
    nroremito = models.CharField(max_length=200,db_column='nroRemito',verbose_name='Nro.Remito')
    nroordencompra = models.CharField(max_length=200,db_column='nroOrdenCompra',verbose_name='OrdenCompra', blank=True)
    nroexpediente = models.CharField(max_length=200,db_column='nroExpediente',verbose_name='Expediente', blank=True)
    observaciones = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = u'VW_comprasGaiman'
        verbose_name_plural ="Compra Gaiman"
        verbose_name = "Compra"
    def __unicode__(self):
        return force_unicode(self.observaciones)         

class Detallecomprarw(models.Model):
     iddetcompra = models.AutoField(primary_key=True, db_column='idDetCompra',verbose_name='Det.Compra')
     idcompra = models.ForeignKey(VwComprasrw, db_column='idCompra',verbose_name='Compra') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     preciounitario = models.CharField(max_length=200, db_column='precioUnitario',verbose_name='PrecioUnitario')

     class Meta:
         db_table = u'detalleCompra'
	 verbose_name_plural ="Detalle Compra Rawson"
	 unique_together = ("idcompra","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class Detallecompratrevelin(models.Model):
     iddetcompra = models.AutoField(primary_key=True, db_column='idDetCompra',verbose_name='Det.Compra')
     idcompra = models.ForeignKey(VwComprastrevelin, db_column='idCompra',verbose_name='Compra') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     preciounitario = models.CharField(max_length=200, db_column='precioUnitario',verbose_name='PrecioUnitario')

     class Meta:
         db_table = u'detalleCompra'
	 verbose_name_plural ="Detalle Compra Trevelin"
	 unique_together = ("idcompra","idarticulo")
     def __unicode__(self):
        return force_unicode('')
        
class Detallecomprasarmiento(models.Model):
     iddetcompra = models.AutoField(primary_key=True, db_column='idDetCompra',verbose_name='Det.Compra')
     idcompra = models.ForeignKey(VwComprassarmiento, db_column='idCompra',verbose_name='Compra') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     preciounitario = models.CharField(max_length=200, db_column='precioUnitario',verbose_name='PrecioUnitario')

     class Meta:
         db_table = u'detalleCompra'
	 verbose_name_plural ="Detalle Compra Sarmiento"
	 unique_together = ("idcompra","idarticulo")
     def __unicode__(self):
        return force_unicode('')
        
class Detallecompramadryn(models.Model):
     iddetcompra = models.AutoField(primary_key=True, db_column='idDetCompra',verbose_name='Det.Compra')
     idcompra = models.ForeignKey(VwCompraspmadryn, db_column='idCompra',verbose_name='Compra') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     preciounitario = models.CharField(max_length=200, db_column='precioUnitario',verbose_name='PrecioUnitario')
     #preciounitario = PriceField('Precio unitario', db_column='preciounitario', currency='BTC')

     class Meta:
         db_table = u'detalleCompra'
	 verbose_name_plural ="Detalle Compra Madryn"
	 unique_together = ("idcompra","idarticulo")
     def __unicode__(self):
        return force_unicode('')
        
class Detallecompragaiman(models.Model):
     iddetcompra = models.AutoField(primary_key=True, db_column='idDetCompra',verbose_name='Det.Compra')
     idcompra = models.ForeignKey(VwComprasgaiman, db_column='idCompra',verbose_name='Compra') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     preciounitario = models.CharField(max_length=200, db_column='precioUnitario',verbose_name='PrecioUnitario')

     class Meta:
         db_table = u'detalleCompra'
	 verbose_name_plural ="Detalle Compra Gaiman"
	 unique_together = ("idcompra","idarticulo")
     def __unicode__(self):
        return force_unicode('')

         
class Detallecompraesquel(models.Model):
     iddetcompra = models.AutoField(primary_key=True, db_column='idDetCompra',verbose_name='Det.Compra')
     idcompra = models.ForeignKey(VwComprasesquel, db_column='idCompra',verbose_name='Compra') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     preciounitario = models.CharField(max_length=200, db_column='precioUnitario',verbose_name='PrecioUnitario')
     #preciounitario = models.PriceField(db_column='precioUnitario',verbose_name='PrecioUnitario')

     class Meta:
         db_table = u'detalleCompra'
	 verbose_name_plural ="Detalle compra Esquel"
	 unique_together = ("idcompra","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class Detallecompra(models.Model):
     iddetcompra = models.AutoField(primary_key=True, db_column='idDetCompra',verbose_name='Det.Compra')
     idcompra = models.ForeignKey(Compra, db_column='idCompra',verbose_name='Compra') 
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     preciounitario = models.CharField(max_length=200, db_column='precioUnitario',verbose_name='PrecioUnitario')

     class Meta:
         db_table = u'detalleCompra'
	 verbose_name_plural ="Detalle Compra"
	 unique_together = ("idcompra","idarticulo")
     def __unicode__(self):
         return force_unicode('')

#----------------------------------------------------------------------------------------------------------------------------------------------------
#==DEVOLUCIONES======================================================================================================================================
#----------------------------------------------------------------------------------------------------------------------------------------------------
class Devoluciones(models.Model):
     iddevolucion = models.AutoField(primary_key=True, db_column='idDevolucion',verbose_name='Devolución')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',verbose_name='Depósito')
     observaciones = models.CharField(max_length=200)
     idproveedor =  models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     fecha = models.DateField()
     
     class Meta:
         db_table = u'devoluciones'
	 verbose_name_plural ="Devoluciones"
	 verbose_name='Devolución'
     def __unicode__(self):
         return force_unicode(self.observaciones)

class Devoluciongaiman(models.Model):
     iddevolucion = models.AutoField(primary_key=True, db_column='idDevolucion',verbose_name='Devolución')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',editable=False,default=4,verbose_name='Depósito') # Field name made lowercase.
     observaciones = models.CharField(max_length=200)
     idproveedor =  models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     fecha = models.DateField()

     class Meta:
         db_table = u'devolucionesGaiman'
	 verbose_name_plural ="Devoluciones Gaiman"
         verbose_name = "Articulo Devolucion"
         verbose_name='Devolución'
     def __unicode__(self):
         return force_unicode(self.observaciones)
         
class Devoluciontrevelin(models.Model):
     iddevolucion = models.AutoField(primary_key=True, db_column='idDevolucion',verbose_name='Devolución')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',editable=False,default=4,verbose_name='Depósito') # Field name made lowercase.
     observaciones = models.CharField(max_length=200)
     idproveedor =  models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     fecha = models.DateField()

     class Meta:
         db_table = u'devolucionesTrevelin'
	 verbose_name_plural ="Devoluciones Trevelin"
         verbose_name = "Articulo Devolucion"
         verbose_name='Devolución'
     def __unicode__(self):
         return force_unicode(self.observaciones)

"""class Devolucionrtrevelin(models.Model):
     iddevolucion = models.AutoField(primary_key=True, db_column='idDevolucion',verbose_name='Devolución')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',editable=False,default=6,verbose_name='Depósito') # Field name made lowercase.
     observaciones = models.CharField(max_length=200)
     idproveedor =  models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     fecha = models.DateField()

     class Meta:
         db_table = u'devolucionesTrevelin'
	 verbose_name_plural ="Devoluciones Trevelin"
         verbose_name = "Articulo Devolucion"
         verbose_name='Devolución'
     def __unicode__(self):
         return force_unicode(self.observaciones)
"""         
class Devolucionmadryn(models.Model):
     iddevolucion = models.AutoField(primary_key=True, db_column='idDevolucion',verbose_name='Devolución')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',editable=False,default=2) # Field name made lowercase.
     observaciones = models.CharField(max_length=200)
     idproveedor =  models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     fecha = models.DateField()
     
     class Meta:
         db_table = u'devolucionesMadryn'
	 verbose_name_plural ="Devoluciones Madryn"
         verbose_name = "Articulo Devolucion"
     def __unicode__(self):
         return force_unicode(self.observaciones)

class Devolucionrw(models.Model):
     iddevolucion = models.AutoField(primary_key=True, db_column='idDevolucion',verbose_name='Devolución')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',editable=False,default=5,verbose_name='Depósito') # Field name made lowercase.
     observaciones = models.CharField(max_length=200)
     idproveedor =  models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     fecha = models.DateField()

     class Meta:
         db_table = u'devolucionesRw'
	 verbose_name_plural ="Devoluciones Rawson"
         verbose_name = "Articulo Devolucion"
	 verbose_name = "Devolución"
     def __unicode__(self):
         return force_unicode(self.observaciones)

class Devolucionsarmiento(models.Model):
     iddevolucion = models.AutoField(primary_key=True, db_column='idDevolucion',verbose_name='Devolución')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',editable=False,default=1,verbose_name='Depósito') # Field name made lowercase.
     observaciones = models.CharField(max_length=200)
     idproveedor =  models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     fecha = models.DateField()
     
     class Meta:
         db_table = u'devolucionesSarmiento'
	 verbose_name_plural ="Devoluciones Sarmiento"
         verbose_name = "Articulo Devolucion"
	 verbose_name = "Devolución"
     def __unicode__(self):
         return force_unicode(self.observaciones)

class Devolucionesquel(models.Model):
     iddevolucion = models.AutoField(primary_key=True, db_column='idDevolucion',verbose_name='Devolución')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',editable=False,default=3,verbose_name='Depósito')
     observaciones = models.CharField(max_length=200)
     idproveedor =  models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     fecha = models.DateField()
     
     class Meta:
         db_table = u'devolucionesEsquel'
	 verbose_name_plural ="Devoluciones Esquel"
         verbose_name = "Articulo Devolucion"
	 verbose_name = "Devolución"
     def __unicode__(self):
         return force_unicode(self.observaciones)

class DetalledevolucionRw(models.Model):
     iddetdevolucion = models.AutoField(primary_key=True, db_column='idDetDevolucion',verbose_name='Det.Devolución')
     iddevolucion = models.ForeignKey(Devolucionrw,db_column='idDevolucion',verbose_name='Devolución') # Field name made lowercase.
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo,db_column='idArticulo',verbose_name='Artículo') # Field name made lowercase.
     observacion = models.CharField(max_length=200,verbose_name='Observaciones')
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
         db_table = u'detalleDevolucion'
	 verbose_name_plural ="Detalle Devolución Rawson"
	 unique_together = ("iddevolucion","idarticulo")
         verbose_name = "Detalle Artículo Devolución"
     def __unicode__(self):
         return force_unicode('')

         
class DetalledevolucionTrevelin(models.Model):
     iddetdevolucion = models.AutoField(primary_key=True, db_column='idDetDevolucion',verbose_name='Det.Devolución')
     iddevolucion = models.ForeignKey(Devoluciontrevelin,db_column='idDevolucion',verbose_name='Devolución') # Field name made lowercase.
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo,db_column='idArticulo',verbose_name='Artículo') # Field name made lowercase.
     observacion = models.CharField(max_length=200,verbose_name='Observaciones')
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
         db_table = u'detalleDevolucion'
	 verbose_name_plural ="Detalle Devolución Trevelin"
	 unique_together = ("iddevolucion","idarticulo")
         verbose_name = "Detalle Artículo Devolución"
     def __unicode__(self):
         return force_unicode('')
         
class DetalledevolucionMadryn(models.Model):
     iddetdevolucion = models.AutoField(primary_key=True, db_column='idDetDevolucion',verbose_name='Det.Devolución')
     iddevolucion = models.ForeignKey(Devolucionmadryn,db_column='idDevolucion',verbose_name='Devolución') # Field name made lowercase.
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo,db_column='idArticulo',verbose_name='Artículo') # Field name made lowercase.
     observacion = models.CharField(max_length=200,verbose_name='Observaciones')
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles !')

     class Meta:
         db_table = u'detalleDevolucion'
	 verbose_name_plural ="Detalle Devolución Madryn"
	 unique_together = ("iddevolucion","idarticulo")
         verbose_name = "Detalle Artículo Devolución"
     def __unicode__(self):
         return force_unicode('')

class DetalledevolucionSarmiento(models.Model):
     iddetdevolucion = models.AutoField(primary_key=True, db_column='idDetDevolucion',verbose_name='Det.Devolución')
     iddevolucion = models.ForeignKey(Devolucionsarmiento,db_column='idDevolucion',verbose_name='Devolución') # Field name made lowercase.
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo,db_column='idArticulo',verbose_name='Artículo') # Field name made lowercase.
     observacion = models.CharField(max_length=200,verbose_name='Observaciones')
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalle !')

     class Meta:
         db_table = u'detalleDevolucion'
	 verbose_name_plural ="Detalle Devolución Sarmiento"
	 unique_together = ("iddevolucion","idarticulo")
         verbose_name = "Detalle Artículo Devolución"
     def __unicode__(self):
         return force_unicode('')

class DetalledevolucionGaiman(models.Model):
     iddetdevolucion = models.AutoField(primary_key=True, db_column='idDetDevolucion',verbose_name='Det.Devolución')
     iddevolucion = models.ForeignKey(Devoluciongaiman,db_column='idDevolucion',verbose_name='Devolución') # Field name made lowercase.
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo,db_column='idArticulo',verbose_name='Artículo') # Field name made lowercase.
     observacion = models.CharField(max_length=200,verbose_name='Observaciones')
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles !')

     class Meta:
         db_table = u'detalleDevolucion'
	 verbose_name_plural ="Detalle Devolución Gaiman"
	 unique_together = ("iddevolucion","idarticulo")
         verbose_name = "Detalle Artículo Devolución"
     def __unicode__(self):
         return force_unicode('')

class DetalledevolucionEsquel(models.Model):
     iddetdevolucion = models.AutoField(primary_key=True, db_column='idDetDevolucion',verbose_name='Det.Devolución')
     iddevolucion = models.ForeignKey(Devolucionesquel,db_column='idDevolucion',verbose_name='Devolución') # Field name made lowercase.
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo,db_column='idArticulo',verbose_name='Artículo') # Field name made lowercase.
     observacion = models.CharField(max_length=200,verbose_name='Observaciones')
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles !')
     class Meta:
         db_table = u'detalleDevolucion'
	 verbose_name_plural ="Detalle Devolución Esquel"
	 unique_together = ("iddevolucion","idarticulo")
         verbose_name = "Detalle Artículo Devolución"
     def __unicode__(self):
         return force_unicode('')

class Detalledevolucion(models.Model):
     iddetdevolucion = models.AutoField(primary_key=True, db_column='idDetDevolucion',verbose_name='Det.Devolución')
     iddevolucion = models.ForeignKey(Devoluciones,db_column='idDevolucion',verbose_name='Devolución') # Field name made lowercase.
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo,db_column='idArticulo',verbose_name='Artículo') # Field name made lowercase.
     observacion = models.CharField(max_length=200,verbose_name='Observaciones')
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles !')

     class Meta:
         db_table = u'detalleDevolucion'
	 verbose_name_plural ="Detalle Devolución"
	 unique_together = ("iddevolucion","idarticulo")
         verbose_name = "Detalle Artículo Devolución"
     def __unicode__(self):
         return force_unicode('')
#----------------------------------------------------------------------------------------------------------------------------------------------------
         
class Articulodeposito(models.Model):
     idarticulodeposito = models.AutoField(primary_key=True, db_column='idArticuloDeposito',verbose_name = 'Art.Depósito')
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Articulo') # Field name made lowercase.
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',verbose_name='Deposito') # Field name made lowercase.
     stock = models.FloatField()
     stockentrante = models.FloatField(db_column='stockEntrante',verbose_name='StockEntrada')
     stocksaliente = models.FloatField(db_column='stockSaliente',verbose_name='StockSalida')
     nroficha = models.SmallIntegerField(db_column='nroFicha',verbose_name='NroFicha')
     mueble = models.CharField(max_length=200,verbose_name='Mueble')
     casillero = models.CharField(max_length=200,verbose_name='Casillero')

     class Meta:
         db_table = u'articuloDeposito'
	 verbose_name_plural ="Artículo Depósito (Stock)"
     	 verbose_name = "Artículo Depósito"
     def __unicode__(self):
         return force_unicode(self.idarticulo)


#----------------------------VW Aticulos-----------------------------------------------------------
#----------------------------Rawson----------------------------------------------------------------
   
class ArticuloDepositoRawson(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial')
     nroficha = models.SmallIntegerField(db_column='nroFicha',verbose_name='NroFicha')
     
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem',verbose_name='Descripción')
     mueble = models.CharField(max_length=200,verbose_name='Mueble')
     casillero = models.CharField(max_length=200,verbose_name='Casillero')
     stmin = MinMaxFloat(db_column='stmin',max_value=1000000000000, min_value=0.0, verbose_name='Stock Min')
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Cód.Barra')
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida',verbose_name='UnidadMedida')
     stock = models.FloatField()
     stockentrante = models.FloatField(db_column='stockEntrante',verbose_name='StockEntrante')
     stocksaliente = models.FloatField(db_column='stockSaliente',verbose_name='StockSaliente')

     class Meta:
         db_table = u'depositoRw'
         verbose_name_plural ="Artículos Depósito Rawson"
         verbose_name = "Artículo Depósito"
     def __unicode__(self):
         return force_unicode(self.idarticulo)
#----------------------------Trevelin----------------------------------------------------------------
class ArticuloDepositoTrevelin(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial')
     nroficha = models.SmallIntegerField(db_column='nroFicha',verbose_name='NroFicha')
     
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem',verbose_name='Descripción')
     mueble = models.CharField(max_length=200,verbose_name='Mueble')
     casillero = models.CharField(max_length=200,verbose_name='Casillero')
     stmin = MinMaxFloat(db_column='stmin',max_value=1000000000000, min_value=0.0, verbose_name='Stock Min')
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Cód.Barra')
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida',verbose_name='UnidadMedida')
     stock = models.FloatField()
     stockentrante = models.FloatField(db_column='stockEntrante',verbose_name='StockEntrante')
     stocksaliente = models.FloatField(db_column='stockSaliente',verbose_name='StockSaliente')

     class Meta:
         db_table = u'depositoTrevelin'
         verbose_name_plural ="Artículos Depósito Trevelin"
         verbose_name = "Artículo Depósito"
     def __unicode__(self):
         return force_unicode(self.idarticulo)
#----------------------------Sarmiento----------------------------------------------------------------
class ArticuloDepositoSarmiento(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') # Field n$
     nroficha = models.SmallIntegerField(db_column='nroFicha',verbose_name='NroFicha') # Field name made lowercase.
     
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem',verbose_name='Descripción') # Field name made lowercas$
     mueble = models.CharField(max_length=200,verbose_name='Mueble')
     casillero = models.CharField(max_length=200,verbose_name='Casillero')
     stmin = MinMaxFloat(db_column='stmin',max_value=1000000000000, min_value=0.0, verbose_name='Stock Min')
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Cód.Barra') # Field name made lowercase.
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida',verbose_name='UnidadMedida') # Field name made lowercase.
     stock = models.FloatField()
     stockentrante = models.FloatField(db_column='stockEntrante',verbose_name='StockEntrante')
     stocksaliente = models.FloatField(db_column='stockSaliente',verbose_name='StockSaliente')

     class Meta:
         db_table = u'depositoSarmiento'
         verbose_name_plural ="Artículos Depósito Sarmiento"
         verbose_name = "Artículo Depósito"
     def __unicode__(self):
         return force_unicode(self.idarticulo)


#----------------------------Esquel----------------------------------------------------------------
class ArticuloDepositoEsquel(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') # Field n$
     nroficha = models.SmallIntegerField(db_column='nroFicha',verbose_name='NroFicha') # Field name made lowercase.
     
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem',verbose_name='Descripción') # Field name made lowercas$
     mueble = models.CharField(max_length=200,verbose_name='Mueble')
     casillero = models.CharField(max_length=200,verbose_name='Casillero')
     stmin = MinMaxFloat(db_column='stmin',max_value=1000000000000, min_value=0.0, verbose_name='Stock Min')
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Cod.Barra') # Field name made lowercase.
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida',verbose_name='UnidadMedida') # Field name made lowercase.
     stock = models.FloatField()
     stockentrante = models.FloatField(db_column='stockEntrante',verbose_name='StockEntrante')
     stocksaliente = models.FloatField(db_column='stockSaliente',verbose_name='StockSaliente')

     class Meta:
         db_table = u'depositoEsquel'
         verbose_name_plural ="Artículos Depósito Esquel"
         verbose_name = "Artículo Depósito"
     def __unicode__(self):
         return force_unicode(self.idarticulo)

#----------------------------Gaiman----------------------------------------------------------------
class ArticuloDepositoGaiman(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') # Field n$
     nroficha = models.SmallIntegerField(db_column='nroFicha',verbose_name='NroFicha') # Field name made lowercase.
     
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem',verbose_name='Descripción') # Field name made lowercas$
     mueble = models.CharField(max_length=200,verbose_name='Mueble')
     casillero = models.CharField(max_length=200,verbose_name='Casillero')
     stmin = MinMaxFloat(db_column='stmin',max_value=1000000000000, min_value=0.0, verbose_name='Stock Min')
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Cod.Barra') # Field name made lowercase.
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida',verbose_name='UnidadMedida') # Field name made lowercase.
     stock = models.FloatField()
     stockentrante = models.FloatField(db_column='stockEntrante',verbose_name='StockEntrante')
     stocksaliente = models.FloatField(db_column='stockSaliente',verbose_name='StockSaliente')

     class Meta:
         db_table = u'depositoGaiman'
         verbose_name_plural ="Artículos Depósito Gaiman"
         verbose_name = "Artículo Depósito"
     def __unicode__(self):
         return force_unicode(self.idarticulo)

#----------------------------Madryn----------------------------------------------------------------
class ArticuloDepositoMadryn(models.Model):
     idarticulo = models.AutoField(primary_key=True, db_column='idArticulo',verbose_name='Artículo')
     
     nrocuentapatrimonial = models.ForeignKey(Cuentaspatrimoniales, db_column='nroCuentaPatrimonial',verbose_name='CtaPatrimonial') # Field n$
     nroficha = models.SmallIntegerField(db_column='nroFicha',verbose_name='NroFicha') # Field name made lowercase.
     
     descripcionitem = models.CharField(max_length=200, db_column='descripcionItem',verbose_name='Descripción') # Field name made lowercas$
     mueble = models.CharField(max_length=200,verbose_name='Mueble')
     casillero = models.CharField(max_length=200,verbose_name='Casillero')
     stmin = MinMaxFloat(db_column='stmin',max_value=1000000000000, min_value=0.0, verbose_name='Stock Min')
     idbarra = models.ForeignKey(Barras, db_column='idBarra',verbose_name='Cod.Barra') # Field name made lowercase.
     unidadmedida = models.ForeignKey(Unidadesmedidas, db_column='unidadMedida',verbose_name='UnidadMedida') # Field name made lowercase.
     stock = models.FloatField()
     stockentrante = models.FloatField(db_column='stockEntrante',verbose_name='StockEntrante')
     stocksaliente = models.FloatField(db_column='stockSaliente',verbose_name='StockSaliente')

     class Meta:
         db_table = u'depositoMadryn'
         verbose_name_plural ="Artículos Depósito Madryn"
         verbose_name = "Artículo Depósito"
     def __unicode__(self):
         return force_unicode(self.idarticulo)

        
#----------------------------Historial Precio-----------------------------------------------------------
class HistorialPrecios(models.Model):
     idhistorialprecios = models.AutoField(primary_key=True, db_column='idHistorialPrecios',verbose_name='HistorialPrecio')
     idarticulo =  models.ForeignKey(ArticuloDepositoRawson, db_column='idArticulo',verbose_name='Artículo')
     idproveedor = models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',verbose_name='Depósito')
     fecha = models.DateField(db_column='Fecha')
     iddetcompra = models.ForeignKey(Detallecompra, db_column='idDetCompra', editable=False,verbose_name='Det.Compra')
     precio = models.CharField(max_length=200, db_column='precio',verbose_name='Precio')
     class Meta:
         db_table = u'historialPrecios'
         verbose_name_plural ="Historial Precios"
	 verbose_name='Historial Precio'
     def __unicode__(self):
         return force_unicode('')

class HistorialPreciosArticulo(models.Model):
     idhistorialprecios = models.AutoField(primary_key=True, db_column='idHistorialPrecios',verbose_name='HistorialPrecio')
     idarticulo =  models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo')
     idproveedor = models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',verbose_name='Depósito')
     fecha = models.DateField(db_column='Fecha')
     iddetcompra = models.ForeignKey(Detallecompra, db_column='idDetCompra', editable=False,verbose_name='Det.Compra')
     precio = models.CharField(max_length=200, db_column='precio',verbose_name='Precio')
     class Meta:
         db_table = u'historialPrecios'
         verbose_name_plural ="Historial Precios"
         verbose_name='Historial Precio'
     def __unicode__(self):
         return force_unicode('')
#--------------------------------------------

class HistorialPreciosrw(models.Model):
     idhistorialprecios = models.AutoField(primary_key=True, db_column='idHistorialPrecios',verbose_name='HistorialPrecio')
     idarticulo =  models.ForeignKey(ArticuloDepositoRawson, db_column='idArticulo',verbose_name='Artículo')
     idproveedor = models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',verbose_name='Depósito')
     fecha = models.DateField(db_column='Fecha')
     iddetcompra = models.ForeignKey(Detallecompra, db_column='idDetCompra', editable=False,verbose_name='Det.Compra')
     precio = models.CharField(max_length=200, db_column='precio',verbose_name='Precio')
     class Meta:
         db_table = u'historialPrecios'
         verbose_name_plural ="Historial Precios"
	 verbose_name='Historial Precio'
     def __unicode__(self):
         return force_unicode('')
         
#--------------------------------------------

class HistorialPreciostrevelin(models.Model):
     idhistorialprecios = models.AutoField(primary_key=True, db_column='idHistorialPrecios',verbose_name='HistorialPrecio')
     idarticulo =  models.ForeignKey(ArticuloDepositoTrevelin, db_column='idArticulo',verbose_name='Artículo')
     idproveedor = models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',verbose_name='Depósito')
     fecha = models.DateField(db_column='Fecha')
     iddetcompra = models.ForeignKey(Detallecompra, db_column='idDetCompra', editable=False,verbose_name='Det.Compra')
     precio = models.CharField(max_length=200, db_column='precio',verbose_name='Precio')
     class Meta:
         db_table = u'historialPrecios'
         verbose_name_plural ="Historial Precios"
	 verbose_name='Historial Precio'
     def __unicode__(self):
         return force_unicode('')
#--------------------------------------------
class HistorialPreciosmadryn(models.Model):
     idhistorialprecios = models.AutoField(primary_key=True, db_column='idHistorialPrecios',verbose_name='HistorialPrecio')
     idarticulo =  models.ForeignKey(ArticuloDepositoMadryn, db_column='idArticulo',verbose_name='Artículo')
     idproveedor = models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',verbose_name='Depósito')
     fecha = models.DateField(db_column='Fecha')
     iddetcompra = models.ForeignKey(Detallecompra, db_column='idDetCompra', editable=False,verbose_name='Det.Compra')
     precio = models.CharField(max_length=200, db_column='precio',verbose_name='Precio')
     class Meta:
         db_table = u'historialPrecios'
         verbose_name_plural ="Historial Precios"
	 verbose_name='Historial Precio'
     def __unicode__(self):
         return force_unicode('')
#--------------------------------------------
class HistorialPreciosgaiman(models.Model):
     idhistorialprecios = models.AutoField(primary_key=True, db_column='idHistorialPrecios',verbose_name='HistorialPrecio')
     idarticulo =  models.ForeignKey(ArticuloDepositoGaiman, db_column='idArticulo',verbose_name='Artículo')
     idproveedor = models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',verbose_name='Depósito')
     fecha = models.DateField(db_column='Fecha')
     iddetcompra = models.ForeignKey(Detallecompra, db_column='idDetCompra', editable=False,verbose_name='Det.Compra')
     precio = models.CharField(max_length=200, db_column='precio')
     class Meta:
         db_table = u'historialPrecios'
         verbose_name_plural ="Historial Precios"
	 verbose_name='Historial Precio'
     def __unicode__(self):
         return force_unicode('')
#--------------------------------------------
class HistorialPreciossarmiento(models.Model):
     idhistorialprecios = models.AutoField(primary_key=True, db_column='idHistorialPrecios',verbose_name='HistorialPrecio')
     idarticulo =  models.ForeignKey(ArticuloDepositoSarmiento, db_column='idArticulo',verbose_name='Artículo')
     idproveedor = models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',verbose_name='Depósito')
     fecha = models.DateField(db_column='Fecha')
     iddetcompra = models.ForeignKey(Detallecompra, db_column='idDetCompra', editable=False,verbose_name='Det.Compra')
     precio = models.CharField(max_length=200, db_column='precio',verbose_name='Precio')
     class Meta:
         db_table = u'historialPrecios'
         verbose_name_plural ="Historial Precios"
	 verbose_name='Historial Precio'
     def __unicode__(self):
         return force_unicode('')
#--------------------------------------------
class HistorialPreciosesquel(models.Model):
     idhistorialprecios = models.AutoField(primary_key=True, db_column='idHistorialPrecios',verbose_name='HistorialPrecio')
     idarticulo =  models.ForeignKey(ArticuloDepositoEsquel, db_column='idArticulo',verbose_name='Artículo')
     idproveedor = models.ForeignKey(Proveedor, db_column='idProveedor',verbose_name='Proveedor')
     iddeposito = models.ForeignKey(Deposito, db_column='idDeposito',verbose_name='Depósito')
     fecha = models.DateField(db_column='Fecha')
     iddetcompra = models.ForeignKey(Detallecompra, db_column='idDetCompra', editable=False,verbose_name='Det.Compra')
     precio = models.CharField(max_length=200, db_column='precio',verbose_name='Precio')
     class Meta:
         db_table = u'historialPrecios'
         verbose_name_plural ="Historial Precios"
	 verbose_name='Historial Precio'
     def __unicode__(self):
         return force_unicode('')
#--------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------------
#==SALIDAS===========================================================================================================================================
#----------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
class Salida(models.Model):
     idsalida = models.AutoField(primary_key=True, db_column='idSalida',verbose_name='Salida')
     fecha = models.DateField()
     entregadoa = models.CharField(max_length=200, db_column='entregadoA',verbose_name='Entregado a') 
     destino = models.CharField(max_length=200)
     observaciones = models.CharField(max_length=200, blank=True,)
     iddeposito =models.ForeignKey(Deposito,db_column='idDeposito',verbose_name='Depósito') 

     class Meta:
        db_table = u'salida'
	verbose_name_plural ="Salida"
	verbose_name='Salida'
     def __unicode__(self):
        return force_unicode('')

class Detallesalida(models.Model):
     iddetsalida = models.AutoField(primary_key=True, db_column='idDetSalida',verbose_name='Det.Salida')
     idsalida = models.ForeignKey(Salida, db_column='idSalida',verbose_name='Salida') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
        db_table = u'detalleSalida'
	verbose_name_plural ="Detalle Salida"
	verbose_name='Detalle Salida'
	unique_together = ("idsalida","idarticulo")
     def __unicode__(self):
        return force_unicode(self.idsalida)


class VwSalidaesquel(models.Model):
    idsalida = models.AutoField(primary_key=True, db_column='idSalida',verbose_name='Salida')
    fecha = models.DateField(null=True)
    entregadoa = models.CharField(max_length=200, db_column='entregadoA',verbose_name='Entregado a') # Field name made lowercase.
    destino = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=200,blank=True,)
    iddeposito = models.ForeignKey(Deposito,db_column='idDeposito',default=3, editable=False,verbose_name='Depósito') # Field name made lowercase.
    
    class Meta:
        db_table = u'VW_salidaEsquel'
	verbose_name_plural ="Salida Esquel"
        verbose_name = "Salida"
    def __unicode__(self):
         return force_unicode(self.observaciones)

class DetallesalidaEsquel(models.Model):
     iddetsalida = models.AutoField(primary_key=True, db_column='idDetSalida',verbose_name='Det.Salida')
     idsalida = models.ForeignKey(VwSalidaesquel, db_column='idSalida',verbose_name='Salida') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
        db_table = u'detalleSalida'
        verbose_name_plural ="Detalle Salida Esquel"
	verbose_name='Detalle Salida'
	unique_together = ("idsalida","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class VwSalidatrevelin(models.Model):
    idsalida = models.AutoField(primary_key=True, db_column='idSalida',verbose_name='Salida')
    fecha = models.DateField(null=True)
    entregadoa = models.CharField(max_length=200, db_column='entregadoA',verbose_name='Entregado a') # Field name made lowercase.
    destino = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=200,blank=True,)
    iddeposito = models.ForeignKey(Deposito,db_column='idDeposito',default=6, editable=False,verbose_name='Depósito') # Field name made lowercase.
    
    class Meta:
        db_table = u'VW_salidaTrevelin'
	verbose_name_plural ="Salida Trevelin"
        verbose_name = "Salida"
    def __unicode__(self):
         return force_unicode(self.observaciones)

class DetallesalidaTrevelin(models.Model):
     iddetsalida = models.AutoField(primary_key=True, db_column='idDetSalida',verbose_name='Det.Salida')
     idsalida = models.ForeignKey(VwSalidatrevelin, db_column='idSalida',verbose_name='Salida') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
        db_table = u'detalleSalida'
        verbose_name_plural ="Detalle Salida Trevelin"
	verbose_name='Detalle Salida'
	unique_together = ("idsalida","idarticulo")
     def __unicode__(self):
        return force_unicode('')
        
        
class VwSalidagaiman(models.Model):
    idsalida = models.AutoField(primary_key=True, db_column='idSalida',verbose_name='Salida')
    fecha = models.DateField(null=True)
    entregadoa = models.CharField(max_length=200, db_column='entregadoA',verbose_name='Entregado a') 
    destino = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=200,blank=True,)
    iddeposito = models.ForeignKey(Deposito,db_column='idDeposito',default=4, editable=False,verbose_name='Depósito') 
    
    class Meta:
        db_table = u'VW_salidaGaiman'
	verbose_name_plural ="Salida Gaiman"
        verbose_name = "Salida" 
    def __unicode__(self):
         return force_unicode(self.observaciones)

class DetallesalidaGaiman(models.Model):
     iddetsalida = models.AutoField(primary_key=True, db_column='idDetSalida',verbose_name='Det.Salida')
     idsalida = models.ForeignKey(VwSalidagaiman, db_column='idSalida',verbose_name='Salida') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
        db_table = u'detalleSalida'
        verbose_name_plural ="Detalle Salida Gaiman"
	verbose_name='Detalle Salida'
	unique_together = ("idsalida","idarticulo")
     def __unicode__(self):
        return force_unicode('')


class VwSalidasarmiento(models.Model):
    idsalida = models.AutoField(primary_key=True, db_column='idSalida',verbose_name='Salida')
    fecha = models.DateField(null=True)
    entregadoa = models.CharField(max_length=200, db_column='entregadoA',verbose_name='Entregado a') 
    destino = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=200, blank=True,)
    iddeposito = models.ForeignKey(Deposito,db_column='idDeposito',default=1, editable=False,verbose_name='Depósito') 
    
    class Meta:
        db_table = u'VW_salidaSarmiento'
	verbose_name_plural ="Salida Sarmiento"
        verbose_name = "Salida"
    def __unicode__(self):
         return force_unicode(self.observaciones)

class DetallesalidaSarmiento(models.Model):
     iddetsalida = models.AutoField(primary_key=True, db_column='idDetSalida',verbose_name='Det.Salida')
     idsalida = models.ForeignKey(VwSalidasarmiento, db_column='idSalida',verbose_name='Salida') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo') 
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
        db_table = u'detalleSalida'
        verbose_name_plural ="Detalle Salida Sarmiento"
	verbose_name='Detalle Salida'
	unique_together = ("idsalida","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class VwSalidamadryn(models.Model):
    idsalida = models.AutoField(primary_key=True, db_column='idSalida',verbose_name='Salida')
    fecha = models.DateField(null=True)
    entregadoa = models.CharField(max_length=200, db_column='entregadoA',verbose_name='Entregado a') 
    destino = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=200,blank=True,)
    iddeposito = models.SmallIntegerField(null=True, db_column='idDeposito', default=2,editable=False,verbose_name='Depósito') 
    
    class Meta:
        db_table = u'VW_salidaMadryn'
	verbose_name_plural ="Salida Madryn"
        verbose_name = "Salida"
    def __unicode__(self):
         return force_unicode(self.observaciones)

class DetallesalidaMadryn(models.Model):
     iddetsalida = models.AutoField(primary_key=True, db_column='idDetSalida',verbose_name='Det.Salida')
     idsalida = models.ForeignKey(VwSalidamadryn, db_column='idSalida',verbose_name='Salida') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
        db_table = u'detalleSalida'
        verbose_name_plural ="Detalle Salida Madryn"
	verbose_name='Detalle Salida'
	unique_together = ("idsalida","idarticulo")
     def __unicode__(self):
        return force_unicode('')

class VwSalidarw(models.Model):
    idsalida = models.AutoField(primary_key=True, db_column='idSalida',verbose_name='Salida')
    fecha = models.DateField(null=True)
    entregadoa = models.CharField(max_length=200, db_column='entregadoA',verbose_name='Entregado a') 
    destino = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=200,blank=True,)
    iddeposito = models.ForeignKey(Deposito,db_column='idDeposito',default=5, editable=False,verbose_name='Depósito') 
    
    class Meta:
        db_table = u'VW_salidaRw'
	verbose_name_plural ="Salida Rawson"
        verbose_name = "Salida"
    def __unicode__(self):
         return force_unicode(self.observaciones)

class DetallesalidaRw(models.Model):
     iddetsalida = models.AutoField(primary_key=True, db_column='idDetSalida',verbose_name='Det.Salida')
     idsalida = models.ForeignKey(VwSalidarw, db_column='idSalida',verbose_name='Salida') 
     cantidad = MinMaxFloat(max_value=1000000000000, min_value=0.0)
     idarticulo = models.ForeignKey(Articulo, db_column='idArticulo',verbose_name='Artículo') 
     err = models.BooleanField(default=True,verbose_name='!')
     deterr = models.CharField(max_length=200,verbose_name='Detalles err')

     class Meta:
        db_table = u'detalleSalida'
        verbose_name_plural ="Detalle Salida Rawson"
	verbose_name='Detalle Salida'
	unique_together = ("idsalida","idarticulo")
     def __unicode__(self):
        return force_unicode('')


#*********************************************************************************************************************************
#***MODELOS-DJANGO****************************************************************************************************************
#*********************************************************************************************************************************

class AuthUser(models.Model):
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
    def __unicode__(self):
        return force_unicode(self.username)    
        
class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        db_table = u'django_content_type'
    def __unicode__(self):
        return force_unicode(self.name)    
        
class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = u'django_session'
    def __unicode__(self):
        return force_unicode(self.session_data)    
        
class Log(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey(DjangoContentType)
    object_id = models.TextField()
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = u'django_admin_log'
    def __unicode__(self):
        return force_unicode(self.user)
