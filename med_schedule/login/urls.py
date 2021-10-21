from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.userLogin, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.userLogout)
]