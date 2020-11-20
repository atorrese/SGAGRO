from django import forms
#App
from security.models import Business

class BusinessForm(forms.ModelForm):
    name = forms.CharField(min_length=4)
    alias = forms.CharField(min_length=1)
    description = forms.CharField()
    icon = forms.FileField

    def clean(self):
        cleaned_data = super(BusinessForm,self).clean()
        return cleaned_data

    class Meta:
        model = Business
        fields  = ['name','alias','description','icon']