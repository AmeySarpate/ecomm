from django.shortcuts import render
from django.contrib.auth.models import User
from . import forms
from . import models
import datetime
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
def register(request):
    registered=False
    user_form=forms.UserForm()
    cuto_form=forms.CustomerForm()
    if request.method=='POST':
        form_data=forms.UserForm(request.POST)
        customer_data=forms.CustomerForm(request.POST)

        if form_data.is_valid() & customer_data.is_valid():
            user=form_data.save()
            user.set_password(user.password)
            user.save()
            customer=customer_data.save(commit=False)
            customer.user=user

            customer.save()

            registered=True
        else:
            print("Cleaned DATA IS NOT AVILABLE")

    return render(request,'app/signup.html',{'user_form':user_form,'registered':registered,'customer_form':cuto_form})
# Create your views here.



def user_login(request,slug):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)

                return HttpResponseRedirect(reverse_lazy(slug))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("GLAT PASS")
            return HttpResponse("galata data bhar diya")
    else:
        return render(request,'app/login.html',{'nbar':'login','slug':slug,'message':'You have to login first '})





def user_login_no(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)

                return HttpResponseRedirect(reverse_lazy('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("GLAT PASS")
            return HttpResponse("galata data bhar diya")
    else:
        return render(request,'app/login.html',{'nbar':'login','slug':''})


def sell(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form_data=forms.SellForm(request.POST,request.FILES)
            if form_data.is_valid():
                product=form_data.save(commit=False)

                user=models.Customer.objects.filter(user=request.user)
                product.seller=list(user)[0]

                product.image=request.FILES['image']
                product.save()
                return HttpResponse('Yeah Product is added to our list')
            else:
                print("FORM DATA IS NOT VALID")
                return render(request,'app/sell.html',{'form':form,'nbar':'sell','error':'FORM DATA IS INVALID '})
        else:
            form=forms.SellForm()
            return render(request,'app/sell.html',{'form':form,'nbar':'sell'})


    else:
        return HttpResponseRedirect(reverse('login_param',args=['sell']))



class ProductListView(ListView):
    model=models.Product
    context_object_name='product_list'


def buy(request):
    if request.method=='POST':
        c=request.POST.get('color')
        k=request.POST.get('kind')
        if len(k)==0  and len(k)==0 :
            product_list=models.Product.objects.filter(booked=False)
        elif len(c)==0:
            product_list=models.Product.objects.filter(kind=models.Kind.objects.get(category=k.title()),booked=False)
        elif len(c)==0 and len(k)==0:
            product_list=models.Product.objects.filter(color=models.Color.objects.get(color_name=c.title()),booked=False)
        else:
            product_list=models.Product.objects.filter(kind=models.Kind.objects.get(category=k),color=models.Color.objects.get(color_name=c.title()),booked=False)
    else:
        product_list=models.Product.objects.filter(booked=False)
    return render(request,'app/sell_products.html',{'product_list':product_list,'nbar':'buy'})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def index(request):
    return render(request,'app/index.html',{'nbar':'index'})

class productDetailView(DetailView):
    model=models.Product
    context_object_name='product'
    template_name='app/product_details.html'


def purchase(request,pk):
    if request.user.is_authenticated:
        object=models.Product.objects.get(id=pk)
        object.booked=True
        object.save()
        print("Object has been sold----------------------------")
        user=User.objects.get(id=request.user.id)
        buyer=models.Customer.objects.get(user=user)
        purchase_data=models.Purchase(object=object,Buyer=buyer)
        purchase_data.date=datetime.datetime.now()
        purchase_data.save()

        print('You have succesfully purchased---------------------------------------------------------')
        return HttpResponseRedirect(reverse('buy'))
    else:
        return HttpResponseRedirect(reverse('login_param',args=['buy']))
