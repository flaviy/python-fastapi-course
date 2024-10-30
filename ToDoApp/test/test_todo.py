from fastapi import status

from ..db_session import get_db
from ..routers.auth import get_current_user
from .utils import *
from ..models import ToDoModel

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_all_authenticated(test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'title': 'test', 'description': 'test', 'complete': False, 'priority': 1, 'owner_id': 1, 'id': 1}]
