from django.db import models
from accounts.models import Account

# Create your models here.


class userAddress(models.Model):

    user = models.ForeignKey(Account,on_delete=models.CASCADE)

    house_name = models.CharField(max_length=100)

    landmark = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    district = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    country = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)


    def __str__(self):

        return self.house_name