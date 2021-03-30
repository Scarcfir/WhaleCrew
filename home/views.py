from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.core.paginator import Paginator

from home.forms import ImageForm
from home.models import News, Newsletter, CryptoCoins3
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
            usd_market_cap = format(float(coin['usd_24h_vol']), '.2f')
            usd_24h_vol = format(float(coin['usd_24h_vol']), '.2f')
            coin_name = CryptoCoins3.objects.values_list('name', flat=True)
            if not name in coin_name:
                CryptoCoins3.objects.create(name=name, symbol=symbol, price=price,
                                            usd_market_cap=usd_market_cap, usd_24h_vol=usd_24h_vol)
            else:
                crypto_to_update = CryptoCoins3.objects.get(name=name)
                crypto_to_update.price = coin['price']
                crypto_to_update.usd_market_cap = format(float(coin['usd_24h_vol']), '.2f')
                crypto_to_update.usd_24h_vol = format(float(coin['usd_24h_vol']), '.2f')
                coins_to_update.append(crypto_to_update)

        CryptoCoins3.objects.bulk_update(coins_to_update, ['price', 'usd_market_cap', 'usd_24h_vol'])
        objects = CryptoCoins3.objects.all()
        crypto_coin = objects.order_by("usd_market_cap").reverse()
        paginator = Paginator(crypto_coin, 30)
        page = request.GET.get('page')
        obj = paginator.get_page(page)
        context = {'object_list': crypto_coin, 'paginator': obj}
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


def validateEmail(email):
    if len(email) > 6:
        if re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', email) != None:
            return 1
    return 0
