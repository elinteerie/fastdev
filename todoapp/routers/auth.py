from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from routers.todos import db_dependency
from models import User
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy import or_
import os
from jose import jwt
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
print(SECRET_KEY)
ALGORITHM = os.getenv('ALGORITHM')
print(ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')



router = APIRouter(tags=['Authentication'])

#Encrypt Password
bcrypt_context = CryptContext(schemes=['argon2', 'bcrypt'], default='argon2', deprecated='auto')

#Authenticate Users
def authenticate_user(username_or_email: str, password: str, db: db_dependency):
    user = db.query(User).filter(or_(User.username == username_or_email, User.email == username_or_email)).first()
    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta ):
    encode = {"sub": username, "id": user_id}  
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    

 

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str



@router.post('/auth', status_code=status.HTTP_201_CREATED)
async def create_user(user_request: CreateUserRequest, db: db_dependency):
    
    create_user = User(username = user_request.username,
        email = user_request.email,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        role = user_request.role,
        hashed_password = bcrypt_context.hash(user_request.password),
        is_active = True)
    
    db.add(create_user)
    db.commit()
    return {
        'message': "User Created"
    }
    
    

@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return {
            "Failed Authentication"
        }
    
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    
    
    return {
        "Authenticated": token
    }
    