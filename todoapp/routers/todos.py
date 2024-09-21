from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from models import Todos, TodoRequest, TodoReponse
from database import get_db
from sqlalchemy.orm import Session
from .auth import get_current_user


router = APIRouter(tags=['Todos'])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



class TodoChangeRequest(BaseModel):
    title: str = Field(min_length=4)
    description: str = Field(min_length=7)
    priority: int  = Field(gt=0, lt=6)
    completed: bool

    model_config = {
        "json_schema_extra":{
            'example':{
                "title": "Coding on Monday",
                "description": "Fixing a Bug on Juggy",
                "priority": 3,
                'completed': True
            }
        }
    }



@router.get('/todos', status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentification Failed")
    
    todos = db.exec(select(Todos).where(Todos.owner_id== user.get('id'))).all()  # Query all Todos
        
    return  todos
    




@router.get('/todos/{todo_id}', status_code=status.HTTP_200_OK)
async def get_a_todos(user: user_dependency,db: db_dependency, todo_id: int = Path(gt=0) ):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentification Failed")
    
    a_todos = db.exec(select(Todos).where(Todos.id == todo_id).where(Todos.owner_id == user.get('id'))).first()
    if a_todos is not None:
        return {
        "status": "OK",
        "response": a_todos
    }

    raise HTTPException(status_code=404, detail={
        "status": "OK",
        "response": "No Todo with that ID for User"
    })
    

@router.post('/add-todo', status_code=status.HTTP_201_CREATED, response_model=TodoReponse)
async def add_todo(user: user_dependency, db: db_dependency, todo: TodoRequest):
    
    if user is None:
        raise HTTPException(status_code=401, detail="Authentification Failed")
    new_todo = Todos(**todo.model_dump(), owner_id=user.get('id'))
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.put('/update-todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,todo: TodoChangeRequest, db:db_dependency, todo_id: int =Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentification Failed")
    get_book = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if get_book is None:
        raise HTTPException(status_code=404, detail="Todo with Id not Found")

    get_book.title = todo.title
    get_book.description = todo.description
    get_book.completed = todo.completed
    get_book.priority = todo.priority

    db.commit()
    db.refresh(get_book)
    return get_book
    

@router.delete('/delete-todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,db:db_dependency, todo_id: int =Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentification Failed")
    
    get_todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if get_todo is None:
        raise HTTPException(status_code=404, detail="Todo with Id not Found")

    db.delete(get_todo)
    db.commit()
    
    return {
        "message": "TODO DELETED"
    }
    