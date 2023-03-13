from django.contrib import admin
from . models import Category, Product, Brand, Color, ReviewRating, Carousel_Home, multipleImage

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('color',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}



admin.site.register(ReviewRating)

admin.site.register(Carousel_Home)

admin.site.register(multipleImage)