from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields= '__all__'
        widgets={
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields= '__all__'
        exclude= ['user']
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            
        }

class ProductForm(ModelForm):
    class Meta:
        model= Product
        fields= '__all__'
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            # 'tag': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'tag': forms.SelectMultiple(attrs={'class': 'form-control'}),

        }

class TagForm(ModelForm):
    class Meta:
        model= Tag
        fields= '__all__'
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter the Tag Name'}),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields= ['username', 'email', 'password1', 'password2']
        widgets={
            'username': forms.TextInput(attrs={'class': 'form-control form_border'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form_border'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control form_border'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form_border'}),
        }



