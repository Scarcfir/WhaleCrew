from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.core.paginator import Paginator

from home.forms import ImageForm
from home.models import News


class IndexView(View):

    def get(self, request):
        return render(request, "index.html")


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
