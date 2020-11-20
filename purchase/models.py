from django.db import models

from django.utils.timezone import now

from django.db import models

# Create your models here.
from SGAGRO.funciones2 import METHOD_PAYEMENT, STATUS_PAY
from catalog.models import Product
from security.models import ModelBase


class Provider(ModelBase):
    BussinessName = models.CharField(verbose_name='Razón Social',max_length=80)
    Ruc = models.CharField(verbose_name='Razón Social',max_length=13)
    Phone = models.CharField(verbose_name='Telefono',max_length=80)
    Email= models.EmailField(verbose_name='Correo Electronico', max_length=80)

    def __str__(self):
        return '{}'.format(self.BussinessName)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering= ('-created_at',)

    def have_orders(self):
        return Order.objects.filter(Provider=self).exists()


class Order(ModelBase):
    ProviderId = models.ForeignKey(Provider,verbose_name='Proveedor',on_delete=models.PROTECT)
    DateOrder =models.DateField(default=now)
    WeekOrder = models.PositiveIntegerField(verbose_name='Semana Orden', blank=True, null=True)
    DelieverOrder =models.DateField(null=True,blank=True)
    #PaymentMethod =models.IntegerField(choices=METHOD_PAYEMENT,blank=True, null=True)
    #StatusPay = models.IntegerField(choices=STATUS_PAY,blank=True,null=True)
    Delivery = models.BooleanField(default=False)
    TotalPay = models.DecimalField(max_digits=19,decimal_places=2)

    def __str__(self):
        return 'Fecha: {} Total:{}'.format(self.DateOrder,self.TotalPay)

    class Meta:
        verbose_name ='Pedido de Compra'
        verbose_name_plural = 'Pedidos de Compras'
    def get_Details(self):
        return DetailOrder.objects.filter(OrderId=self)



class DetailOrder(ModelBase):
    ProductId = models.ForeignKey(Product,verbose_name='Producto',on_delete=models.PROTECT)
    OrderId = models.ForeignKey(Order,verbose_name='Orden de Compra',on_delete=models.PROTECT)
    Quantity = models.IntegerField(default=1)
    Price = models.DecimalField(max_digits=19,decimal_places=2)
    Discount = models.DecimalField(max_digits=19,decimal_places=2 ,default=0.00)
    Total = models.DecimalField(max_digits=19,decimal_places=2)

    def __str__(self):
        return '{}'.format(self.ProductId.Name)

    class Meta:
        verbose_name ='Detalle Pedido de Compra'
        verbose_name_plural = 'Detalles de Pedidos de Compra'

