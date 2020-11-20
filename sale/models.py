from decimal import Decimal

from django.utils.timezone import now
from django.db import models
from django.db.models.aggregates import Sum
# Create your models here.
from catalog.models import Product
from security.models import ModelBase
from SGAGRO.funciones2 import METHOD_PAYEMENT,STATUS_PAY

class Client(ModelBase):
    Names = models.CharField(verbose_name='Nombres',max_length=80)
    SurNames = models.CharField(verbose_name='Apellidos',max_length=80)
    IdentificationCard = models.CharField(verbose_name='Cédula',max_length=10)
    City = models.CharField(verbose_name='Ciudad',max_length=80)
    Address = models.CharField(verbose_name='Dirección',max_length=120,blank=True, null=True)
    Phone = models.CharField(verbose_name='Telefono',max_length=88)
    Email = models.EmailField(verbose_name= 'Correo Electronico',max_length=200)

    def __str__(self):
        return '{} {}'.format(self.Names,self.SurNames)

    def get_Names_SurNames(self):
        return self.Names +' '+ self.SurNames

    class Meta:
        verbose_name= 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering= ('-created_at',)

class Seller(ModelBase):
    Names = models.CharField(verbose_name='Nombres',max_length=80)
    SurNames = models.CharField(verbose_name='Apellidos',max_length=80)
    IdentificationCard = models.CharField(verbose_name='Cédula',max_length=10)
    Birthdate = models.DateField(verbose_name='Fecha de Nacimiento',null=True,blank=True)
    City = models.CharField(verbose_name='Ciudad',max_length=80)
    Address = models.CharField(verbose_name='Dirección',max_length=120)
    Phone = models.CharField(verbose_name='Telefono',max_length=88)
    Email = models.EmailField(verbose_name= 'Correo Electronico',max_length=200)

    def __str__(self):
        return '{} {}'.format(self.Names,self.SurNames)

    def get_Names_SurNames(self):
        return self.Names +' '+ self.SurNames

    class Meta:
        verbose_name= 'Vendedor'
        verbose_name_plural = 'Vendedores'
        ordering= ('-created_at',)

class Invoice(ModelBase):
    ClientId = models.ForeignKey(Client,verbose_name='Cliente',on_delete=models.PROTECT)
    SellerId = models.ForeignKey(Seller,verbose_name='Vendedor',on_delete=models.PROTECT)
    DateInvoice =models.DateField(default=now)
    WeekInvoice =models.PositiveIntegerField(verbose_name='Semana Factura',blank=True ,null=True)
    #StatusPay = models.IntegerField(choices=STATUS_PAY,blank=True ,null=True)
    SubTotal = models.DecimalField(blank=True ,null=True, max_digits=19,decimal_places=2,default=0)
    TotalPay = models.DecimalField(blank=True ,null=True, max_digits=19,decimal_places=2,default=0)
    Discount = models.DecimalField(blank=True ,null=True,max_digits=19, decimal_places=2, default=0)
    Num_Porcent_Des= models.IntegerField(blank=True ,null=True,)

    def __str__(self):
        return 'Fecha: {} Total:{}'.format(self.DateInvoice,self.TotalPay)
    
    
    class Meta:
        verbose_name ='Factura'
        verbose_name_plural = 'Facturas'
    
    def get_Details(self):
        return DetailInvoice.objects.filter(InvoiceId=self)

class DetailInvoice(ModelBase):
    ProductId = models.ForeignKey(Product,verbose_name='Producto',on_delete=models.PROTECT)
    InvoiceId = models.ForeignKey(Invoice,verbose_name='Factura',on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=1)
    Price = models.DecimalField(max_digits=19,decimal_places=2)
    Cost = models.DecimalField(max_digits=19,decimal_places=2)
    Utility = models.DecimalField(max_digits=19,decimal_places=2)
    Total = models.DecimalField(max_digits=19,decimal_places=2)
    #Discount = models.DecimalField(blank=True, null=True, max_digits=19, decimal_places=2, default=0)
    def __str__(self):
        return '{}'.format(self.Utility)

    class Meta:
        verbose_name ='Detalle Factura'
        verbose_name_plural = 'Detalles de Factura'