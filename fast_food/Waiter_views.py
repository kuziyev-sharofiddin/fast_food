from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser
from .models import *
from django.db.models import Q
from django.views import View

# from student_management.models import Course,Session_Year,CustomUser,Student,Staff,Subject,Staff_Notification,Staff_leave,Staff_Feedback,Student_Notification,Student_Feedback,Student_leave


def home(request):
    product = Product.objects.all()
    context = {
        'product': product
    }
    return render(request, 'waiter/home.html', context)
