from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

from pydantic import BaseModel, Field
from .database import get_db_connection

from typing import List, Optional
from random import randint

# loading env variables
from dotenv import load_dotenv
load_dotenv() # loading the env variables


'''-------------------------'''



# making FastAPI class instance
app = FastAPI()


# Pydantic Model for Validation
class Post_Model(BaseModel):
    # _id: int
    title: str
    body: str
    tags: List = []

# Pydantic Model for Standardized responses
class Response_Model(BaseModel):
    status_code: int
    msg: Optional[str] = Field(default=None, description="Optional message string")
    data: Optional[dict] = Field(default=None, description="Optional data payload")
    

# temp database
posts_db = [
    {"_id":1001, "title":"First lines of code", "content":"Hello World", "tags":["#coding", "#projects"]},
    {"_id":1002, "title":"Best food of Humanity", "content":"Pizza *drops mike.", "tags":["#pizza4life", "#italian", "#🤌", "#Mamamia"]},
]



# Making connection to Postgre DB
conn = get_db_connection()      # conn instance
cursor = conn.cursor()          # cursor obj



# Path operation (routes)
@app.get("/", response_model=Response_Model)
async def root():
    return {"status_code": status.HTTP_200_OK , "msg": "Hellow World"}

@app.get("/v1/api/posts")
def get_posts():
    '''get all posts'''
    cursor.execute("""
        SELECT * FROM posts_table
        ORDER BY created_at DESC, id DESC
        LIMIT 100;
    """)
    data = cursor.fetchall()
    print(data)
    return {
        "status_code": status.HTTP_200_OK,
        "msg": "Listing of all Lastest posts",
        "data": data
    }

@app.post("/v1/api/post", status_code=status.HTTP_201_CREATED)  # how to set default status codes for a path ops
def make_post(post: Post_Model) -> dict:
    '''create a new post'''
    
    post_data = post.dict()     # converting from pydantic schema to dict
    post_data["_id"] = randint(1,1000000)
    print(f"[Server] Creating post : {post_data}")
    posts_db.append(post_data)
    return {
        "status_code": status.HTTP_200_OK,
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
        "status_code": status.HTTP_200_OK ,
        "msg": "Post published successfully",
        "data": req_post
    }

@app.delete("/v1/api/delpost/{pid}", response_model=Response_Model) # specifying response model for standardized reponses
def delete_post(pid: int):
    
    deleted = None
    for i, post in enumerate(posts_db):
        if post["_id"] == pid:
            deleted = post
            posts_db.pop(i)
            break
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id:{pid} does not exist"
        )
    
    # with status code of 203, we cannot send anything back using return dict
    # hence we send a Response item, but otherwise, send a normal return dict
    return {
        "status_code": status.HTTP_200_OK,
        "msg": f"post {pid} was deleted successfully",
        "data": deleted
    }
    
@app.put("/v1/api/updatepost/{pid}", response_model=Response_Model)
def udpate_post(pid: int, ppost: Post_Model):
    req_post_idx = None
    for i, post in enumerate(posts_db):
        if post["_id"] == pid:
            req_post_idx = i
            break
    
    # the post to be updated is not found
    if not req_post_idx:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id:{pid} does not exist"
        )
    
    # Update post data
    updated_post = ppost.dict()
    updated_post["_id"] = pid
    posts_db[req_post_idx] = updated_post
    return {
        "status_code": status.HTTP_200_OK,
        "msg": f"post {pid} was updated successfully",
        "data": updated_post
    }