from django.urls import path
from . import views

urlpatterns = [

    path('index/',views.index,name="adminindex"),

    path('', views.adminlogin, name='adminlogin'),

    path('adminlogout/', views.adminlogout, name='adminlogout'),

    path('bannerlist/', views.bannerList, name='bannerlist'),

    path('addbanner/', views.addBanner, name='addbanner'),

    path('bannerdelete/<int:id>/', views.bannerDelete, name='deletebanner'),

    path('editbanner/<int:id>/', views.editBanner, name='editbanner'),

]