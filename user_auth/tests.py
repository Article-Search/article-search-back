import pytest
from django.urls import reverse
import json
from .serializer import UserSerializer
from rest_framework.authtoken.models import Token

@pytest.fixture
def valid_registered_user():
    user_data = {'email': 'hello@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 3}
    user_serializer = UserSerializer(data=user_data)
    
    user_serializer.is_valid()
    user = user_serializer.save()
    Token.objects.create(user=user)

    return {'email': user_serializer.data['email'], 'password': 'hello'} 

@pytest.fixture
def valid_registered_authenticated_user():
    user_data = {'email': 'hello@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 3}
    user_serializer = UserSerializer(data=user_data)
    
    user_serializer.is_valid()
    user = user_serializer.save()
    token = Token.objects.create(user=user)

    return {'token': token.key, 'user': user_serializer.data}

@pytest.fixture
def valid_registered_authenticated_admin():
    user_data = {'email': 'hello@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 1}
    user_serializer = UserSerializer(data=user_data)
    
    user_serializer.is_valid()
    user = user_serializer.save()
    token = Token.objects.create(user=user)

    return {'token': token.key, 'user': user_serializer.data}

@pytest.fixture
def valid_registered_authenticated_moderator():
    user_data = {'email': 'hello@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 2}
    user_serializer = UserSerializer(data=user_data)
    
    user_serializer.is_valid()
    user = user_serializer.save()
    token = Token.objects.create(user=user)

    return {'token': token.key, 'user': user_serializer.data}

@pytest.fixture
def valid_non_registered_user():
    user_data = {'email': 'hello@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 3}

    return user_data

# @pytest.mark.skip
@pytest.mark.django_db
def test_user_register(client, valid_non_registered_user):
    endpoint = reverse('register')

    response = client.post(endpoint, valid_non_registered_user)
    body = json.loads(response.content)

    _ , created_user = body.values()

    assert response.status_code == 201

    # assert the user info
    assert 'token' in body
    assert created_user['email'] == valid_non_registered_user['email']
    assert 'password' not in created_user # the response should not include the password
    assert created_user['first_name'] == valid_non_registered_user['first_name']
    assert created_user['last_name'] == valid_non_registered_user['last_name']
    assert created_user['role'] == 3
    
@pytest.mark.django_db
def test_user_register_duplication(client, valid_non_registered_user):
    endpoint = reverse('register')

    response = client.post(endpoint, valid_non_registered_user)
    assert response.status_code == 201

    response = client.post(endpoint, valid_non_registered_user)
    assert response.status_code == 400
    
@pytest.mark.django_db
def test_uesr_login(client, valid_registered_user):
    login_endpoint = reverse('login')

    response = client.post(login_endpoint, valid_registered_user)
    print(response.status_code)
    body = json.loads(response.content)

    _ , registered_user = body.values()

    assert response.status_code == 200
    
    assert 'token' in body
    assert registered_user['email'] == valid_registered_user['email']
    assert 'password' not in registered_user # the response should not include the password
    assert 'first_name' in registered_user
    assert 'last_name' in registered_user
    assert 'role' in registered_user
    
@pytest.mark.skip
@pytest.mark.django_db
def test_logout(client, valid_registered_authenticated_user):
    logout_endpoint = reverse('logout')

    response = client.post(logout_endpoint, HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_user['token']}")

    assert response.status_code == 200

@pytest.mark.django_db
def test_password_reset(client, valid_registered_authenticated_user):
    password_reset_endpoint = reverse('reset_password')
    login_endpoint = reverse('login')

    data = {'email': valid_registered_authenticated_user['user']['email'], 'password': 'this is a new password'}
    response = client.post(password_reset_endpoint, HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_user['token']}", data=data)
    assert response.status_code == 200

    response = client.post(login_endpoint , HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_user['token']}", data=data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_permissions(client, valid_registered_authenticated_user):
    user_endpoint = reverse('test_user')
    admin_endpoint = reverse('test_admin')
    moderator_endpoint = reverse('test_moderator')

    response = client.get(user_endpoint, HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_user['token']}")
    assert response.status_code == 200

    response = client.get(admin_endpoint, HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_user['token']}")
    assert response.status_code == 403

    response = client.get(moderator_endpoint, HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_user['token']}")
    assert response.status_code == 403

@pytest.mark.django_db
def test_admin_permissions(client, valid_registered_authenticated_admin):
    user_endpoint = reverse('test_user')
    admin_endpoint = reverse('test_admin')
    moderator_endpoint = reverse('test_moderator')

    response = client.get(admin_endpoint, HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_admin['token']}")
    assert response.status_code == 200

    response = client.get(user_endpoint, HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_admin['token']}")
    assert response.status_code == 403

    response = client.get(moderator_endpoint, HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_admin['token']}")
    assert response.status_code == 403

@pytest.mark.django_db
def test_moderator_permissions(client, valid_registered_authenticated_moderator):
    user_endpoint = reverse('test_user')
    admin_endpoint = reverse('test_admin')
    moderator_endpoint = reverse('test_moderator')

    response = client.get(moderator_endpoint, HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_moderator['token']}")
    assert response.status_code == 200

    response = client.get(user_endpoint, HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_moderator['token']}")
    assert response.status_code == 403

    response = client.get(admin_endpoint, HTTP_AUTHORIZATION=f"Token {valid_registered_authenticated_moderator['token']}")
    assert response.status_code == 403
