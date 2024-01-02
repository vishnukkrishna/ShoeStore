from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "user",
        "payment_method",
        "grand_total",
        "is_paid",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user", "payment", "delivery_address")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "order", "quantity", "order_status")
