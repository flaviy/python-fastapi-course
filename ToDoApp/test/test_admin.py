from .utils import *
from ..routers.admin import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def read_all_todos_authenticated():
    response = client.get('/admin/read_all')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'title': 'test', 'description': 'test', 'complete': False, 'priority': 1, 'owner_id': 1, 'id': 1}]


def test_admin_delete_todo(test_todo):
    response = client.delete('/admin/delete/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get('/admin/read_all')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    # alternatively
    db = TestingSessionLocal()
    model = db.query(ToDoModel).filter(ToDoModel.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(test_todo):
    response = client.delete('/admin/delete/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}
