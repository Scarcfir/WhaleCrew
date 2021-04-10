from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

from coins_app.models import Transaction, CoinsInfo


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    transactions = models.ManyToManyField("coins_app.CoinsInfo", through="coins_app.Transaction")

    def __str__(self):
        return f'{self.user.email}'


class PasswordRstToken(models.Model):
    token = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Portfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey("coins_app.CoinsInfo", on_delete=models.CASCADE)

    # def get_buy_url(self):
    #     return reverse('BuyCoin', kwargs={'id': self.coin.id})

    @property
    def quantity(self):
        """
        Return the quantity of User's portfolio.
        """
        return \
            float(format((Transaction.objects.filter(profile=self.owner.profile, coin__id=self.coin.id).aggregate(
                amount=Sum('quantity'))[
                              'amount'] or 0), '.2f'))

    @property
    def current_value_of_holdings(self):
        """
        Return the value of User's holdings.
        """
        value_now = (Transaction.objects.filter(profile=self.owner.profile, coin__id=self.coin.id).aggregate(
            amount=Sum('quantity'))['amount'] or 0) * CoinsInfo.objects.get(id=self.coin.id).price
        return format(float(value_now), '.2f')

    @property
    def balance(self):
        """
        Return the balance of User's holdings compared to buy costs.
        """
        actual_holdings = self.current_value_of_holdings
        list_of_transaction = Transaction.objects.filter(profile=self.owner.profile, coin__id=self.coin.id)
        average_purchase_value = 0
        for i in list_of_transaction:
            average_purchase_value += i.price * i.quantity
        average_purchase_value = '{:.2f}'.format(average_purchase_value)
        return float(format(float(actual_holdings) - float(average_purchase_value), '.2f'))
