from django.contrib import admin
from import_export import  resources
from  import_export.admin import  ImportExportModelAdmin
# Register your models here.
from sale.models import Client, Seller


# Client
class ClientResource(resources.ModelResource):
    class Meta:
        model = Client

class ClientAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['Names','SurNames','City','Address','Email']
    list_display = ('Names','SurNames','City','Address','Phone','Email',)

    resource_class = ClientResource
# Seller
class SellerResource(resources.ModelResource):
    class Meta:
        model = Seller

class SellerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['Names','SurNames','IdentificationCard','Birthdate','City','Address','Email']
    list_display = ('Names','SurNames','IdentificationCard','Birthdate','City','Address','Phone','Email',)

    resource_class = SellerResource

# Supervisor
admin.site.register(Client,ClientAdmin)
admin.site.register(Seller,SellerAdmin)

