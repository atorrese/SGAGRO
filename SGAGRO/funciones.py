
from datetime import datetime

from django.db.models import Sum
#from tablib.formats import available

from security.models import GroupModule,Business

from security.business.forms import BusinessForm
from sale.models import  DetailInvoice,Invoice
from purchase.models import Order


def Add_Data(context):
    #context['GroupModules'] = GroupModule.objects.all().order_by('priority')
    #b=Business.objects
    #context['Business']= b.first() if b.exists() else None
    #context['formBusiness']= BusinessForm(instance=b.first() )if b.exists() else None
    context['now'] = datetime.now().date()

