from django.shortcuts import render, redirect, HttpResponse
from accounts.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import Product
from django.contrib import messages
from .forms import CustomUserForm
from django.shortcuts import render, redirect
from fast_food.models import Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
# Create your views here.


# def login(request):
#     return render(request, 'admin/login.html')


# def dologin(request):
#     if request.method == 'POST':
#         user = EmailBackEnd.authenticate(request,
#                                          username=request.POST.get('email'),
#                                          password=request.POST.get('password'))
#         if user != None:
#             # login(request, user)
#             user_type = user.user_type
#             if user_type == '1':
#                 return redirect('home')
#             elif user_type == '2':
#                 return redirect('cook_home')
#             elif user_type == '3':
#                 return redirect('waiter_home')
#             else:
#                 messages.error(request, 'Username and Password are Invalid')
#                 return redirect('login')
#         else:
#             messages.error(request, 'Username and Password are Invalid')
#             return redirect('login')

#     return render(request, 'admin/login.html')


# def doLogout(request):
#     logout(request)
#     return redirect('login')


def home(request):
    product = Product.objects.all()
    context = {
        'product': product
    }
    return render(request, 'admin/home.html', context)


def add_cook(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is Already Taken')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is Already Taken')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=2,

            )
            user.set_password(password)
            user.save()
            messages.success(request, user.first_name + " " +
                             user.last_name + "Are Successfully Added")
            return redirect('add_cook')
    return render(request, 'admin/add_cook.html')


def add_waiter(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is Already Taken')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is Already Taken')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3,

            )
            user.set_password(password)
            user.save()
            messages.success(request, user.first_name + " " +
                             user.last_name + "Are Successfully Added")
            return redirect('add_cook')
    return render(request, 'admin/add_waiter.html')


# @login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("waiter_home")


# @login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


# @login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


# @login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


# @login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


# @login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')
