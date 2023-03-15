"""shoestore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # Admin url
    path('admin/', admin.site.urls),

    # Account url
    path('', include('accounts.urls')),

    # User Store url
    path('store/', include('store.urls')),

    # User Cart url
    path('cart/', include('cart.urls')),

    # User Home url
    path('userhome/', include('userhome.urls')),

    # User Wishlist url
    path('wishlist/', include('wishlist.urls')),

    # AdminAccounts url
    path('ad/', include('adminaccounts.urls')),

    # Admin User Management
    path('ad/user/', include('usermanagement.urls')),

    # Admin Product Management
    path('ad/product/', include('productmanagement.urls')),

    # Admin Category Management
    path('ad/category/', include('categorymanagement.urls')),

    # Admin Coupons Management
    path('ad/coupons/', include('coupon.urls')),

    # Admin Order Management
    path('ad/order/', include('orders.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)