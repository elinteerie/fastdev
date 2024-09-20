from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from pydantic import BaseModel, Field
from models import Todos
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=['Todos'])


db_dependency = Annotated[Session, Depends(get_db)]

class TodoReponse(BaseModel):
    id: int 
    title: str 
    description: str 
    priority: int 
    completed: bool

class TodoRequest(BaseModel):
    title: str = Field(min_length=4)
    description: str = Field(min_length=7)
    priority: int  = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra":{
            'example':{
                "title": "Coding on Monday",
                "description": "Fixing a Bug on Juggy",
                "priority": 3
            }
        }
    }


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
async def get_all_todos(db: db_dependency):
    all_todos = db.query(Todos).all()
    return {
        "status": "OK",
        "response": all_todos
    }




@router.get('/todos/{todo_id}', status_code=status.HTTP_200_OK)
async def get_a_todos(db: db_dependency, todo_id: int = Path(gt=0) ):
    a_todos = db.query(Todos).filter(Todos.id == todo_id).first()
    if a_todos is not None:
        return {
        "status": "OK",
        "response": a_todos
    }

    raise HTTPException(status_code=404, detail={
        "status": "OK",
        "response": "No Todo with that ID"
    })
    

@router.post('/add-todo', status_code=status.HTTP_201_CREATED, response_model=TodoReponse)
async def add_todo(db: db_dependency, todo: TodoRequest):
    new_todo = Todos(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.put('/update-todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(todo: TodoChangeRequest, db:db_dependency, todo_id: int =Path(gt=0)):
    get_book = db.query(Todos).filter(Todos.id == todo_id).first()
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
async def update_todo(db:db_dependency, todo_id: int =Path(gt=0)):
    get_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if get_todo is None:
        raise HTTPException(status_code=404, detail="Todo with Id not Found")

    db.delete(get_todo)
    db.commit()
    
    return {
        "message": "TODO DELETED"
    }
    