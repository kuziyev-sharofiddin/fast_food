from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from accounts.models import CustomUser
from django.db.models import Q

# class OrderViewSet(viewsets.ModelViewSet):

#     def create(self, request, *args, **kwargs):
#         order_data = request.data
#         # new_order = Order.objects.create(
#         #     crated_at=order_data['order_id']['crated_at'], crated_by=order_data['order_id']['crated_by'], status=order_data['order_id']['status'])
#         # new_product = Product.objects.create(
#         #     name=order_data['product_id']['name'], price=order_data['product_id']['price'])
#         order_product = OrderProduct.objects.create(
#             order_id=Order.objects.get('order_id'), product_id=Product.objects.get('product_id'), quantity=['quantity'])
#         order_product.save()

#         order_serializer = OrderProductSerializer(order_product)
#         return Response(order_serializer.data)


@api_view(['GET', 'POST'])
def order_list(request):
    # if request.method == 'GET':
    #     products = OrderProduct.objects.all()
    #     serializer = OrderProductSerializer(products, many=True)
    #     return Response(serializer.data)

    if request.method == 'GET':
        orders = Order.objects.filter(Q(status="NEW") | Q(status="PROCESS"))
        orders_serialized = OrderSerializer(orders, many=True).data

        for order in orders_serialized:
            order_products = OrderProduct.objects.filter(order=order["id"])
            order['records'] = OrderProductSerializer(
                order_products, many=True).data

        return Response(orders_serialized)

    elif request.method == 'POST':
        order_data = request.data
        print(order_data['created_by'])
        createdUser = CustomUser.objects.get(id=order_data['created_by'])
        order = Order.objects.create(created_by=createdUser)
        for record in order_data["records"]:
            product = Product.objects.get(id=record["product_id"])

            op = OrderProduct(
                order=order, product=product, quantity=record["quantity"], price=product.price)
            op.save()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def order_detail(request, pk):

    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        print(order.status)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        if order:
            order.status = 'PROCESS'
            serializer = OrderSerializer(
                order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def order_product_list(request):

    if request.method == 'GET':
        order_products = OrderProduct.objects.all()
        serializer = OrderProductSerializer(order_products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def order_product_detail(request, pk):

    try:
        order_product = OrderProduct.objects.get(pk=pk)
    except OrderProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderProductSerializer(order_product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrderProductSerializer(order_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):

    try:
        product = Product.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def customuser_list(request):

    if request.method == 'GET':
        customusers = CustomUser.objects.all()
        serializer = CustomUserSerializer(customusers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def customuser_detail(request, pk):

    try:
        customuser = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUserSerializer(customuser)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CustomUserSerializer(customuser, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customuser.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
