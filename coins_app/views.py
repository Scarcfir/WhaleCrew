from django.shortcuts import render, redirect
from django.views import View

from coins_app.models import CoinsInfo
from user_account_app.models import Portfolio


class AddToFavoriteView(View):

    def get(self, request, id):
        user = request.user
        coin = CoinsInfo.objects.get(id=id)
        if not user.portfolio_set.filter(coin=coin).exists():
            Portfolio.objects.create(owner=user, coin=coin)
        if coin.favourite.filter(id=user.id).exists():
            coin.favourite.remove(user)
        else:
            coin.favourite.add(user)
        return redirect('IndexPage')
