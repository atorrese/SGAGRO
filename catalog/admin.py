from django.contrib import admin

# Register your models here.
from catalog.models import Mark, Category,Product
from import_export import  resources
from  import_export.admin import  ImportExportModelAdmin


# Category
class CategoryResource(resources.ModelResource):
    class Meta:
        model =Category

class CategoryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['Name']
    list_display = ('Name',)
    resource_class = CategoryResource
# Mark
class MarkResource(resources.ModelResource):
    class Meta:
        model =Mark

class MarkAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['Name']
    list_display = ('Name',)
    resource_class = MarkResource


# Product
class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['Name','CategoryId','MarkId']
    list_display = ('Name','get_category','MarkId','Cost','Price','Stock','Availabel',)

    resource_class = ProductResource

    def get_category(self,obj):
        return  "\n".join([c.Name for c in obj.CategoryId.all()])

admin.site.register(Mark,MarkAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)



