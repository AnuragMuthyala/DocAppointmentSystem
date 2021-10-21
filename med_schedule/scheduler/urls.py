from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.createAppoint, name='createAppoint'),
    path('appoints/', views.priorAppoint, name='priorAppoint'),
    path('create/<str:dept>', views.bookDate, name='bookDate'),
    path('create/<str:dept>/<str:ind>', views.bookAppt, name='bookAppt')
]