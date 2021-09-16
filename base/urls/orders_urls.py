from django.urls import path
from base.views import orders_views as views

urlpatterns = [
    path("add/", views.addOrderItems, name="orders-add"),
    path("myorders/", views.getMyOrders, name="getMyOrders"),
    path("<str:pk>/pay/", views.updateOrderToPaid, name="updateOrderToPaid"),
    path("<str:pk>/", views.getOrderById, name="getOrderById"),
    path("<str:pk>/update/", views.updateOrderStatus, name="getOrderById"),
    path("", views.getAllOrders, name="getAllOrders"),

]