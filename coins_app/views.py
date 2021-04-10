from django.shortcuts import render, redirect
from django.views import View

from coins_app.models import CoinsInfo, Transaction
from user_account_app.models import Portfolio, Profile


class AddToFavoriteView(View):

    """
    Base View class to add coins to favourite for the current user.
    """

    def get(self, request, id):
        user = request.user
        coin = CoinsInfo.objects.get(id=id)
        if coin.favourite.filter(id=user.id).exists():
            coin.favourite.remove(user)
            if user.portfolio_set.filter(coin=coin).exists():
                Portfolio.objects.get(owner=user, coin=coin).delete()
                tran = Transaction.objects.filter(profile=user.id)
                tran.delete()

        else:
            coin.favourite.add(user)
            if not user.portfolio_set.filter(coin=coin).exists():
                Portfolio.objects.create(owner=user, coin=coin)


        return redirect('IndexPage')
