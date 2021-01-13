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
from  SGAGRO.funciones2 import STATUS_PAY,METHOD_PAYEMENT
from catalog.models import Product
from utils.mixins import OldDataMixin
from purchase.order.forms import OrderForm
from purchase.models import Order, Provider, DetailOrder
#from utils.conexion import Info


class Index(LoginRequiredMixin, ListView, OldDataMixin):
    """Lista las Invoices"""
    template_name = 'purchase/orders/index.html'
    model = Order
    paginate_by = 15
    context_object_name = 'orders'
    attributes = {'search': ''}

    def get_queryset(self):
        search = self.get_old_data('search')


        return Order.objects.filter(
            Q(ProviderId__BussinessName__icontains=search)|
            Q(ProviderId__Ruc__icontains=search)
        ).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        Add_Data(context)
        return self.get_all_olds_datas(context=context, attributes=self.attributes)


class Show(LoginRequiredMixin, DetailView):
    """Muestra el detalle del dispositivo"""
    template_name = 'purchase/orders/show.html'
    model = Order
    context_object_name = 'Order'

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
                                        'category':i.ProductId.CategoryId.Name,
                                        'mark':i.ProductId.MarkId.Name,
                            },
                          } for i in self.get_object().get_Details()]
                order = {
                  'provider': self.get_object().ProviderId.BussinessName,
                  'date': self.get_object().DateOrder.strftime("%d-%m-%Y"),
                  #'methodpay': self.get_object().PaymentMethod,
                 # 'status': self.get_object().StatusPay,
                  'total': self.get_object().TotalPay,
                  'detail': detail,
                }
                return JsonResponse({'resp':'ok','order':order})
        except Exception as e:
            print(e)

        return self.get_template_names()

    def get_context_data(self, **kwargs):
        context = super(Show, self).get_context_data(**kwargs)
        return context




class Create(LoginRequiredMixin, CreateView, OldDataMixin):
    """Crea una Invoice"""
    model = Order
    template_name = 'purchase/orders/create.html'
    form_class = OrderForm
    success_url = reverse_lazy('purchase:order.index')
    attributes = {
                     'DateOrder':datetime.now().strftime('%Y-%m-%d'),


    }

    def form_valid(self, form):
        new_order = form.save(commit=False)
        new_order.WeekOrder = new_order.DateOrder.isocalendar()[1]
        new_order.save()
        print(new_order)
        print(self.request.POST['details'])
        details = json.loads(self.request.POST['details'])
        for d in details:
            product = Product.objects.get(pk=d['producto'])
            detalle = DetailOrder(
                                        ProductId=product,
                                        OrderId=new_order,
                                        Quantity=int(d['cantidad']),
                                        Price=Decimal(d['precio']),
                                        Total=Decimal(d['total']),
            )
            detalle.save()
            product.Stock += int(d['cantidad'])
            product.save()
            print('Cantidad: ',d['cantidad'])
            print('Producto: ',product)
            print('Detalle: ',detalle)
        return super(Create, self).form_valid(form)
    def form_invalid(self, form):
        print(form)
        print(form.errors)
        return super(Create, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        Add_Data(context)
        context['old_provider'] = self.post_old_data('ProviderId')
        context['providers'] = Provider.objects.filter(status=True)
        context['products'] = Product.objects.filter(status=True)


        return self.post_all_olds_datas(context=context, attributes=self.attributes)


class Update(LoginRequiredMixin, UpdateView, OldDataMixin):
    """Actualiza una Invoice"""
    model = Order
    template_name = 'purchase/orders/edit.html'
    form_class = OrderForm
    success_url = reverse_lazy('purchase:order.index')

    def get_attributes(self):
        return {
            'DateOrder': self.get_object().DateOrder.strftime('%Y-%m-%d'),

        }

    def form_valid(self, form):
        order = form.save(commit=False)
        order.WeekOrder = order.DateOrder.isocalendar()[1]
        order.save()
        # Eliminando Producto del detalle y Sumando el stock a el Producto
        DetailsOrderOld =DetailOrder.objects.filter(OrderId=order)
        for detailOrder  in DetailsOrderOld:
            detailOrder.ProductId.Stock -=detailOrder.Quantity
            detailOrder.ProductId.save()
            detailOrder.delete()
        #Agregando Nuevo Detalle
        details = json.loads(self.request.POST['details'])
        for d in details:
            product = Product.objects.get(pk=d['producto'])
            detalle = DetailOrder(
                ProductId=product,
                OrderId=order,
                Quantity=int(d['cantidad']),
                Price=Decimal(d['precio']),
                Total=Decimal(d['total']),
            )
            detalle.save()
            product.Stock += int(d['cantidad'])
            product.save()
            print('Cantidad: ', d['cantidad'])
            print('Producto: ', product)
            print('Detalle: ', detalle)


        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)

        return super(Update, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        Add_Data(context)
        context['old_provider'] = self.post_old_data('ProviderId', self.get_object().ProviderId.pk)
        context['providers'] =  Provider.objects.filter(status=True)
        context['products'] =  Product.objects.filter(status=True)
        context['DetailsOrder'] = DetailOrder.objects.filter(OrderId=self.get_object().pk)
        context['TotalPay'] = self.get_object().TotalPay
        return self.post_all_olds_datas(context=context, attributes=self.get_attributes())


class Delete(LoginRequiredMixin, DeleteView):
    """Elimina una Invoice"""
    model = Order
    http_method_names = ['delete']

    def delete(self, request, *args, **kwargs):
        order =self.get_object()
        order.delete_detail()
        order.delete()
        data = {
            'status' :True,
             'message': '¡El registro ha sido eliminado correctamente!'
         }
        return JsonResponse(data)
