from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#Only in some specific city this facility is available#############################
class City(models.Model):
    city_name=models.CharField(max_length=100)
    def __str__(self):
        return self.city_name

#for sorting######################################################################
class Kind(models.Model):
    category=models.CharField(max_length=100)
    def __str__(self):
        return self.category

class Color(models.Model):
    color_name=models.CharField(max_length=40)
    def __str__(self):
        return self.color_name


# Important Models ###############################################################
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.CharField(max_length=250)
    city=models.ForeignKey(City,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username


class Product(models.Model):
    seller=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='sold_products',null=True)
    kind=models.ForeignKey(Kind,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    price=models.IntegerField()
    prod_name=models.CharField(max_length=100,default='XYZ')
    image=models.ImageField(upload_to='Product_Images/')
    booked=models.BooleanField(default=False)
    def __str__(self):
        return self.prod_name

class Purchase(models.Model):
    object=models.ForeignKey(Product,on_delete=models.CASCADE)
    Buyer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='bought_products')
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.object.prod_name
