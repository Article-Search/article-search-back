import pytest
from django.urls import reverse
import json
from user_auth.models import User
from user_auth.serializer import UserSerializer
from rest_framework.authtoken.models import Token

# =============================================== SETUP ======================================================
@pytest.fixture
def admin_token():
    user_data = {'email': 'hello-admin@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 1}
    user_serializer = UserSerializer(data=user_data)
    
    user_serializer.is_valid()
    user = user_serializer.save()
    token = Token.objects.create(user=user)

    return token.key

@pytest.fixture
def user_token():
    user_data = {'email': 'hello-user@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 3}
    user_serializer = UserSerializer(data=user_data)
    
    user_serializer.is_valid()
    user = user_serializer.save()
    token = Token.objects.create(user=user)

    return token.key

@pytest.fixture
def moderator_token():
    user_data = {'email': 'hello-moderator@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 2}
    user_serializer = UserSerializer(data=user_data)
    
    user_serializer.is_valid()
    user = user_serializer.save()
    token = Token.objects.create(user=user)

    return token.key

@pytest.fixture
def valid_non_registered_moderator():
    user_data = {'username':'hello', 'email': 'hello-mod1@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 2}

    return user_data

@pytest.fixture
def non_registered_moderator_updated_data():
    user_data = {"email": "hello-moderator1@world.com", "password": "hello", "first_name": "moderator", "last_name": "world", "role": 2}

    return user_data

@pytest.fixture
def moderator_updated_data():
    user_data = {'email': 'hello@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 2}

    return user_data

@pytest.fixture
def registered_moderator():
    user_data = {'email': 'hello@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 2}
    user_serializer = UserSerializer(data=user_data)
    
    user_serializer.is_valid()
    user = user_serializer.save()
    Token.objects.create(user=user)

    user_data = user_serializer.data
    user_data['id'] = user.id

    return user_data

@pytest.fixture
def registered_moderators_list():
    users_data = [
        {'email': 'hello-mod@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 2},
        {'email': 'hello-mod2@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 2},
        {'email': 'hello-mod3@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 2}
    ]
    data = []

    for user_data in users_data:
        user_serializer = UserSerializer(data=user_data)
        
        user_serializer.is_valid()
        user = user_serializer.save()
        Token.objects.create(user=user)
        data.append(user_serializer.data)

    return {'users': data}

@pytest.fixture
def authenticated_admin():
    admin_data = {'email': 'hello@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 1}
    user_serializer = UserSerializer(data=admin_data)
    
    user_serializer.is_valid()
    admin = user_serializer.save()
    token = Token.objects.create(user=admin)

    return {'token': token.key, 'user': user_serializer.data}

@pytest.fixture
def authenticated_moderator():
    user_data = {'email': 'hello@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 2}
    user_serializer = UserSerializer(data=user_data)
    
    user_serializer.is_valid()
    user = user_serializer.save()
    token = Token.objects.create(user=user)

    return {'token': token.key, 'user': user_serializer.data}

@pytest.fixture
def authenticated_user():
    user_data = {'email': 'hello@world.com', 'password': 'hello', 'first_name': 'hello', 'last_name': 'world', 'role': 3}
    user_serializer = UserSerializer(data=user_data)
    
    user_serializer.is_valid()
    user = user_serializer.save()
    token = Token.objects.create(user=user)

    return {'token': token.key, 'user': user_serializer.data}

# =============================================== TESTS ======================================================
# 1. Testing CRUD operations

@pytest.mark.django_db
def test_mod_create(client, admin_token, valid_non_registered_moderator):
    endpoint = reverse('create_list_mods')

    response = client.post(endpoint, data=valid_non_registered_moderator, HTTP_AUTHORIZATION=f"Token {admin_token}")
    body = json.loads(response.content)

    created_user = body['user']

    assert response.status_code == 201

    # assert the user info
    assert created_user['email'] == valid_non_registered_moderator['email']
    assert 'password' not in created_user # the response should not include the password
    assert created_user['first_name'] == valid_non_registered_moderator['first_name']
    assert created_user['last_name'] == valid_non_registered_moderator['last_name']
    assert created_user['role'] == 2

@pytest.mark.django_db
def test_mod_creation_duplication(client, admin_token, valid_non_registered_moderator):
    endpoint = reverse('create_list_mods')

    response = client.post(endpoint, valid_non_registered_moderator, HTTP_AUTHORIZATION=f"Token {admin_token}")
    assert response.status_code == 201


    response = client.post(endpoint, valid_non_registered_moderator, HTTP_AUTHORIZATION=f"Token {admin_token}")
    assert response.status_code == 400

@pytest.mark.django_db
def test_mods_list(client, admin_token, registered_moderators_list):
    endpoint = reverse('create_list_mods')

    response = client.get(endpoint, HTTP_AUTHORIZATION=f"Token {admin_token}")
    body = json.loads(response.content)

    moderators_list = body['users']

    assert response.status_code == 200

    # assert the body content validity
    assert len(moderators_list) == 3

@pytest.mark.django_db
def test_get_moderator(client, admin_token, registered_moderator):
    endpoint = f"/moderators//{registered_moderator['id']}" # check why this doesn't work
    # endpoint = reverse("pick_update_delete_mod", kwargs={'id': registered_moderator['id']})

    response = client.get(endpoint, HTTP_AUTHORIZATION=f"Token {admin_token}")
    body = json.loads(response.content)

    moderator = body['user']

    assert response.status_code == 200

    # assert body content validity
    assert moderator['email'] == registered_moderator['email']
    assert 'password' not in moderator # the response should not include the password
    assert moderator['first_name'] == registered_moderator['first_name']
    assert moderator['last_name'] == registered_moderator['last_name']
    assert moderator['role'] == 2

@pytest.mark.django_db
def test_update_moderator(client, admin_token, registered_moderator, moderator_updated_data):
    endpoint = reverse('pick_update_delete_mod', kwargs={'id': registered_moderator['id']})
    print(moderator_updated_data)

    # response = client.put(endpoint, data={"user": moderator_updated_data}, headers={"CONTENT_TYPE": "application/json"}, HTTP_AUTHORIZATION=f"Token {admin_token}") # see how to supply a query param
    response = client.put(endpoint, json.dumps(moderator_updated_data), headers={"CONTENT_TYPE": "application/json"}, HTTP_AUTHORIZATION=f"Token {admin_token}") # see how to supply a query param

    body = json.loads(response.content)
    print(f"response body: {body}")

    updated_moderator = body['user']

    assert response.status_code == 200

    #assert body content validity
    assert updated_moderator['email'] == moderator_updated_data['email']
    assert 'password' not in updated_moderator # the response should not include the password
    assert updated_moderator['first_name'] == moderator_updated_data['first_name']
    assert updated_moderator['last_name'] == moderator_updated_data['last_name']
    assert updated_moderator['role'] == 2

@pytest.mark.django_db
def test_delete_moderator(client, admin_token, registered_moderator):
    endpoint = reverse('pick_update_delete_mod', kwargs={'id': registered_moderator['id']})

    response = client.delete(endpoint, HTTP_AUTHORIZATION=f"Token {admin_token}")

    assert response.status_code == 204

# 2. Testing permissions
@pytest.mark.django_db
def test_permissions(client, user_token, moderator_token, registered_moderator): # no access is valid without an admin token
    create_list_endpoint = reverse('create_list_mods')
    pick_update_delete_endpoint = reverse('pick_update_delete_mod', kwargs={'id': registered_moderator['id']})

    # no token
    response = client.get(create_list_endpoint)
    assert response.status_code == 403

    response = client.post(create_list_endpoint)
    assert response.status_code == 403

    response = client.get(pick_update_delete_endpoint)
    assert response.status_code == 403

    response = client.put(pick_update_delete_endpoint)
    assert response.status_code == 403

    response = client.delete(pick_update_delete_endpoint)
    assert response.status_code == 403

    # invalid normal user token
    response = client.get(create_list_endpoint, HTTP_AUTHORIZATION=f"Token {user_token}")
    assert response.status_code == 403

    response = client.post(create_list_endpoint, HTTP_AUTHORIZATION=f"Token {user_token}")
    assert response.status_code == 403

    response = client.get(pick_update_delete_endpoint, HTTP_AUTHORIZATION=f"Token {user_token}")
    assert response.status_code == 403

    response = client.put(pick_update_delete_endpoint, HTTP_AUTHORIZATION=f"Token {user_token}")
    assert response.status_code == 403

    response = client.delete(pick_update_delete_endpoint, HTTP_AUTHORIZATION=f"Token {user_token}")
    assert response.status_code == 403

    # invalid moderator token
    response = client.get(create_list_endpoint, HTTP_AUTHORIZATION=f"Token {moderator_token}")
    assert response.status_code == 403

    response = client.post(create_list_endpoint, HTTP_AUTHORIZATION=f"Token {moderator_token}")
    assert response.status_code == 403

    response = client.get(pick_update_delete_endpoint, HTTP_AUTHORIZATION=f"Token {moderator_token}")
    assert response.status_code == 403

    response = client.put(pick_update_delete_endpoint, HTTP_AUTHORIZATION=f"Token {moderator_token}")
    assert response.status_code == 403

    response = client.delete(pick_update_delete_endpoint, HTTP_AUTHORIZATION=f"Token {moderator_token}")
    assert response.status_code == 403
