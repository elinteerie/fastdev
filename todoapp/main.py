from fastapi import FastAPI
from database import engine, get_db
import models
import routers
from models import Todos, User
from routers import auth, todos
from starlette_admin.contrib.sqla import Admin, ModelView # type: ignore


app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)

admin = Admin(engine, title="Todo App")

admin.add_view(ModelView(Todos))
admin.add_view(ModelView(User))
admin.mount_to(app)



models.Base.metadata.create_all(bind=engine)

