from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..main import app
from ..database import Base
from fastapi.testclient import TestClient
import pytest
from ..models import ToDoModel, Users
from ..routers.auth import context

SQLALCHEMY_DATABASE_URI = 'sqlite:///./todosapptest.db'
'''
The `StaticPool` class in SQLAlchemy is a connection pool that maintains a single connection to the database.
 which is particularly useful for SQLite databases in a testing environment where you want to avoid the overhead 
 of creating and closing connections repeatedly.

'''
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    # this function will return the session that we will use to interact with the database
    db = TestingSessionLocal()
    try:
        # we yield the session to the route that needs it, we use generator
        # instead of return to avoid closing the session each time we use it
        # this way we can use the session multiple times
        # finally will always run after the route is done
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'username', 'user_id': 1, 'role': 'admin'}


@pytest.fixture
def test_todo():
    todo = ToDoModel(
        title='test',
        description='test',
        complete=False,
        priority=1,
        owner_id=1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    db.query(ToDoModel).delete()
    db.commit()
    db.close()


@pytest.fixture
def test_user():
    user = Users(
        id=1,
        username='test',
        email='test@ukr.net',
        hashed_password=context.hash('test'),
        first_name='test',
        last_name='test',
        role='admin',
        phone_number='123456789'
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    db.query(Users).delete()
    db.commit()
    db.close()


client = TestClient(app)
