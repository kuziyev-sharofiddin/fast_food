from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views, Waiter_views, Cook_views


urlpatterns = [
    #     path('', views.login, name='login'),
    #     path('doLogout', views.doLogout, name='dologout'),
    #     path('adminis/home', views.home, name='home'),
    #     path('dologin', views.dologin, name='dologin'),
    path('waiter_home', Waiter_views.home, name='waiter_home'),
    path('cook_home', Cook_views.home, name='cook_home'),
    path('administrator/add_cook', views.add_cook, name='add_cook'),
    path('administrator/add_waiter', views.add_waiter, name='add_waiter'),

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),

]
