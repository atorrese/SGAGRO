""" Seller Forms """

# Django
from django import forms
# App
from sale.models import Seller
class SellerForm(forms.ModelForm):
    """Formulario y validacion de Seller"""
    Names= forms.CharField(min_length=2)
    SurNames= forms.CharField(min_length=2)
    IdentificationCard = forms.CharField(min_length=10,max_length=13)
    Birthdate = forms.DateField()
    City= forms.CharField(min_length=2)
    Address= forms.CharField(min_length=2)
    Phone= forms.CharField(min_length=10)
    Email = forms.EmailField(required=False,min_length=10)
    def clean(self):
        cleaned_data = super(SellerForm, self).clean()
        return cleaned_data

    class Meta:
        model = Seller
        fields = ['Names', 'SurNames','IdentificationCard','Birthdate','City','Address','Phone','Email']
