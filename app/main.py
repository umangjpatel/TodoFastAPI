from fastapi import FastAPI
from typing import List
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app: FastAPI = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


class TodoItem(BaseModel):
    text: str


todo_items: List[TodoItem] = []


async def get_todos(message: str):
    return {"status": message,
            "items": todo_items}


@app.post("/add", response_class=JSONResponse)
async def add_todo_item(item: TodoItem):
    todo_items.append(item)
    return await get_todos(message="Item added successfully")


@app.get("/list", response_class=JSONResponse)
async def get_all_items():
    message: str = "No todo items" if len(todo_items) == 0 else "Items loaded successfully"
    return await get_todos(message=message)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request})


@app.post("/clear", response_class=JSONResponse)
async def clear_todo_items():
    todo_items.clear()
    return await get_todos(message="Items cleared successfully")


@app.delete("/delete/{item_id}", response_class=JSONResponse)
async def delete_todo_item(item_id: int):
    todo_items.pop(item_id)
    return await get_todos(message=f"Item #{item_id + 1} deleted successfully")


@app.put("/update/{item_id}", response_class=JSONResponse)
async def update_todo_item(item_id: int, todo_item: TodoItem):
    todo_items[item_id] = todo_item
    return await get_todos(message=f"Item #{item_id + 1} updated sucessfully")
