from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    path('viewaddress', views.viewAddress, name='viewaddress'), 

    path('addaddress/',views.addAddress,name='addaddress'),

    path('deleteaddress/<int:address_id>/', views.deleteAddress, name='deleteaddress'),

    path('editaddress/<int:address_id>/', views.editAddress, name='editaddress'), 
    
         
]