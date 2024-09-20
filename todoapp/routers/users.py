from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from pydantic import BaseModel, Field
from database import get_db
from sqlalchemy.orm import Session
from .auth import get_current_user
from models import User
from passlib.context import CryptContext


router = APIRouter(prefix='/user',tags=['Users'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['argon2', 'bcrypt'], default='argon2', deprecated='auto')

class UserResponse(BaseModel):
    email: str 
    username: str
    first_name: str
    last_name: str
    role: str
    is_active: bool

class UserWithMessageResponse(BaseModel):
    message: str
    user: UserResponse

class PasswordChangeRequest(BaseModel):
    password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)

@router.get('/', status_code=status.HTTP_200_OK, response_model=UserWithMessageResponse)
async def get_user(user: user_dependency, db: db_dependency) -> UserResponse | None:
    if not user:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    user_info = db.query(User).filter(User.id == user.get('id')).first()
    return {
        "message": "done",
        "user": user_info
    }




@router.patch('/change-password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency,db: db_dependency, password: PasswordChangeRequest):
    if not user:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    user_model = db.query(User).filter(User.id == user.get('id')).first()

    if not bcrypt_context.verify(password.password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect Password")
    
    user_model.hashed_password =bcrypt_context.hash(password.new_password)
    db.add(user_model)
    db.commit()




    
