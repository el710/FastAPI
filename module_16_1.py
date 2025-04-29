import os
import sys
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def mainpage() -> dict:
    return {"message": "Main page"}

@app.get("/user/admin")
async def adminpage() -> dict:
    return {"message": "You logged as Admin"}

@app.get("/user/{user_id}")
async def user_id_page(user_id: str) -> dict:
    return {"message": f"You logged with user id: {user_id}"}

@app.get("/user/")
async def userpage(username: str = 'None', age: int = 0) -> dict:
    return {"message": f"User info. name: {username}, age: {age}"}

if __name__ == "__main__":
    dir_name, file_name = os.path.split(sys.argv[0])
    name = os.path.splitext(file_name)[0]
 
    os.chdir(dir_name)
    os.system(f"python -m uvicorn {name}:app")