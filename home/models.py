from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

from account.models import Profile


class News(models.Model):
    title = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=255)
    description = models.TextField(null=True)
    picture_file = models.ImageField(upload_to='static/images/article/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def get_detail_url(self):
        return f"/News/{self.id}"

    def __str__(self):
        return f'{self.title}'


class Newsletter(models.Model):
    email = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.email}'


class CryptoCoins3(models.Model):
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=20, unique=True)
    price = models.FloatField()
    usd_market_cap = models.FloatField()
    usd_24h_vol = models.FloatField()
    favourite = models.ManyToManyField(User, related_name="favourite", blank=True, default=False)

    def get_detail_url(self):
        return f"{self.id}"

    def __str__(self):
        return f'{self.name} {self.symbol}'


class Portfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey(CryptoCoins3, on_delete=models.CASCADE)

    def get_buy_url(self):
        return reverse('BuyCoin', kwargs={'id': self.coin.id})

    @property
    def quantity(self):
        return Transaction.objects.filter(profile=self.owner.profile, coin__id=self.coin.id).aggregate(amount=Sum('quantity'))['amount'] or 0


class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    coin = models.ForeignKey(CryptoCoins3, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}'
