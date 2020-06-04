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


            return HttpResponseRedirect(reverse('login'))
        else:
            print("Cleaned DATA IS NOT AVILABLE")

    return render(request,'app/signup.html',{'user_form':user_form,'customer_form':cuto_form,'nbar':'register'})
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
        user=User.objects.get(id=request.user.id)
        seller=models.Customer.objects.get(user=user)

        prev_list=models.Product.objects.filter(seller=seller,booked=False)
        prev_sold_list=models.Product.objects.filter(seller=seller,booked=True)
        if request.method=='POST':
            form_data=forms.SellForm(request.POST,request.FILES)
            if form_data.is_valid():
                product=form_data.save(commit=False)

                user=models.Customer.objects.filter(user=request.user)
                product.seller=list(user)[0]
                product.updated_on=datetime.datetime.now()
                product.image=request.FILES['image']
                product.save()
                form=forms.SellForm()
                return render(request,'app/sell.html',{'nbar':'sell','form':form,'message':'You have succesfully added the item to the sell list','prev_product':prev_list,'prev_sold_product':prev_sold_list})
            else:
                print("FORM DATA IS NOT VALID")
                return render(request,'app/sell.html',{'form':form,'nbar':'sell','error':'FORM DATA IS INVALID ','prev_product':prev_list,'prev_sold_product':prev_sold_list})
        else:
            form=forms.SellForm()
            return render(request,'app/sell.html',{'form':form,'nbar':'sell','prev_product':prev_list,'prev_sold_product':prev_sold_list})


    else:
        return HttpResponseRedirect(reverse('login_param',args=['sell']))


class UserUpdateView(UpdateView):
    model=User
    fields=['first_name','last_name']
    template_name='app/User_update_form.html'


def buy(request):
    if request.method=='POST':
        c=request.POST.get('color')
        k=request.POST.get('kind')
        print(c)
        print(type(c))
        print(k)
        print(type(k))

        sort=request.POST.get('price-date')
        print(sort)
        product_list=models.Product.objects.filter(booked=False)
        if sort=='Price1':
            print('-------------------------------------inside price1')
            product_list=models.Product.objects.filter(booked=False).order_by('-price')
        elif sort=='Price2':
            print('---------------------------------------------inside price2')
            product_list=models.Product.objects.filter(booked=False).order_by('price')
        elif sort=='Date1':
            product_list=models.Product.objects.filter(booked=False).order_by('-updated_on')
        elif sort=='Date2':
            product_list=models.Product.objects.filter(booked=False).order_by('updated_on')

        if k is not None:
            if len(k)==0 and len(c)==0 :
                product_list=models.Product.objects.filter(booked=False)
        #    return reverse function based on your search and latest arrival
            elif len(c)==0:
                print('In the len c==0 and buykind is called')
                return HttpResponseRedirect(reverse_lazy('buyKind', args=[k]))
            elif len(k)==0:
                print('In the len k==0 and buyColor is called')
                return HttpResponseRedirect(reverse_lazy('buyColor', args=[c]))
            else :
                product_list=models.Product.objects.filter(kind=models.Kind.objects.get(category=k),color=models.Color.objects.get(color_name=c.title()),booked=False)
    else:
        product_list=models.Product.objects.filter(booked=False)
    product_list=product_list.exclude(seller=models.Customer.objects.get(user=User.objects.get(id=request.user.id)))
    kind=models.Kind.objects.all()
    color=models.Color.objects.all()
    return render(request,'app/sell_products.html',{'product_list':product_list,'nbar':'buy','kind':kind,'color':color})

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
        object.save(update_fields=['booked'])
        user=User.objects.get(id=request.user.id)
        buyer=models.Customer.objects.get(user=user)
        purchase_data=models.Purchase(object=object,Buyer=buyer,date=datetime.datetime.now() )
        purchase_data.date=datetime.datetime.now()
        purchase_data.save()

        return HttpResponseRedirect(reverse_lazy('buy'))
    else:
        return HttpResponseRedirect(reverse('login_param',args=['buy']))

@login_required
def profile(request):
    user=User.objects.get(id=request.user.id)
    print("this is user")
    print(user)
    customer_form=forms.CustomerForm()
    customer=models.Customer.objects.get(user=user)
    prev_sold_list=models.Product.objects.filter(seller=customer,booked=True)
    prev_list=models.Product.objects.filter(seller=customer,booked=False)
    purchase_list=models.Purchase.objects.filter(Buyer=customer)
    bought_id_list=[]
    for item in purchase_list:
        print(item)
        print('------------------------------')
        bought_id_list.append(item.object.id)

    bought_list=models.Product.objects.filter(id__in=bought_id_list)
    return render(request,'app/profile.html',{'customer':customer,'prev_sold_products':prev_sold_list,'prev_products':prev_list,'bought_products':bought_list,'customer_form':customer_form})


def edit_user(request):
    if request.method=='POST':
        user=User.objects.get(id=request.user.id)

        user.email=request.POST.get('email')
        user.first_name=request.POST.get('fname')
        user.last_name=request.POST.get('lname')
        user.save()
        return HttpResponseRedirect(reverse_lazy('profile'))


class ProductDeleteView(DeleteView):
    model=models.Product
    success_url=reverse_lazy('profile')
    template_name='app/product_details.html'
    def get(self, request, *args, **kwargs):
        product=models.Product.objects.get(pk=kwargs['pk'])
        print(kwargs['pk'])
        context = {'message': 'Are you sure you want to delete??','product':product}
        return render(request, "app/product_details.html", context=context)
def edit_contact(request):
    if request.method=='POST':
        user=User.objects.get(id=request.user.id)
        customer=models.Customer.get(user=user)

        customer.address=request.POST.get('address')
        customer.last_name=request.POST.get('city')
        customer.save()
        return HttpResponseRedirect(reverse_lazy('profile'))


def buyColor(request,color):


    product_list=models.Product.objects.filter(color=models.Color.objects.get(color_name=color),booked=False)
    product_list=product_list.exclude(seller=models.Customer.objects.get(user=User.objects.get(id=request.user.id)))
    kind=models.Kind.objects.all()
    col=models.Color.objects.all()
    if request.method=='POST':

        sort=request.POST.get('price-date')
        if sort=='price1':
            product_list=product_list.order_by('-price')
        elif sort=='price2':
            product_list=product_list.order_by('price')
        elif sort=='Date1':
            product_list=models.Product.objects.filter(booked=False).order_by('-updated_on')
        elif sort=='Date2':
            product_list=models.Product.objects.filter(booked=False).order_by('updated_on')
    return render(request,'app/sell_products.html',{'product_list':product_list,'nbar':'buy','kind':kind,'color':col,'message':'You searched for '+color+': ','diff_buy':'yes'});

def buyKind(request,kind):
    product_list=models.Product.objects.filter(kind=models.Kind.objects.get(category=kind),booked=False)

    knd=models.Kind.objects.all()
    col=models.Color.objects.all()
    if request.method=='POST':
        print('------------------------------------------------------request is POST')
        sort=request.POST.get('price-date')
        print(sort)
        if sort=='Price1':
            print('-------------------------------------inside price1')
            product_list=models.Product.objects.filter(kind=models.Kind.objects.get(category=kind),booked=False).order_by('-price')
        elif sort=='Price2':
            print('---------------------------------------------inside price2')
            product_list=models.Product.objects.filter(kind=models.Kind.objects.get(category=kind),booked=False).order_by('price')
        elif sort=='Date1':
            product_list=models.Product.objects.filter(booked=False).order_by('-updated_on')
        elif sort=='Date2':
            product_list=models.Product.objects.filter(booked=False).order_by('updated_on')
    product_list=product_list.exclude(seller=models.Customer.objects.get(user=User.objects.get(id=request.user.id)))
    return render(request,'app/sell_products.html',{'product_list':product_list,'nbar':'buy','kind':knd,'color':col,'message':'You searched for '+kind+': ','diff_buy':'yes'});


def buyColorKind(request):

    return render(request,'app/index.html')
