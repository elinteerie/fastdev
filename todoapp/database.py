from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base



DB_URL = 'sqlite:///./dbtest.db'

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Session
    try:
        yield db
    finally:
        db.close()