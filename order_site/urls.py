from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    url(r'^login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^$', home, name='home')
]