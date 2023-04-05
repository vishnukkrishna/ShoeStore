from django.urls import path
from . import views

urlpatterns = [

    path('', views.cart_summary, name='cart-summary'),

    path('add_cart/<int:product_id>/',views.add_cart, name="add_cart"),

    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart, name="remove_cart"),

    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',views.remove_cart_item, name="remove_cart_item"),
    
    path('apply-coupon/', views.cart_summary, name="apply_coupon"),

    path('remove-coupon/', views.remove_coupon, name="remove_coupon"),

]