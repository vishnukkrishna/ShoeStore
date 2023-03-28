from django.urls import path
from . import views



urlpatterns = [

    path('userlist/', views.userManagement, name='usermanagement'),

    path('blockunblock/<int:id>', views.blockUnblock, name='blockunblock'),

    path('edituser/<int:id>', views.editUser, name='edituser'),

    path('review-managemet/', views.review_management, name="review_management"),

    path('remove-review/<int:id>/', views.remove_review, name="remove_review"),


]