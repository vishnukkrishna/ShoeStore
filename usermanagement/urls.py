from django.urls import path
from . import views



urlpatterns = [

    path('userlist/', views.userManagement, name='usermanagement'),

    path('blockunblock/<int:id>', views.blockUnblock, name='blockunblock'),

    path('edituser/<int:id>', views.editUser, name='edituser'),


]