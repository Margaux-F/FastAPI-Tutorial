from fastapi import FastAPI, HTTPException
from models import Todo, Todo_Pydantic, TodoIn_Pydantic
import tortoise
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel

class Message(BaseModel):
    message: str

app = FastAPI()

@app.get("/")
async def hello():
    return {"Hello" : "World"}

@app.post("/todo/", response_model = Todo_Pydantic)
async def create(todo: TodoIn_Pydantic):
    obj = await Todo.create(**todo.dict(exclude_unset = True))
    return await Todo_Pydantic.from_tortoise_orm(obj)

@app.get("/todo/{id}", response_model = Todo_Pydantic, responses = {404: {'model': HTTPNotFoundError}})
async def get_one(id : int):
    return await Todo_Pydantic.from_queryset_single(Todo.get(id = id))

@app.put("/todo/{id}", response_model = Todo_Pydantic, responses = {404: {"model" : HTTPNotFoundError}})
async def update_one(id : int, todo: TodoIn_Pydantic):
    await Todo.filter(id = id).update(**todo.dict(exclude_unset = True))
    return await Todo_Pydantic.from_queryset_single(Todo.get(id = id))

@app.delete("/todo/{id}", response_model = Message, responses = {404: {"model" : HTTPNotFoundError}})
async def delete_todo(id : int):
    delete_obj = await Todo.filter(id = id).delete()
    if not delete_obj:
        raise HTTPNotFoundError(status_code = 404, detail = "this todo is not found")
    return Message(message = "Successfully deleted")

register_tortoise(
    app,
    db_url = "sqlite://store.db",
    modules = {'models':['models']},
    generate_schemas = True,
    add_exception_handlers = True
)


