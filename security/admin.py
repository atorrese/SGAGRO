from django.contrib import admin
from django.contrib.auth.models import Group

from security.models import GroupModule,Module,Business
from import_export import  resources
from import_export.admin import ImportExportModelAdmin
# Business
class BusinessResource(resources.ModelResource):
    class Meta:
        model= Business

class BusinessAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name','description','alias']
    list_display = ('name','description','alias','Icon')
    resource_class = BusinessResource
# Module
class ModuleResource(resources.ModelResource):
    class Meta:
        model= Module

class ModuleAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name','description']
    list_display = ('name','description','url','icon','order','available')

    resource_class = ModuleResource
# GroupModule
class GroupModuleResource(resources.ModelResource):
    class Meta:
        model= GroupModule

class GroupModuleAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name','description']
    list_display = ('name', 'descripcion','icon','get_groups','get_modules', 'priority')
    resource_class = GroupModuleResource

    def get_groups(self, obj):
        return "\n".join([g.name for g in obj.groups.all()])

    def get_modules(self, obj):
        return "\n".join([m.name for m in obj.modules.all()])

# Group
'''class GroupResource(resources.ModelResource):
    class Meta:
        model = Group

class GroupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name',)
    resource_class = GroupResource

admin.site.register(Group,GroupAdmin)'''

admin.site.register(Business,BusinessAdmin)
admin.site.register(Module,ModuleAdmin)
admin.site.register(GroupModule,GroupModuleAdmin)
