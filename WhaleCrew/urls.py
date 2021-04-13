from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from coins_app.views import *
from user_account_app.views import *
from home.views import IndexView, NewsListView, NewsPageView, AddArticleView
from footer_app.views import *




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='IndexPage'),
    path('login/', LoginView.as_view(), name='Login'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('forgot_pass/', ForgotPass.as_view(), name='Forgot_Pass'),
    path('sing_up/', SingUp.as_view(), name='Sing_up'),
    path('contact/', Contact.as_view(), name='Contact'),
    path('news_list/', NewsListView.as_view(), name='NewsList'),
    path('news/<int:id>/', NewsPageView.as_view(), name='News_page'),
    path('add_article', AddArticleView.as_view(), name='AddArticle'),
    path('portfolio', PortfolioView.as_view(), name='PortfolioView'),
    path('<int:id>/', AddToFavoriteView.as_view(), name='AddTOFavorite'),
    path('reset/<slug:token>/', resetPasswordView, name='ResetPassword'),

    path('about_Us/', AboutUsView.as_view(), name='About_Us'),
    path('branding_guide/', BrandingGuideView.as_view(), name='Branding_Guide'),
    path('regulations/', RegulationsView.as_view(), name='Regulations'),
    path('get_candy/', GetCandyView.as_view(), name='GetCandy'),

    path('user_profile/', UserProfile.as_view(), name='UserProfile'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATICFILES_DIRS)
