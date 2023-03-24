from django.db import models
from store.models import Product, Variation
from accounts.models import Account

# Create your models here.


class Coupon(models.Model):

    coupon_code = models.CharField(max_length=20)

    discount_price = models.PositiveIntegerField(default=799)

    min_amount = models.PositiveIntegerField(default=17999)

    is_expired = models.BooleanField(default=False)


    def __str__(self):
        
        return self.coupon_code


class Cart(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True,blank=True)

    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    is_paid=models.BooleanField(default=False)

    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)

    date_added = models.DateField(auto_now=True)


    def get_cart_total(self):

        cart_items = CartItem.objects.filter(cart=self.id)

        price = []

        for cart_item in cart_items:

            quantity = cart_item.quantity

            price.append(cart_item.product.price * quantity)
            # if cart_item.variant:
            #     price.append(cart_item.variant.price * quantity)

        if self.coupon:

            if self.coupon.min_amount < sum(price):

                return sum(price) - self.coupon.discount_price
            
        return sum(price)



    # Tax of cart_total
    def get_tax(self):

        return round(0.025 * self.get_cart_total(), 2)

    # tax + cart_total
    def get_grand_total(self):

        return self.get_cart_total() + self.get_tax()


    def _str_(self):

        return self.user.first_name
    


    
class CartItem(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    variant = models.ForeignKey(Variation, on_delete=models.SET_NULL, null=True, blank=True)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    is_active = models.BooleanField(default=True)



    def get_product_price(self):

        return self.product.price
    

    def get_sub_total(self):

        return self.product.price * self.quantity



    def __str__(self):

        return self.cart
