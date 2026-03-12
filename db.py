from typing import Annotated
from fastapi import FastAPI
from fastapi.params import Depends
from sqlmodel import SQLModel, create_engine, Session


sqlite_name = "db.sqlite"
sqlite_url = f"sqlite:///{sqlite_name}"
engine = create_engine(sqlite_url, echo=True)


def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
