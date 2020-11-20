from django.db import models
from django.contrib.auth.models import Group,User
from django.utils.safestring import mark_safe


from utils.mixins import OldDataMixin

#Clase Base Para eliminacion
class ModelBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True
#Clase Abstracta para Persona
'''class Persona(models.Model):
    Names = models.CharField(verbose_name='Nombres',max_length=80)
    SurNames = models.CharField(verbose_name='Apellidos',max_length=80)
    IdentificationCard = models.CharField(verbose_name='Cédula',max_length=10)
    Birthdate = models.DateField(verbose_name='Fecha de Nacimiento',null=True,blank=True)
    Ciudad = models.ForeignKey(Canton, verbose_name='Ciudad',on_delete=models.PROTECT)
    Address = models.CharField(verbose_name='Dirección',max_length=120)
    References= models.CharField(verbose_name='Referencia Domiciliaria',max_length=150)
    Phone = models.CharField(verbose_name='Telefono',max_length=88)
    Email = models.EmailField(verbose_name= 'Correo Electronico',max_length=200)
    class Meta:
        abstract = True'''


class Module(models.Model):
    url = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ('order',)


class GroupModule(models.Model):
    name = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True)
    icon = models.CharField(null=True,blank=True,max_length=100)
    modules = models.ManyToManyField(Module)
    groups = models.ManyToManyField(Group)
    priority = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Grupo de Módulos'
        verbose_name_plural = 'Grupos de Módulos'
        ordering = ('priority',)

    def module_active(self):
        return self.modules.filter(available=True).order_by('order')


class Business(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=20)
    description = models.CharField(max_length=200, blank=True)
    icon = models.ImageField(upload_to='media/Business/icon/',null=False,blank=False,error_messages={'required':'Cargar Un Imagen Para El icono de la Empresa'})

    def  Icon(self):
        if self.icon:
            return mark_safe('<img src="%s" style="width:45px; height:45px;"/>'%self.icon.url)
        else:
            return 'imagen no disponible'
    icon.short_description='Icon'

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
