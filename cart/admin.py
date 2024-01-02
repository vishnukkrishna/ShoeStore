from django.contrib import admin
from .models import Cart, CartItem, Coupon

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "date_added", "coupon", "razor_pay_order_id")


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product", "cart", "quantity", "is_active", "variant")


admin.site.register(Cart, CartAdmin)

admin.site.register(CartItem, CartItemAdmin)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("coupon_code", "min_amount", "discount_price", "is_expired")
