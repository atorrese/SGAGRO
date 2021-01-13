from django.urls import path

import sale.client.views as Client
import sale.seller.views as Seller
import sale.invoice.views as Invoice
import sale.order.views as Order

urlpatterns = [
    #Routes client
    path(route='client/', view= Client.Index.as_view(),name='client.index'),
    path(route='client/create', view= Client.Create.as_view(),name='client.store'),
    path(route='client/edit/<pk>', view= Client.Update.as_view(),name='client.update'),
    path(route='client/delete/<pk>', view= Client.Delete.as_view(),name='client.delete'),
    # Routes seller
    path(route='seller/', view=Seller.Index.as_view(), name='seller.index'),
    path(route='seller/create', view=Seller.Create.as_view(), name='seller.store'),
    path(route='seller/edit/<pk>', view=Seller.Update.as_view(), name='seller.update'),
    path(route='seller/delete/<pk>', view=Seller.Delete.as_view(), name='seller.delete'),
    # Routes invoice
    path(route='invoice/', view=Invoice.Index.as_view(), name='invoice.index'),
    path(route='invoice/create', view=Invoice.Create.as_view(), name='invoice.store'),
    path(route='invoice/edit/<pk>', view=Invoice.Update.as_view(), name='invoice.update'),
    path(route='invoice/show/<pk>', view=Invoice.Show.as_view(), name='invoice.show'),
    path(route='invoice/delete/<pk>', view=Invoice.Delete.as_view(), name='invoice.delete'),

    # Routes Order Sale
    path(route='order/', view=Order.Index.as_view(), name='ordersale.index'),
    path(route='order/show/<pk>', view=Order.Show.as_view(), name='ordersale.show'),
    path(route='order/change/', view=Order.change, name='ordersale.change'),

]