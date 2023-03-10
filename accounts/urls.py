from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register', views.register, name='register'),

    path('login', views.login, name='login'),

    path('logout', views.logout, name='logout'),

    path('social-auth/', include('social_django.urls', namespace='social')),  # <-- here


    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),

    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),

    path('resetpassword/', views.resetPassword, name='resetPassword'),

    path('profile/', views.dashboard, name='dashboard'),

    path('edit_profile/<int:user_id>/', views.edit_profile, name="edit_profile"),

    path('change_password/<int:user_id>/', views.change_password, name="change_password"),



]