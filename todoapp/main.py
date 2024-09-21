from fastapi import FastAPI
from database import engine, get_db
import models
import routers
from models import Todos, User
from routers import auth, todos, admin, users
from contextlib import asynccontextmanager
from models import create_db_and_tables

from starlette_admin.contrib.sqla import Admin, ModelView # type: ignore

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("db created ")
    create_db_and_tables()
    yield  # Your application runs during this yield


app = FastAPI()


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

admin = Admin(engine, title="Todo App")

admin.add_view(ModelView(Todos))
admin.add_view(ModelView(User))
admin.mount_to(app)





