from django.urls import path
from . import views

urlpatterns = [
    path("categorylist/", views.categoryManagement, name="categorymanagement"),
    path("editcategory/<int:id>/", views.editCategory, name="editcategory"),
    path("deletecategory/<int:id>/", views.deleteCategory, name="deletecategory"),
    path("addcategory/", views.addCategory, name="addcategory"),
]
