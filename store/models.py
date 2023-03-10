from django.db import models
from django.urls import reverse



# Create your models here.

# Category Model
class Category(models.Model):

    name = models.CharField(max_length=250, db_index=True)

    slug = models.SlugField(max_length= 250, unique=True)

    image = models.ImageField(upload_to='category', blank=True)



    class Meta:

        verbose_name_plural = 'categories'



    # To convert object into a string
    def __str__(self):

        return self.name
    


    def get_absolute_url(self):

        return reverse("list_category", args=[self.slug])





# Product Model
class Product(models.Model):

    title = models.CharField(max_length=250)

    slug = models.SlugField(max_length=255)

    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)

    description = models.TextField(blank=True)

    price = models.IntegerField()

    image = models.ImageField(upload_to='products', blank=True)

    color = models.CharField(max_length=100, blank=True)

    stock = models.IntegerField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    is_available = models.BooleanField(default=True)  

    created_date = models.DateTimeField(auto_now_add=True)

    modified_date = models.DateTimeField(auto_now=True)



    class Meta:

        verbose_name_plural = 'products'



    # To convert object into a string
    def __str__(self):

        return self.title
    


    def get_absolute_url(self):

        return reverse("product_info", args=[self.slug])
    





# Brand Model
class Brand(models.Model):

    name = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(max_length=255, unique=True)



    class Meta:

        verbose_name_plural = 'brands'



    # To convert object into a string
    def __str__(self):

        return self.name




    def get_absolute_url(self):

        return reverse("list_brand", args=[self.slug])








# Color Model
class Color(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_colors')

    color = models.CharField(max_length=200)

    slug = models.SlugField(max_length=255)



    class Meta:

        verbose_name_plural = 'colors'



    # To convert object into a string
    def __str__(self):

        return self.product.title
