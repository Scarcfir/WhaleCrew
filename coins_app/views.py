from django.shortcuts import render, redirect
from django.views import View

from coins_app.models import CoinsInfo
from user_account_app.models import Portfolio, Profile


class AddToFavoriteView(View):

    """
    Base View class to add coins to favourite for the current user.
    """

    def get(self, request, id):
        user = request.user
        coin = CoinsInfo.objects.get(id=id)
        if coin.favourite.filter(id=user.id).exists():
            print("do")
            coin.favourite.remove(user)
            if user.portfolio_set.filter(coin=coin).exists():
                print("do4")
                Portfolio.objects.get(owner=user, coin=coin).delete()

        else:
            coin.favourite.add(user)
            print("do3")
            if not user.portfolio_set.filter(coin=coin).exists():
                print("do2")
                Portfolio.objects.create(owner=user, coin=coin)


        return redirect('IndexPage')
