from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel

from typing import List
'''-------------------------'''



# making FastAPI class instance
app = FastAPI()


# Pydantic Model for Validation
class Post_schema(BaseModel):
    title: str
    body: str
    tags: List = []



# Path operation (routes)
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/v1/api/posts")
def get_posts():
    return {
        "postsList": [
            {"p1": "post 1"},
            {"p2": "post 2"},
            {"p3": "post 3"},
        ]
    }

@app.post("/v1/api/post")
def make_post(post: Post_schema) -> dict:
    print(post)
    return {
        "success": True,
        "msg": f'Successfully created post',
        "post_title": post.title,
        "post_body": post.body,
        "tags": post.tags
    }