from django.contrib import admin
from django.urls import path
from wishlist import views


urlpatterns = [
    path("", views.wishlist, name="wishlist"),
    path("add_wishlist/<int:product_id>/", views.add_wishlist, name="add_wishlist"),
    path(
        "remove_wishlistitem/<int:product_id>/",
        views.remove_wishlistitem,
        name="remove_wishlistitem",
    ),
]
