from django.contrib import admin
from purchase.models import Provider
from import_export  import resources
from import_export.admin import  ImportExportModelAdmin
# Provider
class ProviderResource(resources.ModelResource):
    class Meta:
        model = Provider

class ProviderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['BussinessName','Ruc','Phone','Email']
    list_display = ('BussinessName','Ruc','Phone','Email',)
    resource_class = ProviderResource

admin.site.register(Provider,ProviderAdmin)

