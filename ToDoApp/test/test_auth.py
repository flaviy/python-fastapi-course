from fastapi import HTTPException

from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from jose import jwt
from datetime import timedelta, datetime, timezone

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(db, test_user.username, 'test')
    assert authenticated_user is not False
    assert authenticated_user.username == test_user.username

def test_authenticate_user_incorrect_user_name(test_user):
    db = TestingSessionLocal()
    incorrect_name_user = authenticate_user(db, 'incorrect', 'test')
    assert incorrect_name_user is False

    wrong_password_user = authenticate_user(db, test_user.username, 'wrong')
    assert wrong_password_user is False

def test_create_access_token():
    username = 'test'
    user_id = 1
    role = 'admin'
    expires_delta = timedelta(days=1)
    token = create_access_token(username, user_id, role, expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user():
    encode = {'sub': 'username', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token)
    assert user['username'] == 'username'
    assert user['user_id'] == 1
    assert user['role'] == 'admin'

@pytest.mark.asyncio
async def test_get_current_user_missing_payload(test_user):
    encode = { 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Invalid authentication credentials'

