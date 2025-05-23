from fastapi import FastAPI, Response
from fastapi.params import Body

from pydantic import BaseModel

from typing import List
from random import randint
'''-------------------------'''



# making FastAPI class instance
app = FastAPI()


# Pydantic Model for Validation
class Post_schema(BaseModel):
    title: str
    body: str
    tags: List = []

# temp database
posts_db = [
    {"_id":1001, "title":"First lines of code", "content":"Hello World", "tags":["#coding", "#projects"]},
    {"_id":1002, "title":"Best food of Humanity", "content":"Pizza *drops mike.", "tags":["#pizza4life", "#italian", "#🤌", "#Mamamia"]},
]



# Path operation (routes)
@app.get("/")
async def root():
    return {"msg": "Hellow World"}

@app.get("/v1/api/posts")
def get_posts() -> List:
    '''get all posts'''
    
    return {
        "data": posts_db
    }

@app.post("/v1/api/post")
def make_post(post: Post_schema) -> dict:
    '''create a new post'''
    
    post_data = post.dict()     # converting from pydantic schema to dict
    post_data["_id"] = randint(1,1000000)
    print(f"[Server] Creating post : {post_data}")
    posts_db.append(post_data)
    return {
        "success": True,
        "msg": "Post published successfully",
        "data": post_data
    }


# using path parameters
@app.get("/v1/api/post/{id}")
def get_specific_post(id: int, res: Response):
    print(f"[Server] Request for fecthing post [{id}]")
    req_post = None
    res.status_code = 404
    for post in posts_db:
        if post["_id"] == id:
            req_post = post
            res.status_code = 200
            break
    return {
        "Status Code": res.status_code ,
        "msg": "Post published successfully" if req_post else "Post not found",
        "data": req_post
    }