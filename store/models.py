from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from accounts.models import Account


# Create your models here.


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)

    slug = models.SlugField(max_length=250, unique=True)

    image = models.ImageField(upload_to="category", blank=True)

    class Meta:
        verbose_name_plural = "categories"

    # To convert object into a string
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("list_category", args=[self.slug])


# Product Model
class Product(models.Model):
    title = models.CharField(max_length=250)

    slug = models.SlugField(max_length=255)

    brand = models.ForeignKey("Brand", on_delete=models.SET_NULL, null=True)

    description = models.TextField(blank=True)

    price = models.PositiveBigIntegerField()

    image = models.ImageField(upload_to="products", blank=True)

    color = models.CharField(max_length=100, blank=True)

    stock = models.PositiveIntegerField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    is_available = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)

    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "products"

    # To convert object into a string
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_info", args=[self.slug])

    def get_product_price(self, variant):
        return self.price


# Brand Model
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(max_length=255, unique=True)

    image = models.ImageField(upload_to="brands", blank=True)

    class Meta:
        verbose_name_plural = "brands"

    # To convert object into a string
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("list_brand", args=[self.slug])


# Color Model
class Color(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_colors',null=True,blank=True)

    color = models.CharField(max_length=200)

    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name_plural = "colors"

    # To convert object into a string
    def __str__(self):
        return self.color


# Class ReviewRate Model
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    subject = models.CharField(max_length=100, blank=True)

    review = models.TextField(max_length=500, blank=True)

    rating = models.FloatField()

    image = models.ImageField(upload_to="productreview", blank=True)

    ip = models.CharField(max_length=20, blank=True)

    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


# Carousel Banner Model
class Carousel_Home(models.Model):
    carousel_img = models.ImageField(upload_to="banner")

    carousel_heading = models.CharField(max_length=200)

    carousel_text = models.CharField(max_length=200)

    def __str__(self):
        return self.carousel_heading


# Multiple Image Fields
class multipleImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    images = models.ImageField(upload_to="multipleImages")

    def __str__(self):
        return self.product.title


variation_category_choice = (("color", "color"),)


# Variation Models
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)

    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now=True)

    # def __unicode__(self):

    #     return self.variation_value

    def save(self, *args, **kwargs):
        self.variation = f"{self.color}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.color.color
