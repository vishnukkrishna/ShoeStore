from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    path('couponlist', views.couponManagement, name='couponlist'), 

    path('add_coupon',views.add_coupon,name="add_coupon"),

    path('edit-coupon/<int:id>/', views.edit_coupon, name="edit_coupon"),

    path('delete_coupon',views.delete_coupon,name="delete_coupon"),   
  
         
]