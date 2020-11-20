""" Seller Views """

# Django
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
# App
from SGAGRO.funciones import Add_Data
from utils.mixins import OldDataMixin
from sale.seller.forms import SellerForm
from sale.models import Seller


#from utils.conexion import Info


class Index(LoginRequiredMixin, ListView, OldDataMixin):
    """Lista las Sellers"""
    template_name = 'sale/sellers/index.html'
    model = Seller
    paginate_by = 2
    context_object_name = 'sellers'
    attributes = {'search': ''}


    def get_queryset(self):
        search = self.get_old_data('search')
        if self.request.is_ajax():
            queryset=   Seller.objects.filter(Names__icontains=search)
        else:
            queryset = Seller.objects.filter(Names__icontains=search).order_by('-created_at')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):


        context = super(Index, self).get_context_data(**kwargs)
        Add_Data(context)
        return self.get_all_olds_datas(context=context, attributes=self.attributes)

    def get(self, request, *args, **kwargs):
        response = super(Index, self).get(request,*args,**kwargs)
        if self.request.is_ajax():
            sellers = self.get_queryset()
            if sellers:
                data=[{'id':seller.pk,'value':seller.get_Names_SurNames()} for seller in sellers]
            else:
                data={}
            return JsonResponse({'data':data})
        return response


#DetailInvoice.objects.filter(InvoiceId__SellerId__id=1).aggregate(Sum(F('Quantity')),Sum(F('Total')))
'''
--Form Lista 
for s in vendedores:
    list.append([s,DetailInvoice.objects.filter(InvoiceId__SellerId__id=s.pk).aggregate(Sum(F('Quantity')),Sum(F('Total')))])
    
--forma diccionario
for s in vendedores:
    list.append({'objeto':s ,'Consulta':DetailInvoice.objects.filter(InvoiceId__SellerId__id=s.pk).aggregate(Sum(F('Quantity')),Sum(F('Total')))})
    
for i in list:
    print(i)
'''

# class Show(LoginRequiredMixin, DetailView):
#     """Muestra el detalle del dispositivo"""
#     template_name = 'Sellers/Sellers/show.html'
#     model = Seller
#     context_object_name = 'Seller'
#     info = Info()
#
#     def get_context_data(self, **kwargs):
#         context = super(Show, self).get_context_data(**kwargs)
#         try:
#             ip_address = IpAddress.objects.get(Seller=self.get_object())
#             context['informations'] = self.info.get_status(target=ip_address.address)
#             context['interfaces'] = self.info.get_interface(target=ip_address.address)
#             context['addresses '] = self.info.get_ip_address(target=ip_address.address)
#         except(Exception,):
#             context['informations'] = []
#             context['interfaces'] = []
#             context['addresses'] = []
#
#         return context


class Create(LoginRequiredMixin, CreateView, OldDataMixin):
    """Crea una Seller"""
    model = Seller
    template_name = 'sale/sellers/create.html'
    form_class = SellerForm
    success_url = reverse_lazy('sale:seller.index')
    attributes = {
                     'Names': '',
                     'SurNames':'',
                     'IdentificationCard':'',
                     'Birthdate':'',
                     'City':'',
                     'Address':'',
                     'Phone':'',
                     'Email':'',
    }
    def form_valid(self, form):
        form.save()
        if self.request.is_ajax():
            data = {
                'status': True,
                'message': '¡El registro ha sido creado correctamente!'
            }
            return JsonResponse(data)
        return super().form_valid(form)
    def form_invalid(self, form):
        if self.request.is_ajax():
            data = {
                'status': False,
                'message': '¡El Formulario Tiene errores!',
                'form_errors': form.errors.as_json(),

            }
            return JsonResponse(data)
        return  super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        Add_Data(context)
        return self.post_all_olds_datas(context=context, attributes=self.attributes)


class Update(LoginRequiredMixin, UpdateView, OldDataMixin):
    """Actualiza una Seller"""
    model = Seller
    template_name = 'sale/sellers/edit.html'
    form_class = SellerForm
    success_url = reverse_lazy('sale:seller.index')

    def get_attributes(self):
        return {
            'Names': self.get_object().Names,
            'SurNames': self.get_object().SurNames,
            'IdentificationCard': self.get_object().IdentificationCard,
            'Birthdate': self.get_object().Birthdate.isoformat,
            'City': self.get_object().City,
            'Address': self.get_object().Address,
            'Phone': self.get_object().Phone,
            'Email': self.get_object().Email
        }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        Add_Data(context)
        return self.post_all_olds_datas(context=context, attributes=self.get_attributes())


class Delete(LoginRequiredMixin, DeleteView):
    """Elimina una Seller"""
    model = Seller
    http_method_names = ['delete']

    def delete(self, request, *args, **kwargs):
        data = {
                'status': False,
                'message': '¡No se Elimino el Regitro. Porque esta Asociado a una Factura o varias Facturas!'
            }
        if  not self.get_object().invoice_set.exists():
            self.get_object().delete()
            data = {
                'status': True,
                'message': '¡El registro ha sido eliminado correctamente!'
            }
        return JsonResponse(data)

