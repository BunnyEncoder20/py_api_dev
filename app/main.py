from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from typing import List, Optional
from random import randint

# loading env variables
from dotenv import load_dotenv
load_dotenv() # loading the env variables
'''-------------------------'''
from .database import get_db_connection             
from .database import engine, SessionLocal, get_db
from . import models





# making FastAPI class instance
app = FastAPI()


# Pydantic Model for Validation
class Post_Model(BaseModel):
    # _id: int
    title: str
    content: str
    published: bool
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

# Making connection to Postgres DB using SLQ Alchemy
models.Base.metadata.create_all(bind=engine)            # needed in main to create tables at server startup




# Path operation (routes)
@app.get("/", response_model=Response_Model)
async def root():
    return {"status_code": status.HTTP_200_OK , "msg": "Hellow World"}

@app.get("/v1/api/posts")
def get_posts():
    '''get all posts'''
    # execute SQL query on DB server
    cursor.execute("""
        SELECT * FROM posts_table
        ORDER BY created_at DESC, id DESC
        LIMIT 100;
    """)
    # fetch results of query from DB server
    data = cursor.fetchall()    # fetchall() for multiple posts and fetchone() for fetching by ID

    # sending res
    return {
        "status_code": status.HTTP_200_OK,
        "msg": "Listing of all Lastest posts",
        "data": data
    }

# using path parameters
@app.get("/v1/api/post/{pid}")
def get_specific_post(pid: int):
    print(f"[Server] Request for fecthing post {pid}")
    
    # executing SQL query on pg server
    cursor.execute("""
        SELECT * FROM posts_table
        WHERE id = %s  
    """, (str(pid),))    # Need the id to be an string to fit into query here. Also remember how to pass single value tuples.
    
    # Fetch query results from pg server
    req_post = cursor.fetchone()
    
    if not req_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {pid} could not be found"
        )
    
    return {
        "status_code": status.HTTP_200_OK ,
        "msg": "Post fetched successfully",
        "data": req_post
    }


@app.post("/v1/api/makepost", status_code=status.HTTP_201_CREATED)  # how to set default status codes for a path ops
def make_post(post: Post_Model):
    '''create a new post'''
    # execute SQL on pgserver
    cursor.execute("""
        INSERT INTO posts_table (title, content, published, tags)
        VALUES (%s, %s, %s, %s)
        RETURNING *
    """, (post.title, post.content, post.published, post.tags))
    #!!! NEVER USE f"" strings for executing SQL commands. They expose our database to SQL injection attacks, if the user input would contain malicious SQL cmds
    #!!! Python does not escape the values safely like the psycopg2 parameterized %s syntax does.
    
    # fetch the STAGED results from the server
    new_post = cursor.fetchone()

    # Commit the changes to DB
    conn.commit()

    return {
        "status_code": status.HTTP_201_CREATED,
        "msg": "Post published successfully",
        "data": new_post
    }


@app.delete("/v1/api/delpost/{pid}", response_model=Response_Model) # specifying response model for standardized reponses
def delete_post(pid: int):
    # exe sql in pg server
    cursor.execute("""
        DELETE FROM posts_table
        WHERE id = %s
        RETURNING *
    """, (str(pid),))
    
    # fetching results from pg server
    deleted_post = cursor.fetchone()

    # Commit changes to DB
    conn.commit()
    
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id:{pid} does not exist"
        )
    
    # with status code of 203, we cannot send anything back using return dict
    # hence we send a Response item, but otherwise, send a normal return dict
    return {
        "status_code": status.HTTP_200_OK,
        "msg": f"post {pid} was deleted successfully",
        "data": deleted_post
    }
    
@app.put("/v1/api/updatepost/{pid}", response_model=Response_Model)
def udpate_post(pid: int, ppost: Post_Model):
    # execute sql on pg server side
    cursor.execute("""
        UPDATE posts_table
        SET title = %s, content = %s, published = %s, tags = %s
        WHERE id = %s
        RETURNING *
    """, (ppost.title, ppost.content, ppost.published, ppost.tags, str(pid)))

    # fetch the results back from server
    updated_post = cursor.fetchone()
    
    # commit changes to DB 
    conn.commit()
    
    # the post to be updated is not found
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id:{pid} does not exist"
        )
    
    return {
        "status_code": status.HTTP_200_OK,
        "msg": f"post {pid} was updated successfully",
        "data": updated_post
    }
    
    
    
    
    
    
    
    
    
'''-------------- V2 APIs -------------'''

@app.get("/v2/api/posts")
def get_posts(db: Session = Depends (get_db)):
    '''get all posts'''
    data = db.query(models.Posts).all()
    print(data)
    # sending res
    return {
        "status_code": status.HTTP_200_OK,
        "msg": "Listing of all Lastest posts",
        "data": data
    }

@app.get("/v1/api/post/{pid}")
def get_specific_post(pid: int):
    '''retrieving a post by ID'''
    
    # 
    
    
    return {
        "status_code": status.HTTP_200_OK ,
        "msg": "Post fetched successfully",
        "data": req_post
    }


@app.post("/v2/api/makepost", status_code=status.HTTP_201_CREATED)  # how to set default status codes for a path ops
def make_post(ppost: Post_Model, db: Session = Depends(get_db)):
    '''create a new post'''
    
    # making a new entry
    new_post = models.Posts(
        title=ppost.title, 
        content=ppost.content,  
        published=ppost.published,  
        tags=ppost.tags
    )
    
    db.add(new_post)        # stage changes 
    db.commit()             # commit change 
    db.refresh(new_post)    # retreive new entry added to DB

    return {
        "status_code": status.HTTP_201_CREATED,
        "msg": "Post published successfully",
        "data": new_post
    }

