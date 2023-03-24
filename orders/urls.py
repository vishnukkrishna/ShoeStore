from django.urls import path
from . import views

urlpatterns = [
    

    path('ad/ordermanagement', views.orderManagement, name='ordermanagement'),

    path('checkout/', views.checkOut, name='checkout'),

    path('ordersuccess/', views.orderSuccessfully, name='success'),

    path('orders-list/', views.orders_list, name="orders_list"),

    path('order-details/<str:order_id>/', views.order_details, name="order_details"),

    path('order-tracking/<int:item_id>/', views.order_tracking, name="tracking"),

    path('order-invoice/<str:order_id>/', views.order_invoice, name="order_invoice"),

    path('cancel-order/<int:item_id>/<str:order_id>', views.cancel_order, name="cancel_order"),

]