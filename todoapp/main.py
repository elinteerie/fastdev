from fastapi import FastAPI
from database import engine
import models
from models import Todos
from starlette_admin.contrib.sqla import Admin, ModelView # type: ignore


app = FastAPI()

admin = Admin(engine, title="Todo App")

admin.add_view(ModelView(Todos))
admin.mount_to(app)



models.Base.metadata.create_all(bind=engine)

