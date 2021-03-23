from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from account.forms import LoginForm, ForgotPassword


class LoginView(View):

    def get(self, request):
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form})


class ForgotPass(View):

    def get(self, request):
        form = ForgotPassword(request.POST)
        return render(request, 'ForgotPassword.html', {'form': form})
