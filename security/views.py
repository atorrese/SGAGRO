import json
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
from django.views.generic import ListView, TemplateView, FormView, View
from SGAGRO.funciones import Add_Data
#
from security.models import Business
from sale.models import Invoice,DetailInvoice,Client,Seller
from catalog.models import Product
from security.forms import RegisterForm
from purchase.models import Order
from django.views.defaults import page_not_found

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def mi_error_404(request):
    nombre_template = '404.html'

    return page_not_found(request, template_name=nombre_template)

class LoginView(auth_views.LoginView):
    context={}
    #context['Business']= Business.objects.first() 
    extra_context = context
    template_name = 'auth/login.html'
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin,auth_views.LogoutView):
    pass

class HomeView(LoginRequiredMixin,TemplateView):
    context={}
    Add_Data(context)
    date_now=datetime.now()
    print(date_now.year)
    context['year']=date_now.year
    context['week']=date_now.isocalendar()[1]#Semana empieza desde el dia Lunes y Termina el dia Domingo
    context['TotalSales']=Invoice.objects.filter(
                                            StatusInvoice=3,
                                            DateInvoice=date_now
                                            ).count()

    revenue =Invoice.objects.filter(
                                StatusInvoice=3,
                                DateInvoice = date_now
                                ).aggregate(Sum('TotalPay'))['TotalPay__sum']

    context['Revenue'] = round(revenue,2) if revenue else 0.00

    expenses = Order.objects.filter(
                                #StatusInvoice=3,
                                DateOrder__year = date_now.year 
                                ).aggregate(Sum('TotalPay'))['TotalPay__sum']

    context['Expenses'] = round(expenses,2) if expenses else 0.00
    context['TotalOrders']= Order.objects.filter(
                                            DateOrder=date_now
                                            ).count()
    totalu=DetailInvoice.objects.filter(
                                InvoiceId__DateInvoice = date_now ,
                                ).aggregate(Sum('Utility'))['Utility__sum']
    context['TotalUtility']= round(totalu,2) if totalu else 0.00
    #context['TopSales']=Invoice.objects.all()[10].order_by('-created_at')
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
    #context['Business']= Business.objects.first() 
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

def Filterdashboard(request):
    #year = request.GET['year']
    #week = request.GET['week']
    date = str(request.GET['date'])
    date = datetime.strptime(date, '%d-%m-%Y')
    print(date)
    data = {}
    #data['year'] = year
    #data['week'] = week
    data['date'] = date
    print(date)
    data['TotalSales'] = Invoice.objects.filter(
        DateInvoice=date,

    ).count()
    revenue =Invoice.objects.filter(
                                StatusInvoice=3,
                                DateInvoice= date
                                ).aggregate(Sum('TotalPay'))['TotalPay__sum']

    data['Revenue'] = round(revenue,2) if revenue else 0.00

    expenses = Order.objects.filter(
                                #StatusInvoice=3,
                                DateOrder = date ,
                               ).aggregate(Sum('TotalPay'))['TotalPay__sum']

    data['Expenses'] = round(expenses,2) if expenses else 0.00

    data['TotalOrders'] = Order.objects.filter(
        DateOrder=date,
       
    ).count()
    totalu = DetailInvoice.objects.filter(
        InvoiceId__DateInvoice=date
        ).aggregate(Sum('Utility'))['Utility__sum']

    data['TotalUtility'] = round(totalu, 2)if totalu else 0.00
    return JsonResponse(data)



# @csrf_exempt
# @api_view(['POST'])
# def Webhook(request):
#     print(request)
#     json_data = json.loads(request.body)
#     print(json_data)
#     return JsonResponse({})


@method_decorator(csrf_exempt, name='dispatch')
class Webhook(View):

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        for dialog in json_data:
            print(dialog)
        texto=''
        #Calculo de factura
        if json_data['queryResult']['intent']['displayName'] == 'pedido':
            factura='Pedidos{'
            total =0.0
            valor =0.0
            item=json_data['queryResult']['parameters']['pedidoInsumo']
            for pro in item:
                product = Product.objects.get(Name= pro['insumo'])
                valor= (product.Price*int(pro['number']))
                total+=float(valor)
                factura +='({}, {}, ${}, ${})'.format(pro['insumo'],pro['number'],product.Price,valor)
                if pro == item[-1]:
                    factura += ".\n} \n"
                else:
                    factura += "; \n"
            factura +='Total_Pagar (${})'.format(total) 
            texto +=factura
            texto +='\n¿Desea realizar la compra?Digite si o no'
            #print(json_data)
        #Busqueda de  producto
        if json_data['queryResult']['intent']['displayName'] == 'catalogo':
            products = Product.objects.all()
            p=''
            for pro in products:
                p += "{} STOCK {} PVP $ {}".format(pro.Name,pro.Stock,pro.Price)
                if pro == products.last():
                    p += ". \n"
                else:
                    p += ", \n"
            texto =json_data['queryResult']['fulfillmentText']+ "\n "+p
        #Confirmar Pedido
        if json_data['queryResult']['intent']['displayName'] == 'confirmarPedido':
           params =json_data['queryResult']['outputContexts'][1]['parameters']
           client= Client.objects.filter(IdentificationCard=params['cedula']['dni-person'])
           if not client.exists():
               client = Client(
                   Names= params['nombres-apellidos']['nombres.original'],
                   SurNames= params['nombres-apellidos']['apellidos.original'],
                   IdentificationCard=params['cedula']['dni-person'],
                   City= params['geo-city'],
                   Address= params['street-address.original'],
                   Phone = params['phone-number'],
                   Email= params['email.original']
               )
               client.save()
           else:
               client= Client.objects.get(IdentificationCard=params['cedula']['dni-person'])   
           seller= Seller.objects.get(IdentificationCard='0940113315')
           factura= Invoice(ClientId= client, SellerId=seller)
           factura.save()
          
           items=json_data['queryResult']['outputContexts'][0]['parameters']['pedidoInsumo']
           print(items)
           print('---------------------------------¬\n')

           for i in items:
               print(i)

           total = 0.0
           for item in items:
               product = Product.objects.get(Name= item['insumo'])
               detail=DetailInvoice(
                   ProductId = product,
                   InvoiceId = factura,
                   Quantity = int(item['number']),
                   Price = product.Price,
                   Cost =product.Cost,
                   Utility= product.Price - product.Cost,
                   Total = (product.Price*int(item['number']))
                   )
               detail.save()
               product.Stock -= detail.Quantity
               product.save()
               total += float(detail.Total)
           factura.TotalPay=total
           factura.save()
           texto='Su Pedido se Encuentra Reservado.Puede acercarse  al AgroServicio  con el siguiente ticket {} y con el valor a pagar e ${} '.format('1122',factura.TotalPay)
        

        json_data['fulfillmentMessages'] =[
    {
      "text": {
        "text": [
           texto
        ]
      }
    }
  ]
        
        
        return JsonResponse(json_data)