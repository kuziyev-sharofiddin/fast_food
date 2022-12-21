from rest_framework import serializers
from accounts.models import *
from .models import *
from accounts.models import CustomUser
from fast_food.models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    # order_id = OrderSerializer()
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
