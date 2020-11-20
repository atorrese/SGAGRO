from django.urls import path

import purchase.provider.views as Provider
#import sale.seller.views as Seller
import purchase.order.views as Order


urlpatterns = [
    #Routes provider
    path(route='provider/', view= Provider.Index.as_view(),name='provider.index'),
    path(route='provider/create', view= Provider.Create.as_view(),name='provider.store'),
    path(route='provider/edit/<pk>', view= Provider.Update.as_view(),name='provider.update'),
    path(route='provider/delete/<pk>', view= Provider.Delete.as_view(),name='provider.delete'),
    # Routes order
    path(route='order/', view=Order.Index.as_view(), name='order.index'),
    path(route='order/create', view=Order.Create.as_view(), name='order.store'),
    path(route='order/edit/<pk>', view=Order.Update.as_view(), name='order.update'),
    path(route='order/show/<pk>', view=Order.Show.as_view(), name='order.show'),
    path(route='order/delete/<pk>', view=Order.Delete.as_view(), name='order.delete'),
    ]