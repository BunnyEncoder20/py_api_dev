from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from random import randint
from typing import List

from app.database import get_db_connection
from app.schemas.response import Response_PyModel
from app.schemas.post import Post_PyModel

'''------------------------------------------------------------------'''

router = APIRouter(
    prefix="/v1/api/posts",
    tags=["Posts"]
)

# Making connection to Postgre DB
conn = get_db_connection()      # conn instance
cursor = conn.cursor()          # cursor obj


'''-------------- V1 APIs -------------'''
@router.get("/",)
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
@router.get("/{pid}", response_model=Response_PyModel)
def get_specific_post(pid: int):

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

@router.post("/makepost", response_model=Response_PyModel)  # how to set default status codes for a path ops
def make_post(post: Post_PyModel):
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

@router.delete("/delpost/{pid}", response_model=Response_PyModel) # specifying response model for standardized reponses
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

@router.put("/updatepost/{pid}", response_model=Response_PyModel)
def udpate_post(pid: int, ppost: Post_PyModel):
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
