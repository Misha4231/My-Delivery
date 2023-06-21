from .models import Customer
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms

class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('email','first_name','last_name','phone_number')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ('email','first_name','last_name','phone_number')

    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('email','first_name','last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']