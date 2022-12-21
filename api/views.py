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
from django.db.models import Sum
from django.db.models import F
import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import requests


def get_orders_by_status(statuses):
    orders = Order.objects.filter(status__in=statuses)
    orders_serialized = OrderSerializer(orders, many=True).data

    for order in orders_serialized:
        order_products = OrderProduct.objects.filter(order=order["id"])
        order['records'] = OrderProductSerializer(
            order_products, many=True).data
    return orders_serialized


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list(request):
    if request.method == 'GET':
        status = request.GET.getlist('status')
        return Response(get_orders_by_status(status))

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
        print(op.id)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
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
        if order.status == "NEW":
            order.status = 'PROCESS'
            serializer = OrderSerializer(
                order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif order.status == "PROCESS":
            order.status = 'DONE'
            serializer = OrderSerializer(
                order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_product_list(request):
    totals = []
    for queryset in OrderProduct.objects.all():
        totals.append({
            "product_id": queryset.product.id,
            "product": queryset.product.name,
            "total": queryset.price * queryset.quantity
        })

    return Response(totals)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def total_order_product(request):

    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        print(datetime.datetime.strptime(start_date, '%d-%m-%Y'))
        if start_date is None:
            start_date = datetime.date.today()
        else:
            start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y')

        if end_date is None:
            end_date = datetime.date.today()
        else:
            end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y')

        order_product_total = OrderProduct.objects.filter(order__created_at__range=(start_date, end_date)).aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total']
        return Response({
            "order_product_total": order_product_total
        })

    elif request.method == 'POST':
        serializer = OrderProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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


@ api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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


@ api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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


@ api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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


@ api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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
