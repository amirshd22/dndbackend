from django.shortcuts import render
from django.contrib.auth.models import User
from requests.sessions import Request

from ..models import Order,OrderItem, Product, ShippingAddress
from ..serializers import ProductSerializer, OrderSerializer

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
import requests
from datetime import datetime

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    orderCred = {
        'pin' : '63A01E4D9C3A023E66A0',
        'amount' : int(data["totalPrice"]),
        'callback' : 'https://DND.ir/verify/',   
    }
    if orderItems and len(orderItems) == 0:
        return Response({"details": "No order items"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # create order 
        try:
            response = requests.post("https://panel.aqayepardakht.ir/api/create", data=orderCred)
            if response.status_code == 200 and not response.text.replace('-',"").isdigit():
                url ='https://panel.aqayepardakht.ir/startpay/6102B10D5A412SSGMA'+response.text
                order = Order.objects.create(
                user=user,
                paymentMethod = data['paymentMethod'],
                shippingPrice = data['shippingPrice'],
                TotalPrice = data["totalPrice"],
                taransId = response.text
            )
            # create shipping address
                shipping = ShippingAddress.objects.create(
                    order= order,
                    address = data['shippingAddress']['address'],
                    city = data['shippingAddress']['city'],
                    postalCode = data['shippingAddress']['postalCode'],
                    phoneNumber = data['shippingAddress']['phoneNumber'],
                )
            # create orderItems and set order to orderItems relationship
                for i in orderItems:
                    product = Product.objects.get(_id=i["product"])
                    item = OrderItem.objects.create(
                        product= product,
                        order=order,
                        name = product.name,
                        qty= i["qty"],
                        price= i['price'],
                        hasOff = i["hasOff"],
                        image = product.image.url
                    )
            # update the stock
                    product.countInStock  -= item.qty
                    product.save()
                serializer = OrderSerializer(order, many=False)
                return Response(serializer.data)
        
            else:
                return Response("Error")
        except:
            return Response("Error")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all().order_by("-createdAt")
    serializer = OrderSerializer(orders , many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    try:

        order = Order.objects.get(taransId=pk)

        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order , many=False)
            return Response(serializer.data)
        else:
            return Response({"details": "Not authorize to view this order"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'details': "Order does not exist"}, status= status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
#@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(taransId=pk)
    orderItems = OrderItem.objects.filter(order=order).all()
    address = ShippingAddress.objects.get(order=order)
 
    
    data = {
    'pin' : '63A01E4D9C3A023E66A0',
    'amount' : int(order.TotalPrice),
    'transid' : order.taransId
    }
    try:
        response = requests.post('https://panel.aqayepardakht.ir/api/verify', data = data)
        if response.status_code == 200 and response.text == '1':
            order.isPaid = True
            order.paidAt = datetime.now()
            order.save()
            return Response({"message": "پرداخت با موفقیت انجام شد"}, status=status.HTTP_200_OK)
        elif response.status_code == 200 and response.text =='0':
            print(response, "else if error")
            return Response({"details": "تراکنش با موفقیت انجام نشد"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(response, "else Error")
            return Response({"details": "تراکنش با موفقیت انجام نشد"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"details": f"{e}"})

@api_view(["GET"])
@permission_classes([IsAdminUser])
def getAllOrders(request):
    orders = Order.objects.all().order_by("-createdAt")
    serializer = OrderSerializer(orders , many=True)
    return Response(serializer.data) 




@api_view(["PUT"])
@permission_classes([IsAdminUser])
def updateOrderStatus(request, pk):
    data = request.data
    try:
        order = Order.objects.get(taransId=pk)
        order.isDelivered = True
        order.deliveredAt = datetime.now()
        order.post_code = data["post_code"]
        order.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({"details": f"{e}"})
