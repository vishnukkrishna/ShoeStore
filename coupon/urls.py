from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    path('couponlist', views.couponManagement, name='couponlist'),    
  
         
]