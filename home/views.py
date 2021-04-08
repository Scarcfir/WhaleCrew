from django.shortcuts import render

from django.views import View
from django.core.paginator import Paginator

from footer_app.models import Newsletter
from home.models import NewsArticle as News
from coins_app.models import CoinsInfo
import re
import coins_app.functions.get_binance_data as get_crypto_data


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
            coin_name = CoinsInfo.objects.values_list('name', flat=True)
            if not name in coin_name:

                CoinsInfo.objects.create(name=name, symbol=symbol, price=price,
                                         usd_market_cap=usd_market_cap, usd_24h_vol=usd_24h_vol)
            else:
                crypto_to_update = CoinsInfo.objects.get(name=name)
                crypto_to_update.price = price
                crypto_to_update.usd_market_cap = usd_market_cap
                crypto_to_update.usd_24h_vol = usd_24h_vol
                coins_to_update.append(crypto_to_update)

        CoinsInfo.objects.bulk_update(coins_to_update, ['price', 'usd_market_cap', 'usd_24h_vol'])

        All_coins_info = CoinsInfo.objects.all()
        crypto_coin = All_coins_info.order_by("usd_market_cap").reverse()
        paginator = Paginator(crypto_coin, 30)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

        fav_coin_list = []
        if request.user.is_authenticated:
            user_fav = request.user
            favourite_coins = user_fav.favourite.all()
            for i in favourite_coins:
                fav_coin_list.append(i.id)

        context = {'object_list': crypto_coin, 'paginator': obj, 'favourite_coins': fav_coin_list}
        return render(request, "index.html", context)

    def post(self, request):
        create = False
        email = request.POST['EMAIL']
        email_exist = list(Newsletter.objects.filter(email=email))
        if validateEmail(email) and email_exist == []:
            Newsletter.objects.create(email=email)
            create = True
        return render(request, "index.html", {'object_list': create})


class NewsListView(View):

    def get(self, request):
        news_list = News.objects.all()
        objects = news_list.order_by("created").reverse()
        paginator = Paginator(objects, 6)
        page = request.GET.get('page')
        news = paginator.get_page(page)
        context = {'object_list': objects, 'news': news}
        return render(request, "News_List.html", context)


class NewsPageView(View):

    def get(self, request, id):
        objects = News.objects.get(id=id)
        return render(request, "news_page.html", {'obj': objects})


class AddArticleView(View):

    def get(self, request):
        return render(request, "add_news.html")

    def post(self, request):
        title = request.POST['Title']
        short_desc = request.POST['ShortDesc']
        desc = request.POST['Text']
        photo_file = request.FILES['photo']
        obj = News.objects.create(title=title, short_desc=short_desc, description=desc, picture_file=photo_file)
        obj.save()
        news_list = News.objects.all()
        objects = news_list.order_by("created").reverse()
        return render(request, "News_List.html", {'object_list': objects})


def validateEmail(email):
    if len(email) > 6:
        if re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', email) is not None:
            return 1
    return 0
