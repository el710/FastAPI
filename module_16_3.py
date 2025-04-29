from fastapi import FastAPI, Path
from typing import Annotated
import os
import sys

app = FastAPI()

users = {"1": "Name: Example, age: 18"}

@app.get("/users")
async def get_all_users() -> dict:
    return users

@app.post("/user/{username}/{age}")
async def add_user(username: Annotated[str, Path(min_length=5, max_length=28, description="Enter username", examples="Peter")],
                   age: Annotated[int, Path(ge=16, le=100, description="Enter age", examples="33")]) -> str:
    next_id = str(int(max(users, key=int)) + 1)
    users[next_id] = f"Name: {username}, age: {age}"
    return f"User {next_id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[str, Path(description="Enter id number of user", examples="1")],
                      username: Annotated[str, Path(min_length=5, max_length=28, description="Enter username", examples="Peter")],
                      age: Annotated[int, Path(ge=16, le=100, description="Enter age", examples="33")]) -> str:
    users[user_id] = f"Name: {username}, age: {age}"
    return f"The user {user_id} is udated"

@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[str, Path(description="Enter id number of user", examples="1")]) -> str:
    return f"{users.pop(user_id)} deleted"

if __name__ == "__main__":
    dir, file = os.path.split(sys.argv[0])
    os.chdir(dir)
    name = os.path.splitext(file)[0]
    os.system(f"python -m uvicorn {name}:app")