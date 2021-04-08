from django.contrib.auth.models import User
from django.db import models


class CoinsInfo(models.Model):
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


class Transaction(models.Model):
    profile = models.ForeignKey("user_account_app.Profile", on_delete=models.CASCADE)
    coin = models.ForeignKey('coins_app.CoinsInfo', on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}'
