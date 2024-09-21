from database import engine
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Column, ForeignKey, Integer, Boolean, String
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    email: str  = Field(unique=True)
    username: str = Field(unique=True)
    first_name: str 
    last_name: str
    hashed_password: str
    is_active: bool = Field(default=True)
    role: str 
    phone_number: str = Field(nullable=True)

    # Relationship: One User can have many Todos
    todos: List["Todos"] = Relationship(back_populates="owner")




class Todos(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    title: str
    description: str
    priority: int = Field(gt=0, lt=11)
    completed: bool = Field(default=False)
    owner_id: int = Field(foreign_key="user.id")

    owner: "User" = Relationship(back_populates='todos')

    


class TodoRequest(SQLModel):
    title: str = Field(min_length=4)
    description: str = Field(min_length=7)
    priority: int  = Field(gt=0, lt=6)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete the project",
                "description": "Finish the project and submit it before the deadline.",
                "priority": 5,
                
            }
        }

class TodoReponse(SQLModel):
    id: int 
    title: str 
    description: str 
    priority: int 
    completed: bool
    owner_id: int




def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
