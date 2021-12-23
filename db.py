from typing import List
from databases.core import DatabaseURL

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import databases
import sqlalchemy
from datetime import date, datetime

from sqlalchemy import sql
from sqlalchemy import engine
from sqlalchemy.sql.dml import ValuesBase
from sqlalchemy.sql.functions import now
from starlette.routing import NoMatchFound

DATABASE_URL = "sqlite:///./test.db"

metadata = sqlalchemy.MetaData()

database = databases.Database(DatabaseURL)

register = sqlalchemy.table(
    "register",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("date_created", sqlalchemy.DateTime())
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check same thread": False}
)

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect

@app.on_event("shutdown")
async def disconnect():
    await database.disconnect

class Register():
    id : int
    name : str
    date_created: date

class RegisterIn(BaseModel):
    name : str = Field(...)

@app.post("./register/", response_model=Register)
async def create(r: RegisterIn = Depends()):
    query = Register.insert().values(
        name = r.name,
        date_created = datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

##testtttt
##try here







