from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    transactions = models.ManyToManyField("home.CryptoCoins3", through="home.Transaction")

    def __str__(self):
        return f'{self.user.email}'
