from fastapi import FastAPI, APIRouter

from .models import Base
from .routers import auth, todo, admin, users
from .database import engine

app = FastAPI()

router = APIRouter()
router.include_router(auth.router, tags=["auth"], prefix="/auth")
router.include_router(admin.router, tags=["admin"], prefix="/admin")
router.include_router(users.router, tags=["user"])
app.include_router(router)
app.include_router(todo.router, tags=["todo"])

# here we create the tables in the database
Base.metadata.create_all(bind=engine)


@app.get("/healthy", status_code=200)
def healthy():
    return {"status": "healthy"}
