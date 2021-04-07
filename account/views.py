from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from account.forms import LoginForm, ForgotPassword, RegisterForm
from account.models import Profile
from home.models import CryptoCoins3, Portfolio, Transaction
import re
from django.core.mail import send_mail
from django.conf import settings


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
                redirect_url = request.GET.get('next', 'IndexPage')
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
                    p = Profile.objects.create(user=u)
                    p.save()
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

                    return render(request, 'Sing_Up.html',
                                  {'form': form, 'error_mail': error_mail, 'error_user': error_username})
        else:
            return render(request, 'Sing_Up.html', {'form': form})


class Contact(View):

    def get(self, request):
        return render(request, "contact.html")

    def post(self, request):
        name = request.POST['txtName']
        email = request.POST['txtEmail']
        phonenumber = request.POST['txtPhone']
        msg = request.POST['txtMsg']
        subject = name
        message = f"{msg} + {email} + {phonenumber}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['whale.crew.help@gmail.com', ]
        send_mail(subject, message, email_from, recipient_list)

        return render(request, "contact.html")


def validateEmail(email):
    if len(email) > 6:
        if re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', email) != None:
            return 1
    return 0


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('IndexPage')


class PortfolioView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('Login')

        portfolios = Portfolio.objects.filter(owner=request.user)


        paginator = Paginator(portfolios, 30)
        page = request.GET.get('page')
        obj = paginator.get_page(page)
        context = {'paginator': obj}
        return render(request, 'portfolio.html', context)


class BuyCoin(View):

    def get(self, request,id):
        user = request.user
        coin = CryptoCoins3.objects.get(id=id)
        print(id)
        t = Transaction.objects.create(profile=user.profile, coin=coin, quantity=1.0, price=10.0)
        t.save()

        if coin.favourite.filter(id=user.id).exists():
            coin.favourite.remove(user)
        else:
            coin.favourite.add(user)
        return redirect('PortfolioView')
