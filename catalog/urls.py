from django.urls import path

import catalog.mark.views as Mark
import catalog.category.views as Category
import catalog.product.views as Product


urlpatterns = [
    #Routes Mark
    path(route='mark/', view= Mark.Index.as_view(),name='mark.index'),
    path(route='mark/create', view= Mark.Create.as_view(),name='mark.store'),
    path(route='mark/edit/<pk>', view= Mark.Update.as_view(),name='mark.update'),
    path(route='mark/delete/<pk>', view= Mark.Delete.as_view(),name='mark.delete'),
    # Routes Category
    path(route='category/', view=Category.Index.as_view(), name='category.index'),
    path(route='category/create', view=Category.Create.as_view(), name='category.store'),
    path(route='category/edit/<pk>', view=Category.Update.as_view(), name='category.update'),
    path(route='category/delete/<pk>', view=Category.Delete.as_view(), name='category.delete'),
    # Routes Product
    path(route='product/', view=Product.Index.as_view(), name='product.index'),
    path(route='product/create', view=Product.Create.as_view(), name='product.store'),
    path(route='product/show/<pk>', view=Product.Show.as_view(), name='product.show'),
    path(route='product/edit/<pk>', view=Product.Update.as_view(), name='product.update'),
    path(route='product/delete/<pk>', view=Product.Delete.as_view(), name='product.delete'),

]