from django.db import models
from store.models import Product
from accounts.models import Account

# Create your models here.



class Wishlist(models.Model):

    wishlist_id = models.CharField(max_length=250, blank=True,null=True)

    date_added = models.DateField(auto_now=True)


    def __str__(self):

        return str(self.cart_id) 
    



class WishlistItem(models.Model):

    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)

    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=True)

    is_active = models.BooleanField(default=True)
   

    def __str__(self):
        
        return str(Product.objects.get(id=self.product.id))
    


    