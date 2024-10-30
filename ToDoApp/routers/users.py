from fastapi import Depends, HTTPException, APIRouter, Path, Query
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from .. import models
from ..models import Users
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
from ..requests.change_password_request import UserVerification

#prefix and path could be included here or in the main.py file
router = APIRouter(prefix="/user", tags=["user"])
# here we create the tables in the database
models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", status_code=status.HTTP_200_OK)
# async def read_all(db: Annotated[Session, Depends(get_db)]):
async def get_user(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(Users).filter(Users.id == user.get("user_id")).first()


@router.post("/change_password")
async def change_password(db: db_dependency, user: user_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")


    user = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if not context.verify(user_verification.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')

    user.hashed_password = context.hash(user_verification.new_password)

    db.add(user)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Password updated successfully"})


@router.put("/change_phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(db: db_dependency, user: user_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = db.query(Users).filter(Users.id == user.get("user_id")).first()
    user.phone_number = phone_number
    db.add(user)
    db.commit()
