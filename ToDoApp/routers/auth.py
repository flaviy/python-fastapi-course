from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from ..db_session import get_db
from ..requests.create_user_request import CreateUserRequest
from ..models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt

from ..token_response import TokenResponse

context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

'''
zsh: command not found: openslect/ToDoApp  opensl rand -hex 32                                                                                                                               ok | fastApiProject py | at 16:57:52 
> openssl rand -hex 32
bd7fc632fc04c95175050180c4c99f0fd513582c20e5ebcaaf46edbd0930cae6      
'''

SECRET_KEY = 'bd7fc632fc04c95175050180c4c99f0fd513582c20e5ebcaaf46edbd0930cae6'
ALGORITHM = 'HS256'

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str,  expires_delta: timedelta):
    to_encode = {"sub": username, "id": user_id, "role": role}
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        db: db_dependency,
        create_user_request: CreateUserRequest
):
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        hashed_password=context.hash(create_user_request.password),
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        phone_number=create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=15))
    return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {'username': username, 'user_id': user_id, 'role': role}
