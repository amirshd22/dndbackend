from ..models import Product,Reviews
from ..serializers import ProductSerializer

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q 




def is_there_more_data(request):
    offset = request.GET.get('offset')
    if int(offset) > Product.objects.all().count():
        return False
    return True


def infiniteFilter(request):
    query = request.query_params.get("keyword")
    if query == None:
        query = ""
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    return Product.objects.filter(name__icontains=query).order_by('-createdAt')[int(offset): int(offset) + int(limit)]


@api_view(["GET"])
def getProducts(request):
    qs = infiniteFilter(request)
    serializer = ProductSerializer(qs, many=True)
    return Response({
        "products":serializer.data,
        "has_more":is_there_more_data(request)
    })


@api_view(['GET'])
def getProductsByQuery(request):
    query = request.query_params.get('q')
    products = Product.objects.filter(Q(groupName__icontains=query) | Q(category__icontains=query) | Q(skinType__icontains=query) | Q(brand__icontains=query)).order_by("-createdAt")
    serializer= ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductByPk(request, pk):
    product= Product.objects.get(_id=pk)
    serializer= ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(["GET"])
def getProductByCategory(request, c):
    products = Product.objects.filter(category= c).order_by("-createdAt")
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getProductByBrand(request, b):
    products = Product.objects.filter(brand= b).order_by("-createdAt")
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getNewestProducts(request):
    products = Product.objects.all().order_by("-createdAt")
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    product= Product.objects.get(_id= pk)
    data= request.data
    user= request.user

    alreadyExists = product.reviews_set.filter(user=user).exists()
    if alreadyExists:
        content = {
            "details": "Product already reviewed"
        }
        return Response(content , status=status.HTTP_400_BAD_REQUEST)
    elif data["rating"] == 0:
        content = {
            "details": "Please select a rating"
        }
        return Response(content , status=status.HTTP_400_BAD_REQUEST)
    else:
        review= Reviews.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating= data['rating'],
            comment = data['comment']
        )
        reviews = product.reviews_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews :
            total += i.rating
        product.rating = total / len(reviews)
        product.save()

        return Response({"detail": "Review added"})