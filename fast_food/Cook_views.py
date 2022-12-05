from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser
from .models import *
# from student_management.models import Course,Session_Year,CustomUser,Student,Staff,Subject,Staff_Notification,Staff_leave,Staff_Feedback,Student_Notification,Student_Feedback,Student_leave


def home(request):
    return render(request, 'cook/home.html')
