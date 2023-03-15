from django.urls import path, include
from . import views

urlpatterns = [

    path('ordermanagement', views.orderManagement, name='ordermanagement'),


]