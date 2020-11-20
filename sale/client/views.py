""" Client Views """

# Django
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
# App
from SGAGRO.funciones import Add_Data
from utils.mixins import OldDataMixin
from sale.client.forms import ClientForm
from sale.models import Client


#from utils.conexion import Info


class Index(LoginRequiredMixin, ListView, OldDataMixin):
    """Lista las Clients"""
    template_name = 'sale/clients/index.html'
    model = Client
    paginate_by = 2
    context_object_name = 'clients'
    attributes = {'search': ''}

    def get_queryset(self):
        search = self.get_old_data('search')
        return Client.objects.filter(Names__icontains=search).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        Add_Data(context)
        return self.get_all_olds_datas(context=context, attributes=self.attributes)

    def get(self, request, *args, **kwargs):
        response = super(Index,self).get(request,*args,**kwargs)
        if self.request.is_ajax():
            clients= self.get_queryset()
            if  clients:
                data = [{'id':client.pk,'value':client.get_Names_SurNames()} for client in clients ]
            else:
                data={}
            return  JsonResponse({'data':data})
        return  response


# class Show(LoginRequiredMixin, DetailView):
#     """Muestra el detalle del dispositivo"""
#     template_name = 'Clients/Clients/show.html'
#     model = Client
#     context_object_name = 'Client'
#     info = Info()
#
#     def get_context_data(self, **kwargs):
#         context = super(Show, self).get_context_data(**kwargs)
#         try:
#             ip_address = IpAddress.objects.get(Client=self.get_object())
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
    """Crea una Client"""
    model = Client
    template_name = 'sale/clients/create.html'
    form_class = ClientForm
    success_url = reverse_lazy('sale:client.index')
    attributes = {
                     'Names': '',
                     'SurNames':'',
                     'IdentificationCard':'',
                     'City':'',
                     'Address':'',
                     'Phone':'',
                     'Email':''
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
    """Actualiza una Client"""
    model = Client
    template_name = 'sale/clients/edit.html'
    form_class = ClientForm
    success_url = reverse_lazy('sale:client.index')

    def get_attributes(self):
        return {
            'Names': self.get_object().Names,
            'SurNames': self.get_object().SurNames,
            'IdentificationCard': self.get_object().IdentificationCard,
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
    """Elimina una Client"""
    model = Client
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
