from fastapi import FastAPI, Body
from ComicsLibrary.orchestrators import Orchestrator
from ComicsLibrary.DTO import UserDTO, ComicDTO


app = FastAPI()
orchestrator = Orchestrator()

@app.post("/users/")
def add_user(user_data: UserDTO = Body(...)):
    return orchestrator.add_user(user_data)

@app.post("/comics/")
def add_comic(comic_data: ComicDTO = Body(...)):
    print(f"data in post: {comic_data}")
    return orchestrator.add_comic(comic_data)

@app.get("/comics/")
def get_comic(id: str = None, title: str = None):
    return orchestrator.get_comic(id=id, title=title)

@app.get("/users/")
def get_user(chat_id: str = None, id: str = None):
    return orchestrator.get_user(chat_id=chat_id, id=id)

@app.get("/comics/all")
def get_comics():
    return orchestrator.get_comics()

@app.post("/users/{user_id}/comics/{comic_id}")
def add_comic_to_user(comic_id: str, user_id: str):
    return orchestrator.add_comic_to_user(comic_id, user_id)