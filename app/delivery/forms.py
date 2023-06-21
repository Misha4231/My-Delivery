from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','address','pay_type']

class StatusChangeForm(forms.Form):
    STATUS_CHOICES = [
        ('Queue', 'Queue'),
        ('Getting_ready', 'Getting ready'),
        ('Ready', 'Ready'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES)
