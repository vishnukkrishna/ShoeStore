from django.contrib import admin
from . models import Category, Product, Brand, Color, ReviewRating, Carousel_Home, multipleImage, Variation

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



@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):

    list_display = ('product', 'color', 'is_active') 

    list_editable = ('is_active',)

    list_filter = ('product', 'color', 'is_active') 

    model=Variation

