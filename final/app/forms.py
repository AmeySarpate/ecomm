from django import forms
from django.contrib.auth.models import User
from . import models


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model=models.User
        fields=('username','email','password')


class CustomerForm(forms.ModelForm):
    class Meta():
        model=models.Customer
        fields=('city','address',)


class SellForm(forms.ModelForm):
    class Meta():
        model=models.Product
        fields=('kind','color','price','image','prod_name')
