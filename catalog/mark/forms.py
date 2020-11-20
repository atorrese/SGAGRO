from django import forms

from catalog.models import Mark

class MarkForm(forms.ModelForm):
    Name = forms.CharField(min_length=2)
    
    def clean(self):
        cleaned_data = super(MarkForm,self).clean()
        return cleaned_data
        

    class Meta:
        model = Mark
        fields = ['Name']

        widgets = {
            'Name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }
    