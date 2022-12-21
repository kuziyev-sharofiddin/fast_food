from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


@api_view(['GET', 'POST'])
def accounts_get(request):
    if request.method == 'GET':
        return Response({"success": "You are authenticated"})


@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        username = request.data["username"]
        password = request.data["password"]
        user = CustomUser(username=username)
        user = CustomUser(password=password)
        user.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "success": "success",
            "user_id": user.id,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
