from django.db import models
from accounts.models import Account

# Create your models here.


class userAddress(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100, null=True)

    phone_number = models.CharField(max_length=20, null=True)

    house_name = models.CharField(max_length=100)

    landmark = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    district = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    country = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "userAddress"
        verbose_name_plural = "userAddresss"

    def __str__(self):
        return self.house_name
