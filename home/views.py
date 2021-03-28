from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.core.paginator import Paginator

from home.forms import ImageForm
from home.models import News, Newsletter
import re


class IndexView(View):

    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        create = False
        email = request.POST['EMAIL']
        email_exist = list(Newsletter.objects.filter(email=email))
        print(email_exist)
        print(email)
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
