""" Client Forms """

# Django
from django import forms
# App
from sale.models import Client, Seller, Invoice
from SGAGRO.funciones2 import METHOD_PAYEMENT,STATUS_PAY

class InvoiceForm(forms.ModelForm):
    """Formulario y validacion de Client"""
    ClientId= forms.ModelChoiceField(queryset=Client.objects.filter(status=True))
    SellerId = forms.ModelChoiceField( queryset=Seller.objects.filter(status=True))
    DateInvoice= forms.DateTimeField()
    #PaymentMethod= forms.ChoiceField(choices=METHOD_PAYEMENT)
    #StatusPay= forms.ChoiceField(choices=STATUS_PAY)
    #Num_Porcent_Des = forms.IntegerField()
    #Discount = forms.DecimalField(required=False)
    TotalPay = forms.DecimalField()

    def clean(self):
        cleaned_data = super(InvoiceForm, self).clean()
        return cleaned_data

    class Meta:
        model = Invoice
        fields = ['ClientId', 'SellerId', 'DateInvoice','TotalPay']
