""" Client Forms """

# Django
from django import forms
# App
from sale.models import Client

class ClientForm(forms.ModelForm):
    """Formulario y validacion de Client"""
    Names= forms.CharField(min_length=2)
    SurNames= forms.CharField(min_length=2)
    IdentificationCard = forms.CharField(min_length=10,max_length=13)
    City = forms.CharField(min_length=2)
    Address= forms.CharField(min_length=2)
    Phone= forms.CharField(min_length=10)
    Email = forms.EmailField(min_length=10)
    
    def clean(self):
        cleaned_data = super(ClientForm, self).clean()
        return cleaned_data

    class Meta:
        model = Client
        fields = ['Names', 'SurNames', 'IdentificationCard','City', 'Address','Phone','Email']
