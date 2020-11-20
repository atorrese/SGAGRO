from django import forms
#App
from catalog.models import Product, Category, Mark

class ProductForm(forms.ModelForm):
    CategoryId = forms.ModelChoiceField(required=False,queryset= Category.objects.filter(status=True))
    MarkId = forms.ModelChoiceField(required=False,queryset= Mark.objects.filter(status=True))
    Name = forms.CharField(min_length=4 )
    Description = forms.Textarea()
    Cost= forms.DecimalField()
    Price = forms.DecimalField()
    Stock = forms.IntegerField()
    Availabel =  forms.BooleanField()

    def clean(self):
        cleaned_data = super(ProductForm,self).clean()
        return cleaned_data

    class Meta:
        model = Product
        fields  = ['Name','Description','Cost','Price','Stock','Availabel','CategoryId','MarkId',]