#from sqlalchemy.orm import Session, sessionmaker
#from sqlalchemy.engine import create_engine
from sqlmodel import Session, create_engine
#from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()





DB_URL = os.getenv('DB_URL')
print(DB_URL)
connect_arg= {"check_same_thread": False}
engine = create_engine(DB_URL, connect_args=connect_arg, echo=True)

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()


def get_db():
    with Session(engine) as session:
        yield session