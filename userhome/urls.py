from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("addaddress/<int:num>/", views.addAddress, name="addaddress"),
    path(
        "deleteaddress/<int:address_id>/<int:num>/",
        views.deleteAddress,
        name="deleteaddress",
    ),
    path("editaddress/<int:address_id>/", views.editAddress, name="editaddress"),
    path(
        "defaultaddress/<int:address_id>/<int:num>/",
        views.default_address,
        name="defaultaddress",
    ),
]
