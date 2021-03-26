from django.shortcuts import render

# Create your views here.
from django.views import View
from django.core.paginator import Paginator


class IndexView(View):

    def get(self, request):
        return render(request, "index.html")


class NewsList(View):
    def get(self, request):
        return render(request, "News_List.html")


class News(View):
    def get(self, request):
        return render(request, "news_page.html")

##### PAGINATOR
#      class Recipes(View):
#       def get(self, request):
#           plan_count = Plan.objects.count()
#           racipe_list = Recipe.objects.all().order_by('-votes', 'created')
#           paginator = Paginator(racipe_list, 9)
#           page = request.GET.get('page')
#           news = paginator.get_page(page)
#           context = {'plan_count': plan_count, 'recipes': recipes}
#       return render(request, "app-recipes.html", context)
