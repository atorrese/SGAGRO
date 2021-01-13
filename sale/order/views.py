import json
# Django
from decimal import Decimal

from django.utils.timezone import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView ,DetailView
from SGAGRO.funciones import Add_Data
from SGAGRO.funciones2 import  STATUS_PAY,METHOD_PAYEMENT
from catalog.models import Product
from utils.mixins import OldDataMixin


from sale.models import Invoice, Client, Seller, DetailInvoice

class Index(LoginRequiredMixin, ListView, OldDataMixin):
    """Lista las Invoices"""
    template_name = 'sale/orders/index.html'
    model = Invoice
    paginate_by = 15
    context_object_name = 'invoices'
    attributes = {'search': ''}

    def get_queryset(self):
        search = self.get_old_data('search')

        print(search.split(' '))

        return Invoice.objects.filter(
            Q(ClientId__Names__icontains=search)| Q(ClientId__SurNames__icontains=search)|
            Q(SellerId__Names__icontains=search)| Q(SellerId__SurNames__icontains=search)
        ).order_by('-created_at').filter(StatusInvoice__in=[1,2])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        Add_Data(context)
        return self.get_all_olds_datas(context=context, attributes=self.attributes)


class Show(LoginRequiredMixin, DetailView):
    """Muestra el detalle del dispositivo"""
    template_name = 'sale/orders/show.html'
    model = Invoice
    context_object_name = 'Invoice'

    def get(self, request, *args, **kwargs):
        request = super(Show, self).get(request, *args, **kwargs)
        try:
           if self.request.is_ajax():
                detail =[{
                            'quantity':i.Quantity,
                            'price': i.Price,
                            'total': i.Total,
                            'product':{
                                        'name':i.ProductId.Name,
                                        'mark':i.ProductId.MarkId.Name,
                                        'category':i.ProductId.CategoryId.Name,
                            },
                          } for i in self.get_object().get_Details()]
                invoice = {
                  'client': self.get_object().ClientId.get_Names_SurNames(),
                  'seller': self.get_object().SellerId.get_Names_SurNames(),
                  'date': self.get_object().DateInvoice.strftime("%d-%m-%Y"),
                  'total': self.get_object().TotalPay,
                  'detail': detail,
                }
                return JsonResponse({'resp':'ok','invoice':invoice})
        except Exception as e:
            print(e)

        return self.get_template_names()

    def get_context_data(self, **kwargs):
        context = super(Show, self).get_context_data(**kwargs)
        return context


class Show(LoginRequiredMixin, DetailView):
    """Muestra el detalle del dispositivo"""
    template_name = 'sale/invoices/show.html'
    model = Invoice
    context_object_name = 'Invoice'

    def get(self, request, *args, **kwargs):
        request = super(Show, self).get(request, *args, **kwargs)
        try:
           if self.request.is_ajax():
                detail =[{
                            'quantity':i.Quantity,
                            'price': i.Price,
                            'total': i.Total,
                            'product':{
                                        'name':i.ProductId.Name,
                                        'mark':i.ProductId.MarkId.Name,
                                        'category':i.ProductId.CategoryId.Name,
                            },
                          } for i in self.get_object().get_Details()]
                invoice = {
                  'client': self.get_object().ClientId.get_Names_SurNames(),
                  'seller': self.get_object().SellerId.get_Names_SurNames(),
                  'date': self.get_object().DateInvoice.strftime("%d-%m-%Y"),
                  'total': self.get_object().TotalPay,
                  'detail': detail,
                }
                return JsonResponse({'resp':'ok','invoice':invoice})
        except Exception as e:
            print(e)

        return self.get_template_names()

    def get_context_data(self, **kwargs):
        context = super(Show, self).get_context_data(**kwargs)
        return context





def change(request):
    print(request.POST['pk'])
    print(request.POST['StatusInvoice'])
    invoice = Invoice.objects.get(id=request.POST['pk'])
    invoice.StatusInvoice =request.POST['StatusInvoice']
    invoice.save()
    return JsonResponse({})