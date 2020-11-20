""" Client Forms """

# Django
from django import forms
# App
from purchase.models import Provider


class ProviderForm(forms.ModelForm):
    """Formulario y validacion de Client"""
    BussinessName= forms.CharField(min_length=1)
    Ruc= forms.CharField(max_length=13)
    Phone= forms.CharField(min_length=10)
    Email = forms.EmailField(min_length=10)
    
    def clean(self):
        cleaned_data = super(ProviderForm, self).clean()
        return cleaned_data

    class Meta:
        model = Provider
        fields = ['BussinessName', 'Ruc','Phone','Email']
