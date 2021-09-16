from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class Product(models.Model):
    BRAND_NAME = [
        ("apple", "apple")
    ]
    GROUP_NAME = [
        ("airpod", "airpod"),
        ("iphone", "iphone"),
        ("macbook", "macbook"),
        ("applewatch", "applewatch"),
        ("imac", "imac"),
        ("ipad", "ipad"),
    ]
    name= models.CharField(max_length=200 , null=True,blank=True)
    image= models.ImageField(null=True,blank=True)
    brand=  models.CharField(max_length=200 , null=True,blank=True, choices=BRAND_NAME)
    groupName= models.CharField(max_length=200 , choices=GROUP_NAME,null=True,blank=True)
    description= models.TextField(null=True, blank=True)
    rating= models.DecimalField(max_digits=7, decimal_places=2, null=True,blank=True)
    numReviews= models.IntegerField(null=True, blank=True, default=0)
    countInStock= models.IntegerField(null=True, blank=True, default=0)
    hasOff = models.CharField(max_length=200,null=True,blank=True)
    hasRegister= models.BooleanField(default=False, null=True , blank=True)
    price= models.DecimalField(max_digits=7, decimal_places=0, null=True,blank=True)
    createdAt= models.DateTimeField(auto_now_add=False, null=True, blank=True)
    _id= models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Reviews(models.Model):
    product= models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    user= models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    name= models.CharField(max_length=200 , null=True,blank=True)
    rating= models.IntegerField(null=True, blank=True, default=0)
    comment= models.TextField(null=True, blank=True)
    _id= models.AutoField(primary_key=True, editable=False)
    createdAt= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.rating}-{self.name}")

class Order(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    paymentMethod= models.CharField(max_length=200 , null=True,blank=True)
    taxPrice= models.DecimalField(max_digits=7, decimal_places=2, null=True,blank=True)
    shippingPrice= models.DecimalField(max_digits=7, decimal_places=0, null=True,blank=True)
    TotalPrice= models.DecimalField(max_digits=7, decimal_places=0, null=True,blank=True)
    isPaid= models.BooleanField(default=False)
    paidAt=  models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered= models.BooleanField(default=False)
    deliveredAt= models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt=  models.DateTimeField(auto_now_add=True)
    taransId = models.CharField(max_length=500,null=True, blank=True)
    _id= models.AutoField(primary_key=True, editable=False)


    def __str__(self):
        return str(f"{self.taransId}-{self.user}- {self.isPaid}")


class OrderItem(models.Model):
    product= models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    name= models.CharField(max_length=200 , null=True,blank=True)
    qty= models.IntegerField(null=True, blank=True, default=0)
    price= models.DecimalField(max_digits=7, decimal_places=0, null=True,blank=True)
    image= models.CharField(max_length=200 , null=True,blank=True)
    _id= models.AutoField(primary_key=True, editable=False)
    hasOff = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return f"{self.name} {self.order.user}"

class ShippingAddress(models.Model):
    order= models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address=models.CharField(max_length=200 , null=True,blank=True)
    city=models.CharField(max_length=200 , null=True,blank=True)
    postalCode=models.CharField(max_length=200 , null=True,blank=True)
    shippingPrice=models.CharField(max_length=200 , null=True,blank=True)
    phoneNumber = models.CharField(max_length=200 , null=True,blank=True)
    _id= models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.order)
