from django.contrib import admin
from .models import Product, Order,OrderItem,Reviews,ShippingAddress
# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Reviews)
admin.site.register(ShippingAddress)
