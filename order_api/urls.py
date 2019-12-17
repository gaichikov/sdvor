from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from .views import orders, orders_detail, items, login_jwt

urlpatterns = [
    path('orders/<int:pk>/', orders_detail, name='orders'),
    path('orders', orders, name='orders'),
    path('items', items, name='items'),

    path('login_jwt', login_jwt, name='login_jwt'),

]


