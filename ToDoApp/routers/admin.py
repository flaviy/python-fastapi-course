from fastapi import Depends, HTTPException, Path, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from .. import models
from ..models import ToDoModel
from ..database import engine
from typing import Annotated
from ..db_session import get_db
# the dot This ensures that the get_current_user function is correctly imported from the
# auth module located in the same directory.
# If you don't add the dot in the import statement,
# it will be interpreted as an absolute import rather than a relative import.
# This means Python will look for the auth module in the top-level package of your project rather
# than in the same directory as the current module.
from .auth import get_current_user

router = APIRouter()
# here we create the tables in the database
models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/read_all",  status_code=status.HTTP_200_OK)
def read_all_todos(db: db_dependency, user: user_dependency):
    if user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')
    todos = db.query(ToDoModel).all()
    return todos


@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')
    todo = db.query(ToDoModel).filter(ToDoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    db.delete(todo)
    db.commit()
    return
