""" Invoice Views """
import json
# Django
from decimal import Decimal

from django.utils.timezone import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

# App
from SGAGRO.funciones import Add_Data
from SGAGRO.funciones2 import  STATUS_PAY,METHOD_PAYEMENT
from catalog.models import Product
from utils.mixins import OldDataMixin
from sale.invoice.forms import InvoiceForm
from sale.models import Invoice, Client, Seller, DetailInvoice

#from utils.conexion import Info


class Index(LoginRequiredMixin, ListView, OldDataMixin):
    """Lista las Invoices"""
    template_name = 'sale/invoices/index.html'
    model = Invoice
    paginate_by = 15
    context_object_name = 'invoices'
    attributes = {'search': ''}

    def get_queryset(self):
        search = self.get_old_data('search')


        return Invoice.objects.filter(
            Q(ClientId__Names__icontains=search)| Q(ClientId__SurNames__icontains=search)|
            Q(SellerId__Names__icontains=search)| Q(SellerId__SurNames__icontains=search)
        ).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        Add_Data(context)
        return self.get_all_olds_datas(context=context, attributes=self.attributes)


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




class Create(LoginRequiredMixin, CreateView, OldDataMixin):
    """Crea una Invoice"""
    model = Invoice
    template_name = 'sale/invoices/create.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sale:invoice.index')
    attributes = {
                     'DateInvoice':datetime.now().strftime('%Y-%m-%d'),


    }

    def form_valid(self, form):
        new_invoice = form.save(commit=False)        
        new_invoice.WeekInvoice= new_invoice.DateInvoice.isocalendar()[1]
        new_invoice.Num_Porcent_Des= 0
        new_invoice.save()
        print(self.request.POST['details'])
        details = json.loads(self.request.POST['details'])
        for d in details:
            product = Product.objects.get(pk=d['producto'])
            detalle = DetailInvoice(
                                        ProductId=product,
                                        InvoiceId=new_invoice,
                                        Quantity=int(d['cantidad']),
                                        Price=Decimal(d['precio']),
                                        Cost=product.Cost,
                                        Utility=Decimal(d['precio'])-Decimal(product.Cost),
                                        Total=Decimal(d['total'])
            )
            detalle.save()
            product.Stock -= int(d['cantidad'])
            product.save()
            print('Cantidad: ',d['cantidad'])
            print('Producto: ',product)
            print('Detalle: ',detalle)
        return super(Create, self).form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
        return super(Create, self).form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        Add_Data(context)
        context['old_client'] = self.post_old_data('ClientId')
        context['clients'] = Client.objects.filter(status=True)
        context['old_seller'] = self.post_old_data('SellerId')
        context['sellers'] = Seller.objects.filter(status=True)
        context['products'] = Product.objects.filter(status=True)

        return self.post_all_olds_datas(context=context, attributes=self.attributes)


class Update(LoginRequiredMixin, UpdateView, OldDataMixin):
    """Actualiza una Invoice"""
    model = Invoice
    template_name = 'sale/invoices/edit.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sale:invoice.index')

    def get_attributes(self):
        return {
            'DateInvoice': self.get_object().DateInvoice.strftime('%Y-%m-%d')
        }

    def form_valid(self, form):
        invoice = form.save(commit=False)
        invoice.WeekInvoice = invoice.DateInvoice.isocalendar()[1]
        invoice.save()

        #Eliminando Producto del detalle y Sumando el stock a el Producto
        DetailsInvoiceOld= DetailInvoice.objects.filter(InvoiceId=invoice)
        for detailInvoice in DetailsInvoiceOld:
            detailInvoice.ProductId.Stock += detailInvoice.Quantity
            detailInvoice.ProductId.save()
            detailInvoice.delete()

        #Agregando nuevo Detalle
        details = json.loads(self.request.POST['details'])
        for d in details:
            product = Product.objects.get(pk=d['producto'])
            detalle = DetailInvoice(
                                        ProductId=product,
                                        InvoiceId=invoice,
                                        Quantity=int(d['cantidad']),
                                        Price=Decimal(d['precio']),
                                        Cost=product.Cost,
                                        Utility=Decimal(d['precio'])-Decimal(product.Cost),
                                        Total=Decimal(d['total']),
                                        Discount = 0.0
            )
            detalle.save()
            detalle.ProductId.Stock -= detalle.Quantity
            detalle.ProductId.save()


        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)

        return super(Update, self).form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        Add_Data(context)
        context['old_client'] = self.post_old_data('ClientId', self.get_object().ClientId.pk)
        context['clients'] =  Client.objects.filter(status=True)
        context['old_seller'] = self.post_old_data('SellerId', self.get_object().SellerId.pk)
        context['sellers'] =  Seller.objects.filter(status=True)
        context['DetailsInvoice']= DetailInvoice.objects.filter(InvoiceId=self.get_object().pk)
        context['products'] =  Product.objects.filter(status=True)
        context['TotalPay'] = self.object.get_object().TotalPay

        return self.post_all_olds_datas(context=context, attributes=self.get_attributes())




class Delete(LoginRequiredMixin, DeleteView):
    """Elimina una Invoice"""
    model = Invoice
    http_method_names = ['delete']

    def delete(self, request, *args, **kwargs):
        data = invoice =self.get_object()
        return JsonResponse(data)
        
"""         if invoice.PaymentMethod == 1:
            if not invoice.have_pays():
                data = {'status': True, 'message': '¡El Registro se eliminado correctamente!'}
                #invoice.delete_Details()
            else:
                data = {'status': False, 'message': '¡El registro no se  puede eliminar ya que tiene pagos asignados!'}
        else:
            data = {'status': True, 'message': '¡El Registro se eliminado correctamente!'}
            #invoice.delete_Details()
 """
        

