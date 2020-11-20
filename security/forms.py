from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombres',widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Apellidos',widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField( label='Nombre Usuario',widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Correo Electronico',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        return cleaned_data

    class Meta:
        model= User
        fields = ('first_name','last_name','username','email','password',)