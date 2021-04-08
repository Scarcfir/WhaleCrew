from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

from coins_app.models import Transaction


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    transactions = models.ManyToManyField("coins_app.CoinsInfo", through="coins_app.Transaction")

    def __str__(self):
        return f'{self.user.email}'


class Portfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey("coins_app.CoinsInfo", on_delete=models.CASCADE)

    def get_buy_url(self):
        return reverse('BuyCoin', kwargs={'id': self.coin.id})

    @property
    def quantity(self):
        return Transaction.objects.filter(profile=self.owner.profile, coin__id=self.coin.id).aggregate(amount=Sum('quantity'))['amount'] or 0
