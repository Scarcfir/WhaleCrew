from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.core.paginator import Paginator
from home.models import News


class IndexView(View):

    def get(self, request):
        return render(request, "index.html")


class NewsList(View):
    def get(self, request):
        object = News.objects.all()
        objects = object.order_by("created").reverse()
        return render(request, "News_List.html", {'object_list': objects})


class News_Page(View):
    def get(self, request, id):
        objects = News.objects.get(id=id)
        return render(request, "news_page.html", {'obj': objects})


class AddArticle(View):
    def get(self, request):
        return render(request, "add_news.html")
