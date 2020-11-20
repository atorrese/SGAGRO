from django.http import  JsonResponse
from django.urls import  reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
#Sgv
from SGAGRO.funciones import Add_Data
from security.models import Business
from security.business.forms import BusinessForm
from utils.mixins import OldDataMixin
class Create(LoginRequiredMixin,CreateView,OldDataMixin):
    model = Business
    form_class = BusinessForm
    success_url = reverse_lazy('security:home')
    attributes = {'name':'','alias':'','desciption':'','icon':''}

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
        context = super(Create,self).get_context_data(**kwargs)
        Add_Data(context)
        return  self.get_all_olds_datas(context=context,attributes=self.attributes)

class Update(LoginRequiredMixin, UpdateView, OldDataMixin):
    """Actualiza una marca"""
    model = Business
    form_class = BusinessForm
    success_url = reverse_lazy('security:home')
    template_name = 'auth/setting.html'
    context_object_name = 'Business'
    def get_attributes(self):
        return {
            'name': self.get_object().name,
            'description': self.get_object().description,
            'icon': self.get_object().icon,
            'alias': self.get_object().alias,
        }

    def form_valid(self, form):
        form.save(commit=False)
        if self.request.FILES:
            icon = self.request.FILES.get('icon')
            print(icon)
            print(self.request.FILES)
            print(self.request.FILES['icon'])
        l=form
        print(l)
        print(l.icon)
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        form.save(commit=False)
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        Add_Data(context)
        return self.post_all_olds_datas(context=context, attributes=self.get_attributes())
