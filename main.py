from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

from pydantic import BaseModel

from typing import List
from random import randint
'''-------------------------'''



# making FastAPI class instance
app = FastAPI()


# Pydantic Model for Validation
class Post_Model(BaseModel):
    title: str
    body: str
    tags: List = []

class Response_Model(BaseModel):
    status_code: int
    msg: str = ""
    data: dict = {}
    

# temp database
posts_db = [
    {"_id":1001, "title":"First lines of code", "content":"Hello World", "tags":["#coding", "#projects"]},
    {"_id":1002, "title":"Best food of Humanity", "content":"Pizza *drops mike.", "tags":["#pizza4life", "#italian", "#🤌", "#Mamamia"]},
]



# Path operation (routes)
@app.get("/", response_model=Response_Model)
async def root():
    return {"status_code": status.HTTP_200_OK , "msg": "Hellow World"}

@app.get("/v1/api/posts")
def get_posts() -> List:
    '''get all posts'''
    
    return {
        "data": posts_db
    }

@app.post("/v1/api/post", status_code=status.HTTP_201_CREATED)  # how to set default status codes for a path ops
def make_post(post: Post_Model) -> dict:
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
def get_specific_post(id: int):
    print(f"[Server] Request for fecthing post [{id}]")
    
    req_post = None
    for post in posts_db:
        if post["_id"] == id:
            req_post = post
            break
    
    if not req_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} could not be found"
        )
    
    return {
        "Status Code": status.HTTP_200_OK ,
        "msg": "Post published successfully",
        "data": req_post
    }

@app.delete("/v1/api/delpost/{pid}")
def delete_post(pid: int):
    
    deleted = None
    for i, post in enumerate(posts_db):
        if post["_id"] == pid:
            deleted = post
            posts_db.pop(i)
            break
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The post with id:{pid} does not exist"
        )
    
    # with status code of 203, we cannot send anything back using return dict
    # hence we send a Response item, but otherwise, send a normal return dict
    return {
        
    }
    
            