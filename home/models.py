from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=255)
    description = models.TextField(null=True)
    picture_file = models.ImageField(upload_to='static/images/article/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def get_detail_url(self):
        return f"/News/{self.id}"


##############NEWSLETTER######################

class Newsletter(models.Model):
    email = models.CharField(max_length=40)


##############COINS######################


class CryptoCoins3(models.Model):
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=20, unique=True)
    price = models.FloatField()
    usd_market_cap = models.FloatField()
    usd_24h_vol = models.FloatField()
    favourite = models.ManyToManyField(User, related_name="favourite", blank=True, default=False)

    def get_detail_url(self):
        return f"{self.id}"


class Portfolio(models.Model):
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    coins = models.ManyToManyField(CryptoCoins3, through='Wallet')


class Wallet(models.Model):
    account = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    currency = models.ForeignKey(CryptoCoins3, on_delete=models.CASCADE)
    quantity = models.FloatField()
