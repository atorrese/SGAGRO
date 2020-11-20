from django import forms
#App
from catalog.models import Category

class CategoryForm(forms.ModelForm):
    Name = forms.CharField(min_length=4)

    def clean(self):
        cleaned_data = super(CategoryForm,self).clean()
        return cleaned_data

    class Meta:
        model = Category
        fields  = ['Name']
        
        widgets = {
            'Name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }