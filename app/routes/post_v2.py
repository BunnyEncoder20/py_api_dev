from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from typing import List, Optional


from app.database import get_db
from app.schemas import response, post, user
from app.models.vote import Votes as Votes_Table
from app.models.post import Posts as Posts_Table
from app.utils import oauth2

'''------------------------------------------------------------------'''

router = APIRouter(
    prefix="/v2/api/posts",
    tags=["Posts"]
)


'''-------------- V2 APIs -------------'''

@router.get("/", response_model=List[response.Posts_Votes_PyModel])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    '''get all posts'''

    # original query
    # data = db.query(Posts_Table).filter(or_(
    #         Posts_Table.title.ilike(f'%{search}%'),       # making the search case insensitive
    #         Posts_Table.content.ilike(f"%{search}%")      # also so that there can be any char before and after key word
    #     )).limit(limit).offset(skip).all()

    data_with_votes_count = (
        db.query(
            Posts_Table,
            func.count(Votes_Table.post_id).label("votes")  # Counting(votes.post_ids) and renaming
        )
        .join(                                              # SQLALCHEMY's join by default is INNER join
            Votes_Table,                                    # LEFT INNER join of Posts on Votes
            Votes_Table.post_id == Posts_Table.id,          # matching the votes.posts_id to posts.id
            isouter=True                                    # to make it OUTER join (cause that is what we want)
        )
        .group_by(
            Posts_Table.id
        )
        .filter(or_(
            Posts_Table.title.ilike(f'%{search}%'),
            Posts_Table.content.ilike(f'%{search}%')
        ))
        .limit(limit)
        .offset(skip)
        .all()
    )

    results = [{
        "post": post_obj,
        "votes": vote_count
    } for post_obj,vote_count in data_with_votes_count]


    # sending back the results
    # print(results)
    return results

# @router.get("/{pid}")
@router.get("/{pid}", response_model=response.Posts_Votes_PyModel)
def get_specific_post(pid: int, db: Session = Depends(get_db)):
    '''retrieving a post by ID'''

    print(f'SERVER: Fetching post with id:')
    req_post = (
        db.query(
            Posts_Table,
            func.count(Votes_Table.post_id).label("votes")
        )
        .join(
            Votes_Table,
            Votes_Table.post_id == Posts_Table.id,
            isouter=True
        )
        .group_by(Posts_Table.id)
        .filter(Posts_Table.id == pid)
        .first()
    )

    if not req_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id:{pid} does not exist"
        )

    post, votes = (req_post)
    return {
        "post":post,
        "votes":votes
    }

@router.get("/by", response_model=List[response.Posts_Votes_PyModel])
def get_posts_by_user(db:Session = Depends(get_db), current_user: user.User_PyModel = Depends(oauth2.get_current_user)):
    '''get all posts by user'''

    print(f"Fetching all posts by User {current_user.id}")
    list_of_posts = (
        db.query(
            Posts_Table,
            func.count(Votes_Table.post_id).label("votes")
        )
        .filter(Posts_Table.user_id == current_user.id).all()
    )
    return list_of_posts

@router.post("/makepost", response_model=response.Response_PyModel_V2)
def make_post(ppost: post.Post_PyModel, db: Session = Depends(get_db), current_user: user.User_PyModel = Depends(oauth2.get_current_user)):
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
    print(f"User {current_user.id} is making a new post")
    new_post = Posts_Table(user_id=current_user.id, **ppost.dict())

    db.add(new_post)        # stage changes
    db.commit()             # commit change
    db.refresh(new_post)    # retreive new entry (with auto gen fields like ID, created_at)

    return new_post

@router.delete("/delpost/{pid}")
def delete_post(pid: int, db: Session = Depends(get_db), curent_user: user.User_PyModel = Depends(oauth2.get_current_user)):
    '''delete a post by ID'''

    # make init changes
    del_query = db.query(Posts_Table).filter(Posts_Table.id == pid)
    post = del_query.first()

    # if the post was not found
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id:{pid} does not exist"
        )

    print(f"INFO: \t User {curent_user.id} is deleting post {pid}")

    # check if post is not of user
    if post.user_id != curent_user.id:
        print(f"ERR: \t  {curent_user.id} cannot delete post {pid} by {post.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'User {curent_user.id} is not autherized to delete post {pid}'
        )

    # Delete entry via the query
    del_query.delete(synchronize_session=False)
    db.commit()         # don't forget to commit the changes

    print(f"INFO: \t Post {pid} deleted successfully")
    return {
        "status_code": status.HTTP_200_OK,
        "msg": f"post {pid} was deleted successfully",
    }

@router.put("/updatepost/{pid}", response_model=response.Response_PyModel_V2)
def udpate_post(pid: int, ppost: post.Post_PyModel, db: Session = Depends(get_db), current_user: user.User_PyModel = Depends(oauth2.get_current_user)):
    '''Update a post by ID. Remember that PUT is used to replace the entire object/data'''

    findpost_query = db.query(Posts_Table).filter(Posts_Table.id == pid)
    post = findpost_query.first()

    # the post to be updated is not found
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id:{pid} does not exist"
        )

    print(f"INFO: \t User {current_user.id} is updating post {pid}")

    # check if post is of user
    if post.user_id != current_user.id:
        print(f"ERR: \t  {current_user.id} cannot update post {pid} by {post.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'User {current_user.id} is not autherized to update post {pid}'
        )


    # stage the changes (update needs a dict for values)
    findpost_query.update(ppost.dict(), synchronize_session=False)

    # commit the changes
    db.commit()

    print(f"INFO: \t Post {pid} updated successfully")

    return findpost_query.first()
