from django.contrib.auth.models import User
from django.urls import reverse
from django import urls
import pytest


@pytest.mark.parametrize('param', [
    ('IndexPage'),
    ('Login'),
    ('Logout'),
    ('Forgot_Pass'),
    ('Sing_up'),
    ('Contact'),
    ('NewsList'),
    ('AddArticle'),
    ('PortfolioView'),
    ('About_Us'),
    ('Branding_Guide'),
    ('Regulations')

])
@pytest.mark.django_db
def test_check_index(client, param):
    url = urls.reverse(param)
    resp = client.get(url)
    assert resp.status_code == 200 or 302


@pytest.mark.django_db
def test_user_signup(client, user_data, user):
    user_model = User
    assert user_model.objects.count() == 0
    signup_url = urls.reverse('Sing_up')
    resp = client.post(signup_url, user_data)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_add_article(client, article):
    assert addarticle.objects.count() == 0


@pytest.mark.django_db
def test_user_logout(client):
    logout_url = urls.reverse('Logout')
    resp = client.get(logout_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse('NewsList')
