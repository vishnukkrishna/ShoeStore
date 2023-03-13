from django.urls import path
from . import views


# Store
urlpatterns = [

    # Store main page
    path('allproduct/', views.store, name='store'),

    path('ordersuccess/', views.orderSuccessfully, name='ordersuccess'),

    # Individual product
    path('product/<slug:product_slug>/', views.product_info, name='product_info'),

    # Individual category
    path('search/<slug:category_slug>/', views.list_category, name='list_category'),

    # Individual brand
    path('brand/<slug:brand_slug>/', views.list_brand, name='list_brand'),

    path('search/', views.search, name='search'),

    path('submit_review/<int:product_id>', views.submit_review, name='submit_review'),
]
