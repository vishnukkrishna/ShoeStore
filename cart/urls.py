from django.urls import path
from . import views

urlpatterns = [

    path('add_cart/<int:product_id>/',views.add_cart,name="add_cart"),

    path('remove_cart/<int:product_id>/',views.remove_cart,name="remove_cart"),

    path('remove_cart_item/<int:product_id>/',views.remove_cart_item,name="remove_cart_item"),
    
    path('', views.cart_summary, name='cart-summary'),

    

#     path('add/', views.cart_add, name='cart-add'),

#     path('delete/', views.cart_delete, name='cart-delete'),

#     path('update/', views.cart_update, name='cart-update'),
]