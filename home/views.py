from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.core.paginator import Paginator

from home.forms import ImageForm
from home.models import News, Newsletter, CryptoCoins3, Portfolio
import re
import crypto_coin.functions.get_binance_data as get_crypto_data


class IndexView(View):

    def get(self, request):
        get_crypto_info = get_crypto_data.update_db_crypto_coin()
        coins_to_update = []
        for coin in get_crypto_info:
            name = coin['name']
            symbol = coin['symbol']
            price = coin['price']
            usd_market_cap = format((int(coin['usd_market_cap']) / 1000000000), '.2f') if format(
                float(coin['usd_market_cap']),
                '.2f') != 0 else format(
                float(coin['usd_market_cap']), '.2f')
            usd_24h_vol = format((int(coin['usd_24h_vol']) / 1000000000), '.2f') if format(
                float(coin['usd_24h_vol']), '.2f'
            ) != 0 else format(float(coin['usd_24h_vol']), '.2f')
            coin_name = CryptoCoins3.objects.values_list('name', flat=True)
            if not name in coin_name:

                CryptoCoins3.objects.create(name=name, symbol=symbol, price=price,
                                            usd_market_cap=usd_market_cap, usd_24h_vol=usd_24h_vol)
            else:
                crypto_to_update = CryptoCoins3.objects.get(name=name)
                crypto_to_update.price = price
                crypto_to_update.usd_market_cap = usd_market_cap
                crypto_to_update.usd_24h_vol = usd_24h_vol
                coins_to_update.append(crypto_to_update)

        CryptoCoins3.objects.bulk_update(coins_to_update, ['price', 'usd_market_cap', 'usd_24h_vol'])

        objects = CryptoCoins3.objects.all()
        crypto_coin = objects.order_by("usd_market_cap").reverse()
        paginator = Paginator(crypto_coin, 30)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

        list = []
        if request.user.is_authenticated:
            user_fav = request.user
            favourite_coins = user_fav.favourite.all()
            for i in favourite_coins:
                list.append(i.id)

        context = {'object_list': crypto_coin, 'paginator': obj, 'favourite_coins': list}
        return render(request, "index.html", context)

    def post(self, request):
        create = False
        email = request.POST['EMAIL']
        email_exist = list(Newsletter.objects.filter(email=email))
        if validateEmail(email) and email_exist == []:
            Newsletter.objects.create(email=email)
            create = True
        return render(request, "index.html", {'object_list': create})


class NewsList(View):
    def get(self, request):
        object = News.objects.all()
        objects = object.order_by("created").reverse()
        paginator = Paginator(objects, 6)
        page = request.GET.get('page')
        news = paginator.get_page(page)
        context = {'object_list': objects, 'news': news}
        return render(request, "News_List.html", context)


class News_Page(View):
    def get(self, request, id):
        objects = News.objects.get(id=id)
        return render(request, "news_page.html", {'obj': objects})


class AddArticle(View):

    def get(self, request):
        return render(request, "add_news.html")

    def post(self, request):
        Title = request.POST['Title']
        short_desc = request.POST['ShortDesc']
        desc = request.POST['Text']
        photo_file = request.FILES['photo']
        obj = News.objects.create(title=Title, short_desc=short_desc, description=desc, picture_file=photo_file)
        obj.save()
        object = News.objects.all()
        objects = object.order_by("created").reverse()
        return render(request, "News_List.html", {'object_list': objects})


class AddTOFavorite(View):

    def get(self, request, id):
        user = request.user
        coin = CryptoCoins3.objects.get(id=id)
        if not user.portfolio_set.filter(coin=coin).exists():
            Portfolio.objects.create(owner=user, coin=coin)
        if coin.favourite.filter(id=user.id).exists():
            coin.favourite.remove(user)
        else:
            coin.favourite.add(user)
        return redirect('IndexPage')


def validateEmail(email):
    if len(email) > 6:
        if re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', email) != None:
            return 1
    return 0


class About_Us(View):

    def get(self, request):
        return render(request, 'about_us.html')


class Branding_Guide(View):

    def get(self, request):
        return render(request, 'Branding_Guide.html')


class Regulations(View):

    def get(self, request):
        return render(request, 'Regulations.html')


class GetCandy(View):

    def get(self, request):
        return render(request, 'GetCandy.html')
