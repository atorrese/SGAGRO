""" Client Forms """

# Django
from django import forms
# App
from purchase.models import Order,Provider
from SGAGRO.funciones2 import METHOD_PAYEMENT,STATUS_PAY

class OrderForm(forms.ModelForm):
    """Formulario y validacion de Client"""
    ProviderId= forms.ModelChoiceField(queryset=Provider.objects.filter(status=True))
    DateOrder= forms.DateField()
   # PaymentMethod= forms.ChoiceField(choices=METHOD_PAYEMENT, required=False)
    #StatusPay= forms.ChoiceField(choices=STATUS_PAY , required=False)
    TotalPay = forms.DecimalField()

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        return cleaned_data

    class Meta:
        model = Order
        fields = ['ProviderId', 'DateOrder','TotalPay']
