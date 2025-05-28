from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from random import randint
from typing import List

from app.database import get_db
from app.schemas.response import Response_PyModel_V2
from app.schemas.post import Post_PyModel
from app.models.post import Posts

'''------------------------------------------------------------------'''

router = APIRouter(
    prefix="/v2/api/posts",
    tags=["Posts"]
)


'''-------------- V2 APIs -------------'''

@router.get("/", response_model=List[Response_PyModel_V2])
def get_posts(db: Session = Depends(get_db)):
    '''get all posts'''
    data = db.query(Posts).all()
    
    # sending res
    return data

@router.get("/{pid}", response_model=Response_PyModel_V2)
def get_specific_post(pid: int, db: Session = Depends(get_db)):
    '''retrieving a post by ID'''
    
    req_post = db.query(Posts).filter(Posts.id == pid).first()
    
    if not req_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id:{pid} does not exist"
        )
    
    return req_post

@router.post("/makepost", response_model=Response_PyModel_V2)  
def make_post(ppost: Post_PyModel, db: Session = Depends(get_db)):
    '''create a new post'''
    
    # making a new entry
    # * This is not a efficient way if there are many columns. Better to unpack the incoming fields using ** and dict()
    # new_post = Posts(
    #     title=ppost.title, 
    #     content=ppost.content,  
    #     published=ppost.published,  
    #     tags=ppost.tags
    # )
    
    # * Better way to insert the information by unpacking the dict
    new_post = Posts(**ppost.dict())
    
    db.add(new_post)        # stage changes 
    db.commit()             # commit change 
    db.refresh(new_post)    # retreive new entry added to DB

    return new_post

@router.delete("/delpost/{pid}")
def delete_post(pid: int, db: Session = Depends(get_db)):
    '''delete a post by ID'''
    
    # make init changes
    del_query = db.query(Posts).filter(Posts.id == pid)
    post = del_query.first()
    
    # if the post was not found
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id:{pid} does not exist"
        )
    
    # Delete entry via the query
    del_query.delete(synchronize_session=False)
    db.commit()         # don't forget to commit the changes
    
    return {
        "status_code": status.HTTP_200_OK,
        "msg": f"post {pid} was deleted successfully",
    }

@router.put("/updatepost/{pid}", response_model=Response_PyModel_V2)
def udpate_post(pid: int, ppost: Post_PyModel, db: Session = Depends(get_db)):
    '''Update a post by ID. Remember that PUT is used to replace the entire object/data'''
    
    findpost_query = db.query(Posts).filter(Posts.id == pid)
    post = findpost_query.first()
    
    # the post to be updated is not found
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id:{pid} does not exist"
        )
    
    # stage the changes (update needs a dict for values)
    findpost_query.update(ppost.dict(), synchronize_session=False)

    # commit the changes 
    db.commit()
    
    return findpost_query.first()
    