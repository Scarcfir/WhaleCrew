"""WhaleCrew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from coins_app.views import *
from user_account_app.views import *
from home.views import *
from footer_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='IndexPage'),
    path('login/', LoginView.as_view(), name='Login'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('Forgot_Pass/', ForgotPass.as_view(), name='Forgot_Pass'),
    path('Sing_up/', SingUp.as_view(), name='Sing_up'),
    path('Contact/', Contact.as_view(), name='Contact'),
    path('NewsList/', NewsListView.as_view(), name='NewsList'),
    path('News/<int:id>/', NewsPageView.as_view(), name='News_page'),
    path('AddArticle', AddArticleView.as_view(), name='AddArticle'),
    path('portfolio', PortfolioView.as_view(), name='PortfolioView'),
    path('<int:id>/', AddToFavoriteView.as_view(), name='AddTOFavorite'),

    path('About_Us/', AboutUsView.as_view(), name='About_Us'),
    path('Branding_Guide/', BrandingGuideView.as_view(), name='Branding_Guide'),
    path('Regulations/', RegulationsView.as_view(), name='Regulations'),
    path('GetCandy/', GetCandyView.as_view(), name='GetCandy'),
    path('BuyCoin/<int:id>/', BuyCoinView.as_view(), name='BuyCoin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATICFILES_DIRS)
