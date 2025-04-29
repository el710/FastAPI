from fastapi import FastAPI, Path
from typing import Annotated
import os
import sys

app = FastAPI()


@app.get("/")
async def mainpage() -> dict:
    return {"message": "Main page"}

@app.get("/user/admin")
async def adminpage() -> dict:
    return {"message": "You logged as Admin"}

@app.get("/user/{user_id}")
async def user_id_page(user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example="88", )]) -> dict:
    return {"message": f"You logged with user id: {user_id}"}

@app.get("/user/{username}/{age}")
async def userpage(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="Pete")]
                   , age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="33")]) -> dict:
    return {"message": f"User info. name: {username}, age: {age}"}



if __name__ == "__main__":
    dir_name, file_name = os.path.split(sys.argv[0])
    name = os.path.splitext(file_name)[0]
 
    os.chdir(dir_name)
    os.system(f"python -m uvicorn {name}:app")