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
from django.urls import path
from account.views import LoginView, ForgotPass, SingUp, Contact, LogoutView
from home.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='IndexPage'),
    path('login/', LoginView.as_view(), name='Login'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('Forgot_Pass/', ForgotPass.as_view(), name='Forgot_Pass'),
    path('Sing_up/', SingUp.as_view(), name='Sing_up'),
    path('Contact/', Contact.as_view(), name='Contact'),
]
