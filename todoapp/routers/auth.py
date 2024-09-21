from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from database import get_db

from models import User
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy import or_
import os
from jose import JWTError, jwt
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
print(SECRET_KEY)
ALGORITHM = os.getenv('ALGORITHM')
print(ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')



router = APIRouter(prefix='/auth',tags=['Authentication'])

#Encrypt Password
bcrypt_context = CryptContext(schemes=['argon2', 'bcrypt'], default='argon2', deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
db_dependency = Annotated[Session, Depends(get_db)]


#Authenticate Users
def authenticate_user(username_or_email: str, password: str, db: db_dependency):
    user = db.query(User).filter(or_(User.username == username_or_email, User.email == username_or_email)).first()
    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

#Create a JWT
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta ):
    encode = {"sub": username, "id": user_id, "role": role}  
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    

#Decode a JWT
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Could Not Valid Credential")
        return {
            'username': username, "id": user_id, "user_role": user_role
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Could Not Valid Credential")
        

 

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str 


class Token(BaseModel):
    access_token: str
    token_type: str
    expires: str


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user_request: CreateUserRequest, db: db_dependency):
    
    create_user = User(username = user_request.username,
        email = user_request.email,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        role = user_request.role,
        hashed_password = bcrypt_context.hash(user_request.password),
        is_active = True,
        phone_number = user_request.phone_number
        )
    
    db.add(create_user)
    db.commit()
    return {
        'message': "User Created"
    }
    
    

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Could Not Valid Credential")
        
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires": "20 Minutes"
    }
    