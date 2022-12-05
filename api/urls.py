from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from api import views


# router = routers.DefaultRouter()
# router.register(r'orders', views.OrderViewSet, basename='order')

# urlpatterns = router.urls


urlpatterns = [
    path('orders/', views.order_list),
    path('order/<int:pk>/', views.order_detail),
    path('products/', views.product_list),
    path('product/<int:pk>/', views.product_detail),
    path('order_products/', views.order_product_list),
    path('order_product/<int:pk>/', views.order_product_detail),
    path('customusers/', views.customuser_list),
    path('customuser/<int:pk>/', views.customuser_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
