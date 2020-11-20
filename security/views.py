from django.shortcuts import render


from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.models import User,Group
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, FormView
from SGAGRO.funciones import Add_Data
#
from security.models import Business
from sale.models import Invoice,DetailInvoice
from security.forms import RegisterForm
from purchase.models import Order
from django.views.defaults import page_not_found


def mi_error_404(request):
    nombre_template = '404.html'

    return page_not_found(request, template_name=nombre_template)

class LoginView(auth_views.LoginView):
    context={}
    context['Business']= Business.objects.first() 
    extra_context = context
    template_name = 'auth/login.html'
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin,auth_views.LogoutView):
    pass

class HomeView(LoginRequiredMixin,TemplateView):
    context={}
    Add_Data(context)
    date_now=datetime.now()
    '''context['year']=date_now.year
    context['week']=date_now.isocalendar()[1]#Semana empieza desde el dia Lunes y Termina el dia Domingo
    context['TotalSales']=Invoice.objects.filter(
                                            DateInvoice__year=date_now.year ,
                                            WeekInvoice=date_now.isocalendar()[1]
                                            ).count()
    context['TotalOrders']= Order.objects.filter(
                                            DateOrder__year=date_now.year ,
                                            WeekOrder=date_now.isocalendar()[1]
                                            ).count()
    totalu=DetailInvoice.objects.filter(
                                InvoiceId__DateInvoice__year = date_now.year ,
                                InvoiceId__WeekInvoice = date_now.isocalendar()[1]).aggregate(Sum('Utility'))['Utility__sum']
    context['TotalUtility']= round(totalu,2) if totalu else 0.00'''
    extra_context = context
    template_name = 'auth/home.html'

class ProfileView(LoginRequiredMixin,TemplateView):
    context={}
    Add_Data(context)
    date_now=datetime.now()
    extra_context = context
    template_name = 'auth/profile.html'


class RegisterView(FormView):
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('security:login')
    context={}
    context['Business']= Business.objects.first() 
    extra_context = context
    def form_valid(self, form):
        f = super(RegisterView, self).form_valid(form)
        print(form.cleaned_data['username'])
        user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],form.cleaned_data['password'])
        group = Group.objects.get(name='Empleados')
        #user.group_set.add(group)
        group.user_set.add(user)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        return f

    def form_invalid(self, form):
        print(form)
        return  super(RegisterView, self).form_invalid(form)

    def get(self, request, *args, **kwargs):
        get = super(RegisterView, self).get(self,request,*args,**kwargs)
        if self.request.is_ajax():
            if 'usu' in self.request.GET:
                response= User.objects.filter(username__search=self.request.GET['usu'])
            json =  [{'id':resp.id,'username':resp.username}for resp in response]
            return JsonResponse({'resp': 'ok','data':json})
        return get

''''def Filterdashboard(request):
    year = request.GET['year']
    week = request.GET['week']
    data = {}
    data['year'] = year
    data['week'] = week
    data['TotalSales'] = Invoice.objects.filter(
        DateInvoice__year=year,
        WeekInvoice=week
    ).count()
    data['TotalOrders'] = Order.objects.filter(
        DateOrder__year=year,
        WeekOrder=week
    ).count()
    totalu = DetailInvoice.objects.filter(
        InvoiceId__DateInvoice__year=year,
        InvoiceId__WeekInvoice=week).aggregate(Sum('Utility'))['Utility__sum']

    data['TotalUtility'] = round(totalu, 2)if totalu else 0.00
    return JsonResponse(data)'''
