'''Marks Views'''
#Django
from django.http import  JsonResponse
from django.template.loader import render_to_string
from django.urls import  reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
#Sgv
from SGAGRO.funciones import Add_Data
from catalog.models import Product, Category, Mark
from catalog.product.forms import ProductForm
from utils.mixins import OldDataMixin
class Index(LoginRequiredMixin, ListView, OldDataMixin):
    template_name = 'catalog/products/index.html'
    model = Product
    paginate_by = 2
    context_object_name = 'products'
    attributes = {'search':''}

    def get_queryset(self):
        search = self.get_old_data('search')
        return  Product.objects.filter(Name__icontains = search,status= True).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index,self).get_context_data(**kwargs)
        Add_Data(context)
        return self.get_all_olds_datas(context = context,attributes = self.attributes)


class Show(LoginRequiredMixin, DetailView):
    """Muestra el detalle del dispositivo"""
    template_name = 'catalog/products/show.html'
    model = Product
    context_object_name = 'product'


    def get(self, request, *args, **kwargs):
        request = super(Show, self).get(request, *args, **kwargs)
        if self.request.is_ajax():
            product = {
                'CategoryId': self.get_object().CategoryId,
                'MarkId': self.get_object().MarkId,
                'Description': self.get_object().Description,
                'Name': self.get_object().Name,
                'Cost': self.get_object().Cost,
                'Price': self.get_object().Price,
                'Stock': self.get_object().Stock,
                'pk': self.get_object().pk,
            }
            item = render_to_string(self.request.GET['item_html'], context= product)
            product_resp = {
                'Mark': self.get_object().MarkId.Name if self.get_object().MarkId else 'Sin Marca',
                'Category': self.get_object().CategoryId.Name if self.get_object().CategoryId else 'Sin Marca',
                'Stock': self.get_object().Stock,
            }
            return JsonResponse({'resp':'ok','item':item,'product':product_resp,'tipo':self.request.GET['tipo']})
        return self.get_template_names()


    def get_context_data(self, **kwargs):
        context = super(Show, self).get_context_data(**kwargs)
        return context



class Create(LoginRequiredMixin,CreateView,OldDataMixin):
    model = Product
    template_name = 'catalog/products/create.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product.index')
    attributes = {
                     'Name':'',
                     'Description':'',
                     'Cost':'',
                     'Price':'',
                     'Stock':'',
                     'Availabel':True,

    }




    def form_valid(self, form):
        new_product = form.save(commit=False)
        new_product.save()
        print(new_product)
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(Create,self).get_context_data(**kwargs)
        Add_Data(context)
        context['old_category']= self.post_old_data('CategoryId')
        context['categories']= Category.objects.filter(status=True)
        context['old_mark']= self.post_old_data('MarkId')
        context['marks']= Mark.objects.filter(status=True)
        context['products'] = Product.objects.filter(status=True)

        return  self.get_all_olds_datas(context=context,attributes=self.attributes)


class Update(LoginRequiredMixin, UpdateView, OldDataMixin):
    """Actualiza una marca"""
    model = Product
    template_name = 'catalog/products/edit.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product.index')

    def get_attributes(self):
        return {
            'Name': self.get_object().Name,
            'Description': self.get_object().Description,
            'Cost': self.get_object().Cost,
            'Price': self.get_object().Price,
            'Stock': self.get_object().Stock,
            'Availabel': self.get_object().Availabel,
            'CategoryId': self.get_object().CategoryId,
            'MarkId': self.get_object().MarkId
        }

    def form_valid(self, form):
        update_product = form.save(commit=False)
        update_product.save()
        return super(Update, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        Add_Data(context)

        context['old_mark']= self.post_old_data('MarkId',self.get_object().MarkId.pk)
        context['marks']= Mark.objects.filter(status=True)
        context['products'] = Product.objects.filter(status=True)
        context['old_category'] = self.post_old_data('CategoryId',self.get_object().CategoryId.pk)
        context['categories'] = Category.objects.filter(status=True)
        return self.post_all_olds_datas(context=context, attributes=self.get_attributes())


class Delete(LoginRequiredMixin, DeleteView):
    """Elimina una marca"""
    model = Product
    http_method_names = ['delete']

    def delete(self, request, *args, **kwargs):
        data = {
                'status': False,
                'message': '¡No se Elimino el Regitro. Porque esta Asociado a una Factura u Orden Compra!'
            }
        if  not (self.get_object().detailinvoice_set.exists() or self.get_object().detailorder_set.exists()):
            self.get_object().delete()
            data = {
                'status': True,
                'message': '¡El registro ha sido eliminado correctamente!'
            }
        return JsonResponse(data)

