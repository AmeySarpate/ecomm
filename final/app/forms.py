from django import forms
from django.contrib.auth.models import User
from . import models


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model=models.User
        fields=('username','email','password')
        help_texts = {
            'username': None,
            'email': None,
        }


class CustomerForm(forms.ModelForm):
    class Meta():
        model=models.Customer
        fields=('phone','city','address',)


class SellForm(forms.ModelForm):
    class Meta():
        model=models.Product
        fields=('prod_name','kind','color','price','image')


class ProductUpdateForm(forms.ModelForm):
    class Meta():
        model=models.Product
        fields=('prod_name','price')
