from django.contrib.auth.tokens import default_token_generator
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import re
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from coins_app.models import Transaction, CoinsInfo
from user_account_app.forms import LoginForm, ForgotPassword, RegisterForm, ResetPassword
from user_account_app.models import Profile, Portfolio, PasswordRstToken


class SingUp(View):
    """
    Class View to Sing Up new User.
    """

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
                user = list(User.objects.filter(username=username))
                mail = list(User.objects.filter(email=email))
                if user == [] and mail == []:
                    password = form.cleaned_data['password1']
                    u = User.objects.create(username=username, email=email)
                    u.set_password(password)
                    u.save()
                    p = Profile.objects.create(user=u)
                    p.save()
                    return render(request, 'welcome.html', {'user': username})
                else:
                    if not mail:
                        error_mail = 1
                    else:
                        error_mail = 0
                    if not user:
                        error_username = 1
                    else:
                        error_username = 0
                    return render(request, 'Sing_Up.html',
                                  {'form': form, 'error_mail': error_mail, 'error_user': error_username})
        else:
            return render(request, 'Sing_Up.html', {'form': form})


class ForgotPass(View):
    """
    Class view to remind password for Users
    """

    def get(self, request):
        form = ForgotPassword()
        return render(request, 'ForgotPassword.html', {'form': form})

    def post(self, request):
        form = ForgotPassword(request.POST)
        domain = request.headers['Host']
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return redirect('Forgot_Pass')

            token = default_token_generator.make_token(user)
            PasswordRstToken.objects.filter(user=user).delete()
            PasswordRstToken.objects.create(token=token, user=user)
            link = f"http://{domain}/reset/{token}"
            context = {
                "link": link
            }
            html_message = render_to_string("reset_password.html", context)
            message = f"Hi, please reset your password with this link: {link}"
            try:
                send_mail("Password Reset Requested", message, settings.EMAIL_HOST_USER, [user.email],
                          fail_silently=False, html_message=html_message)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        return redirect('Forgot_Pass')  # TODO Reset


def resetPasswordView(request, token):
    """
    View to reset Password for User from unique mail url information.
    """
    if request.method == 'GET':
        try:
            password_rst_token = PasswordRstToken.objects.get(token=token)
        except PasswordRstToken.DoesNotExist:
            return redirect('IndexPage')
        form = ResetPassword(initial={"email": password_rst_token.user.email})
        return render(request, 'rst_password.html', {'form': form})
    else:

        form = ResetPassword(request.POST)
        try:
            password_rst_token = PasswordRstToken.objects.get(token=token)
        except PasswordRstToken.DoesNotExist:
            return redirect('IndexPage')
        if form.is_valid():
            password = form.cleaned_data['password1']
            password_rst_token.user.set_password(password)
            password_rst_token.user.save()
        return redirect('Login')


class LoginView(View):
    """
    Base class view to Log in the User
    """

    def get(self, request):
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


class LogoutView(View):
    """
    Base class View to log
    """

    def get(self, request):
        logout(request)
        return redirect('NewsList')


class Contact(View):
    """
    Base class view to contact form.
    """

    def get(self, request):
        return render(request, "contact.html")

    def post(self, request):
        name = request.POST['txtName']
        email = request.POST['txtEmail']
        phone_number = request.POST['txtPhone']
        msg = request.POST['txtMsg']
        subject = name
        message = f"{msg} + {email} + {phone_number}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['whale.crew.help@gmail.com', ]
        send_mail(subject, message, email_from, recipient_list)

        return render(request, "contact.html")


class PortfolioView(View):
    """
    Base class view for authenticated User. View show the favourite's User coins , balance and allowed to do the Transaction.
    """

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('Login')
        portfolios = Portfolio.objects.filter(owner=request.user)
        paginator = Paginator(portfolios, 30)
        page = request.GET.get('page')
        obj = paginator.get_page(page)
        context = {'paginator': obj}
        return render(request, 'portfolio.html', context)

    def post(self, request):

        user = request.user
        buy_price = (request.POST['price_act']).replace(",", ".")
        quantity = (request.POST['amount']).replace(",", ".")
        coin_id = request.POST['id_coin']

        """If User try to sell more than has got, the Balance will be 0"""

        actual_coin_quantity = Portfolio.objects.get(owner=request.user, coin=coin_id).quantity
        print(actual_coin_quantity - float(quantity))
        if actual_coin_quantity + float(quantity) <= 0:
            quantity = - actual_coin_quantity

        coin = CoinsInfo.objects.get(id=coin_id)
        t = Transaction.objects.create(profile=user.profile, coin=coin, quantity=quantity, price=buy_price)
        t.save()
        return redirect('PortfolioView')


def validateEmail(email):
    """
    Function to validate email.
    """
    if len(email) > 6:
        if re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', email) is not None:
            return 1
    return 0
