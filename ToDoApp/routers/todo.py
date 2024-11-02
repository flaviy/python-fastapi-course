import sys

from fastapi import Depends, HTTPException, Path, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse

from .. import models
from ..models import ToDoModel
from ..database import engine
from typing import Annotated
from ..requests.todo_request import TodoRequest
from ..db_session import get_db
from fastapi.templating import Jinja2Templates

# the dot This ensures that the get_current_user function is correctly imported from the
# auth module located in the same directory.
# If you don't add the dot in the import statement,
# it will be interpreted as an absolute import rather than a relative import.
# This means Python will look for the auth module in the top-level package of your project rather
# than in the same directory as the current module.
from .auth import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)
# here we create the tables in the database
models.Base.metadata.create_all(bind=engine)

'''
The `Annotated` type in Python is used to add metadata to type hints. This metadata can be used by frameworks and 
libraries to provide additional functionality or validation. In the context of FastAPI, `Annotated` is often used to 
combine type hints with dependency injection.

Here's a breakdown of how `Annotated` works:

1. **Basic Structure**:
   ```python
   from typing import Annotated
   ```

2. **Combining Type Hints with Metadata**:
   ```python
   from fastapi import Depends
   from sqlalchemy.orm import Session

   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()

   db: Annotated[Session, Depends(get_db)]

Using yield db in the get_db function is a way to create a generator 
that provides a database session to the caller and ensures that the session is properly closed 
after use. Here are the main reasons:  
Resource Management: By using yield, the function can provide the database session to the c
aller and then ensure that the session is closed after the caller is done with it. This is done in the finally block, 
which guarantees that db.close() is called, releasing the database connection back to the pool.  
Dependency Injection: In FastAPI, dependencies can be provided using functions that yield values. 
This allows FastAPI to manage the lifecycle of the dependency, ensuring that resources are properly cleaned up. When a 
route depends on get_db, FastAPI will call get_db, get the yielded db session, and then close the session after the route 
handler completes.  
Concurrency: Using yield allows the function to be used in an asynchronous context, which is important 
for handling multiple requests concurrently in FastAPI.  
In summary, yield db is used to provide a database session to the caller and ensure that it is properly
 closed after use, leveraging FastAPI's dependency injection system and resource management capabilities.
   ```

3. **Explanation**:
   - `Annotated[Session, Depends(get_db)]`:
     - `Session`: The main type hint, indicating that `db` is a SQLAlchemy `Session`.
     - `Depends(get_db)`: Metadata indicating that FastAPI should use the `get_db` function to provide the `Session` instance.

This allows FastAPI to manage dependencies and inject the required objects into route handlers.
'''

db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency: dict = Depends(get_current_user)
user_dependency = Annotated[dict, Depends(get_current_user)]
templates = Jinja2Templates(directory="ToDoApp/templates")


### pages ###
@router.get("/render-todo-page", response_class=HTMLResponse)
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_non_logged(request)
    except Exception as e:
        return redirect_non_logged(request)
    all_user_todos = db.query(ToDoModel).filter(ToDoModel.owner_id == user.get("user_id")).all()
    return templates.TemplateResponse("todos.html", {"request": request, "todos": all_user_todos, "user": user})

@router.get("/add-todo-page", response_class=HTMLResponse)
async  def add_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_non_logged(request)
    except Exception as e:
        return redirect_non_logged(request)
    return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})

@router.get("/edit-todo-page/{todo_id}", response_class=HTMLResponse)
async def edit_todo_page(request: Request, db: db_dependency, todo_id: int = Path(gt=0)):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_non_logged(request)
    except Exception as e:
        return redirect_non_logged(request)
    todo = db.query(ToDoModel).filter(ToDoModel.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return templates.TemplateResponse("edit-todo.html", {"request": request, "user": user, "todo": todo})


def redirect_non_logged(request):
   # request.session['flash'] = 'You need to log in to access this page.'
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=302)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### endpoints ###

@router.get("/")
# async def read_all(db: Annotated[Session, Depends(get_db)]):
async def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(ToDoModel).filter(ToDoModel.owner_id == user.get("user_id")).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo_model = db.query(ToDoModel).filter(ToDoModel.id == todo_id) \
        .filter(ToDoModel.owner_id == user.get("user_id")) \
        .first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest, db: db_dependency,
                      user: user_dependency
                      ):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo = ToDoModel(**todo_request.model_dump(), owner_id=user.get("user_id"))
    db.add(todo)
    db.commit()
    return {"message": "Todo created successfully", "status": 201}


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo = db.query(ToDoModel).filter(ToDoModel.id == todo_id) \
        .filter(ToDoModel.owner_id == user.get("user_id")).first()
    if todo is not None:
        todo.title = todo_request.title
        todo.description = todo_request.description
        todo.priority = todo_request.priority
        todo.complete = todo_request.complete
        db.add(todo)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo = db.query(ToDoModel).filter(ToDoModel.id == todo_id) \
        .filter(ToDoModel.owner_id == user.get("user_id")).first()
    if todo is not None:
        db.delete(todo)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
