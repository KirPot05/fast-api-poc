from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db_connection
from schemas.posts import Post as PostSchema
import services.posts as post_services
from models.posts import PostBase, Post, PostCreate


router = APIRouter()


@router.post("/posts/", response_model=Post)
def create_new_post(post: PostBase, db: Session = Depends(get_db_connection)):
    return post_services.create_post(db=db, post=post)


@router.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db_connection)):
    db_post = post_services.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.get("/posts/", response_model=list[Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_connection)):
    return post_services.get_posts(db=db, skip=skip, limit=limit)


@router.get("/users/{user_id}/posts/", response_model=list[Post])
def read_user_posts(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db_connection)):
    return post_services.get_user_posts(db=db, user_id=user_id, skip=skip, limit=limit)


# @router.put("/posts/{post_id}", response_model=Post)
# def update_existing_post(post_id: int, post: PostBase, db: Session = Depends(get_db_connection)):
#     db_post = post_services.update_post(db=db, post_id=post_id, post=post)
#     if db_post is None:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return db_post

@router.put("/posts/{post_id}")
def update_post_route(post_id: int, post_update: PostCreate, db: Session = Depends(get_db_connection)):
    updated_post = post_services.update_post(db, post_id, post_update)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post


@router.put("/posts/{post_id}/block", response_model=Post)
def block_existing_post(post_id: int, db: Session = Depends(get_db_connection)):
    db_post = post_services.block_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.delete("/posts/{post_id}", response_model=Post)
def delete_existing_post(post_id: int, db: Session = Depends(get_db_connection)):
    db_post = post_services.delete_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
