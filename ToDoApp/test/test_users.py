from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'test'
    assert response.json()['email'] == 'test@ukr.net'
    assert response.json()['first_name'] == 'test'
    assert response.json()['last_name'] == 'test'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '123456789'
    #assert response.json()['hashed_password'] == context.hash('test')


def test_change_password_invalid_new_password(test_user):
    response = client.post('/user/change_password', json={'password': 'test', 'new_password': 'short'})
    assert response.status_code == 422


def test_change_password_success(test_user):
    response = client.post('/user/change_password', json={'password': 'test', 'new_password': 'VaaaalidPass123'})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.json() == {"message": "Password updated successfully"}

def test_change_password_invalid_current_password(test_user):
    response = client.post('/user/change_password', json={'password': 'testss', 'new_password': 'VaaaalidPass123'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_change_phone_number_success(test_user):
    response = client.put('/user/change_phone_number/2232323223')
    assert response.status_code == status.HTTP_204_NO_CONTENT

