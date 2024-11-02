from fastapi import FastAPI, APIRouter, Request, status
from starlette.responses import HTMLResponse, RedirectResponse

from .models import Base
from .routers import auth, todo, admin, users
from .database import engine
from fastapi.staticfiles import StaticFiles

app = FastAPI()

router = APIRouter()
router.include_router(auth.router, tags=["auth"], prefix="/auth")
router.include_router(admin.router, tags=["admin"], prefix="/admin")
router.include_router(users.router, tags=["user"])
app.include_router(router)
app.include_router(todo.router, tags=["todo"])

# here we create the tables in the database
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")


@app.get("/healthy", status_code=200)
def healthy():
    return {"status": "healthy"}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return RedirectResponse(url="/todos/render-todo-page", status_code=status.HTTP_302_FOUND)
