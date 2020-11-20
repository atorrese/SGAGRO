from django.db import models
from security.models import ModelBase

class Mark(ModelBase):
    Name = models.CharField(verbose_name='Marca', max_length=100,unique=True)
    '''Image = models.ImageField()
    Image = models.ImageField(upload_to='media/mark/icon/',null=False,blank=False,error_messages={'required':'Cargar Un Imagen Para El icono de la Empresa'})

    def  Icon(self):
        if self.icon:
            return mark_safe('<img src="%s" style="width:45px; height:45px;"/>'%self.icon.url)
        else:
            return 'imagen no disponible'
    icon.short_description='Icon'''
    def __str__(self):
        return '{}'.format(self.Name)
    
    class Meta:
        verbose_name='Marca'
        verbose_name_plural='Marcas'
        ordering= ('Name',)

class Category(ModelBase):
    Name = models.CharField(verbose_name='Categoria', max_length=100, unique=True)
    '''Image = models.ImageField()
    Image = models.ImageField(upload_to='media/mark/icon/',null=False,blank=False,error_messages={'required':'Cargar Un Imagen Para El icono de la Empresa'})

    def  Icon(self):
        if self.icon:
            return mark_safe('<img src="%s" style="width:45px; height:45px;"/>'%self.icon.url)
        else:
            return 'imagen no disponible'
    icon.short_description='Icon'''
    def __str__(self):
        return '{}'.format(self.Name)
    
    class Meta:
        verbose_name='Categoria'
        verbose_name_plural='Categorias'
        ordering= ('Name',)

class Product(ModelBase):
    CategoryId = models.ForeignKey(Category,on_delete=models.PROTECT)
    MarkId = models.ForeignKey(Mark, on_delete=models.PROTECT)
    Name = models.CharField(verbose_name='Producto', max_length=100, unique=True)
    Description= models.TextField(verbose_name='Descripcion', max_length=100, unique=True)
    Cost = models.DecimalField(verbose_name='Costo',max_digits= 19, decimal_places=2)
    Price = models.DecimalField(verbose_name='Precio',max_digits= 19, decimal_places=2)
    Stock = models.IntegerField()
    Availabel = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.Name)
    
    class Meta:
        verbose_name='Producto'
        verbose_name_plural='Productos'
        ordering= ('Name',)
