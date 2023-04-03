from django.urls import path
from . import views

urlpatterns = [

    path('',views.index,name="adminindex"),

    path('adminlogin', views.adminlogin, name='adminlogin'),

    path('adminlogout/', views.adminlogout, name='adminlogout'),

    path('bannerlist/', views.bannerList, name='bannerlist'),

    path('addbanner/', views.addBanner, name='addbanner'),

    path('bannerdelete/<int:id>/', views.bannerDelete, name='deletebanner'),

    path('editbanner/<int:id>/', views.editBanner, name='editbanner'),

    path('adminprofile/', views.adminProfile, name='adminprofile'),

    path('admin_password/<int:user_id>/',views.change_admin_password, name='change_admin_password'),

    path('admin_profile_edit',views.admin_profile_edit, name='admin_profile_edit'), 

    path('admin_change_dp',views.admin_change_dp  ,name='admin_change_dp'),


]