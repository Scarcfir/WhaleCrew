import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user_data():
    return {'email': 'emailtest@emailtest.pl', 'name': 'user_name', 'password1': 'user_password', 'password2': 'user_password'}


@pytest.fixture
def create_test_user(user_data):
    user_model = User()
    test_user = user_model.objects.create_user(**user_data)
    return test_user


@pytest.fixture
def authenticated_user(client, user_data):
    user_model = User()
    test_user = user_model.objects.create_user(**user_data)
    client.login(**user_data)
    return test_user
