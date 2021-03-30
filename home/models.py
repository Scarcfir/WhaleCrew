from django.db import models
from django.conf import settings


class News(models.Model):
    title = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=255)
    description = models.TextField(null=True)
    picture_file = models.ImageField(upload_to='static/images/article/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def get_detail_url(self):
        return f"/News/{self.id}"


class Newsletter(models.Model):
    email = models.CharField(max_length=40)


class CryptoCoins2(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20)
    price = models.FloatField()
    usd_market_cap = models.FloatField()
    usd_24h_vol = models.FloatField()

    def get_detail_url(self):
        return f"/News/{self.id}"

# class Wallet(models.Model):
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
#     coins = models.ManyToManyField(CryptoCoins)
