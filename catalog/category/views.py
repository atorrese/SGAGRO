'''Marks Views'''
#Django
from django.http import  JsonResponse
from django.urls import  reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
#Sgv
from SGAGRO.funciones import Add_Data
from catalog.models import Category
from catalog.category.forms import CategoryForm
from utils.mixins import OldDataMixin
class Index(LoginRequiredMixin, ListView, OldDataMixin):
    template_name = 'catalog/categories/index.html'
    model = Category
    paginate_by = 2
    context_object_name = 'categories'
    attributes = {'search':''}

    def get_queryset(self):
        search = self.get_old_data('search')
        return  Category.objects.filter(Name__icontains = search,status= True).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index,self).get_context_data(**kwargs)
        Add_Data(context)
        return self.get_all_olds_datas(context = context,attributes = self.attributes)

    def get(self, request, *args, **kwargs):
        response = super(Index,self).get(request,*args,**kwargs)
        if self.request.is_ajax():
            categories = self.get_queryset()
            data={}
            if categories:
                data = [{'id': category.pk, 'value': category.Name} for category in categories]
            return JsonResponse({'data': data})
        return response


class Create(LoginRequiredMixin,CreateView,OldDataMixin):
    model = Category
    template_name = 'catalog/categories/create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category.index')
    attributes = {'Name':''}

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
    model = Category
    template_name = 'catalog/categories/edit.html'
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category.index')

    def get_attributes(self):
        return {
            'Name': self.get_object().Name,
        }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
    
        context = super(Update, self).get_context_data(**kwargs)
        Add_Data(context)
        return self.post_all_olds_datas(context=context, attributes=self.get_attributes())


class Delete(LoginRequiredMixin, DeleteView):
    """Elimina una marca"""
    model = Category
    http_method_names = ['delete']

    def delete(self, request, *args, **kwargs):
        data = {
                'status': False,
                'message': '¡No se Elimino el Regitro. Porque esta Asociado a un Producto o varios!'
            }
        if  not self.get_object().product_set.exists():
            self.get_object().delete()
            data = {
                'status': True,
                'message': '¡El registro ha sido eliminado correctamente!'
            }
        return JsonResponse(data)

