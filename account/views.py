from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from account.forms import LoginForm, ForgotPassword, RegisterForm
import re


class LoginView(View):

    def get(self, request):
        tekst = 0
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                redirect_url = request.GET.get('next', 'index')
                return redirect(redirect_url)
            else:
                tekst = 1
                return render(request, 'login.html', {'tekst': tekst, 'form': form})


class ForgotPass(View):

    def get(self, request):
        form = ForgotPassword()
        return render(request, 'ForgotPassword.html', {'form': form})


class SingUp(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'Sing_Up.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if validateEmail(email) == 0:
                mail_error = 1
                return render(request, 'Sing_Up.html',
                              {'form': form, 'mail_error': mail_error})
            else:
                uzytkownik = list(User.objects.filter(username=username))
                mail = list(User.objects.filter(email=email))
                if uzytkownik == [] and mail == []:
                    password = form.cleaned_data['password1']
                    u = User.objects.create(username=username, email=email)
                    u.set_password(password)
                    u.save()
                    return render(request, 'welcome.html', {'user': username})
                else:
                    if mail == []:
                        error_mail = 1
                    else:
                        error_mail = 0
                    if uzytkownik == []:
                        error_username = 1
                    else:
                        error_username = 0

                    print(error_mail)
                    print(error_username)
                    return render(request, 'Sing_Up.html',
                                  {'form': form, 'error_mail': error_mail, 'error_user': error_username})
        else:
            return render(request, 'Sing_Up.html', {'form': form})


class Contact(View):
    pass


def validateEmail(email):
    if len(email) > 6:
        if re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', email) != None:
            return 1
    return 0
