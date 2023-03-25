from django.urls import path
from . import views

urlpatterns = [

    path('brandlist/', views.brandManagement, name='brandmanagement'),

    path('addbrand/', views.addBrand, name='addbrand'),

    path('editbrand/<int:id>/', views.editBrand, name='editbrand'),

    path('deletebrand/<int:id>/', views.deleteBrand, name='deletebrand'),

    path('productlist/', views.productManagement, name='productmanagement'),

    path('addproduct/', views.addProducts, name='addproduct'),

    path('deleteproduct/<int:id>/', views.deleteProduct, name='deleteproduct'),

    path('editproduct/<int:id>/', views.editProduct, name='editproduct'),

    path('variants/', views.variantsList, name='variantslist'),

    path('addcolor/', views.addColor, name='addcolor'),

    path('addvariant/', views.addVariant, name='addvariant'),

    path('editvariant/<int:id>/', views.editVariant, name='editvariant'),

    path('deletevariant/<int:id>/', views.deleteVariant, name='deletevariant'),


]


