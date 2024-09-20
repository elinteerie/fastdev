from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from pydantic import BaseModel, Field
from models import Todos
from database import get_db
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(prefix='/admin',tags=['Admin'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db:db_dependency):
    print(user.get('role'))
    print(user)
    if user is None or user.get('user_role') != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not Authorized")
    
    return db.query(Todos).all()


@router.delete('/todo-delete/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not Authorized")
    todo_to_delete = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_to_delete is None:
        raise HTTPException(status_code=404, detail="Todo with Id not Found")
    db.delete(todo_to_delete)
    db.commit()

