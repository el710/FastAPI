from fastapi import FastAPI, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel, ConfigDict
import os
import sys

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users")
async def get_all_users() -> list[User]:
    return users

@app.post("/user/{username}/{age}")
async def add_user(username: Annotated[str, Path(min_length=5, max_length=28, description="Enter username", example="Peter")],
                   age: Annotated[int, Path(ge=16, le=100, description="Enter age", example="33")]) -> User:
    
    if len(users):
        _id = users[-1].id + 1
    else:
        _id = 1
      
    users.append(User(id=_id, username=username, age=age))

    return users[-1]

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(description="Enter id number of user", example="1")],
                      username: Annotated[str, Path(min_length=5, max_length=28, description="Enter username", example="Peter")],
                      age: Annotated[int, Path(ge=16, le=100, description="Enter age", example="33")]) -> User:
    for item in users:
        if item.id == user_id:
            item.username = username
            item.age = age
            return item
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(description="Enter id number of user", example="1")]) -> User:
    for item in users:
        if item.id == user_id:
            users.remove(item)
            return item
    raise HTTPException(status_code=404, detail="User not found")
    

if __name__ == "__main__":
    dir, file = os.path.split(sys.argv[0])
    os.chdir(dir)
    name = os.path.splitext(file)[0]
    os.system(f"python -m uvicorn {name}:app")