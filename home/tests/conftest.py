import pytest
from django.contrib.auth.models import User, Permission

from home.models import NewsArticle


@pytest.fixture
def user_data():
    return {'email': 'emailtest@emailtest.pl', 'name': 'user_name', 'password1': 'user_password',
            'password2': 'user_password'}


@pytest.fixture
def create_test_user(user_data):
    test_user = User.objects.create_user(username="test", password="password", email="email@email.pl")
    return test_user


@pytest.fixture
def authenticated_user(client, user_data):
    user_model = User()
    test_user = user_model.objects.create_user(**user_data)
    client.login(**user_data)
    return test_user


@pytest.fixture
def users():
    users = []
    for x in range(1, 11):
        u = User.objects.create(username=str(x), email=f"email{str(x)}@email.com", password=f"pass{str(x)}")
        users.append(u)
    return users


@pytest.fixture
def article_data():
    return {'title': 'title', 'short_desc': 'desc', 'desc': 'long_desc',
            'photo_file': ''}


@pytest.fixture
def user_with_permissions():
    u = User.objects.create(username='aabb')
    p = Permission.objects.get(codename='home.add_article')
    u.user_permissions.add(p)
    return u


@pytest.fixture
def articele():
    article = []
    for x in range(1, 11):
        u = NewsArticle.objects.create(name=str(x))
        article.append(u)
    return article
