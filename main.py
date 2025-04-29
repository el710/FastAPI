from fastapi import Body, FastAPI, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
### html templates
from fastapi.templating import Jinja2Templates
### html forms
from fastapi import Form

from typing import Annotated, List
from pydantic import BaseModel

templates = Jinja2Templates(directory="templates")

import os
import sys

app = FastAPI()

"""
    Get-request from user...

## Examples

# @app.get("/")
# async def welcome() -> dict:
#     return {"message": "Hello world"}

# @app.get("/main")
# async def welcome() -> dict:
#     return {"message": "Main Page"}

### it's basic...
### python -m uvicorn main:app !!!NOTE: must be in work directory to see main.py

### request with parameters: /id?username=Vasya&age=34
@app.get("/id")                  
async def id_paginator(username: str = "vasya", age: int = 34) -> dict: ## with values by default
    return {"User": username, "Age": age}

### adress-type request: *.org/user/A/B
# @app.get("/user/{first_name}/{last_name}")
# async def news(first_name: str, last_name: str) -> dict:
#     return {"message": f"Hello, {first_name} {last_name}"}


    # Validate data
    # Path() - set conditions for input data
    #     parameters with Path() default should stay in the end of variables list
    #     but Annotated[] solve this mess
    #     in Path() are used mnemonics: ge - great or equal (>=), le - less or equal (<=) e.t.c
        
    # also see Pydentic()



# @app.get("/user/{username}/{id}")
# async def news(username:str = Path(min_length=3, max_length=15, description="Enter your username", example="meuser")
#                , id:int = Path(ge=0, le=100, description="Enter your id", example="56")) -> dict:
#     return {"message": f"{username}:{id}"}

@app.get("/user/{username}/{id}")
async def news(username: Annotated[str, Path(min_length=3, max_length=15, description="Enter your username", example="meuser")]
               , id: Annotated[int, Path(ge=0, le=100, description="Enter your id", example="56")]
               , tail: str) -> dict: ## use Annotated to avoid warnings about tail, because tail must be first in this list
    return {"message": f"{username}:{id}"}
"""
#######################################################
"""
    Project with dictionary

    We work throughout APi with data (dictionary)


"""

# message_db = {"0": "First post in FastAPI"}
"""
    make new class for messages with BaseModel
"""
message_db = []

class Message(BaseModel):
    id: int = None
    text: str


@app.get("/")
#async def get_all_message() -> dict:
async def get_all_message(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("work.html", {"request": request, "base_messages": message_db})

"""
@app.get("/message/{message_id}") - all /therms/ in adress are parameters: message, message_id
"""

@app.get("/message/{message_id}")
# async def get_message(message_id: str) -> dict:
async def get_message(request: Request, message_id: int) -> HTMLResponse:
    try: 
        return templates.TemplateResponse("work.html", {"request": request, "message": message_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post("/")
async def create_message(request: Request, message: str = Form()) -> HTMLResponse:
    # current_index = str(int(max(message_db, key=int)) + 1)
    # message_db[current_index] = message

    if message_db:
        message_id = max(message_db, key=lambda item: item.id).id + 1
    else:
        message_id = 0

    message_db.append(Message(id=message_id, text=message))
    return templates.TemplateResponse("work.html", {"request": request, "base_messages": message_db})


@app.put("/message/{message_id}")
async def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = message_db[message_id]
        edit_message.text = message
        return f"Message {edit_message} update"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")

@app.delete("/message/{message_id}")
async def delete_message(message_id: int) -> str:
    try:
        message_db.pop(message_id)
        return f"Message ID={message_id} deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")

@app.delete("/")
async def delete_all_messages() -> str:
    message_db.clear()
    return "All messages deleted"



if __name__ == "__main__":
    dir_name, file_name = os.path.split(sys.argv[0])
    name = os.path.splitext(file_name)[0]
 
    os.chdir(dir_name)
    os.system(f"python -m uvicorn {name}:app")