from django.db import models
from store.models import Product
from accounts.models import Account

# Create your models here.


class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class WishlistItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=True)

    quantity = models.IntegerField(null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title
