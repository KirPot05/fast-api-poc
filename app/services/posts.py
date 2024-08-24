# from sqlalchemy.orm import Session
# from models.posts import Post as PostModel
# from schemas.posts import Post as PostSchema


# def get_post(db: Session, post_id: int):
#     return db.query(PostModel).filter(PostModel.id == post_id).first()


# def get_posts(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(PostModel).offset(skip).limit(limit).all()


# def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 10):
#     return db.query(PostModel).filter(PostModel.user_id == user_id).offset(skip).limit(limit).all()


# def create_post(db: Session, post: PostSchema):
#     new_post = PostModel(
#         title=post.title,
#         description=post.description,
#         user_id=post.user_id
#     )
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post


# def update_post(db: Session, post_id: int, post: PostSchema):
#     db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
#     if not db_post:
#         return None
#     db_post.title = post.title
#     db_post.description = post.description
#     db.commit()
#     db.refresh(db_post)
#     return db_post


# def block_post(db: Session, post_id: int):
#     db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
#     if not db_post:
#         return None
#     db_post.is_blocked = True
#     db.commit()
#     return db_post


# def delete_post(db: Session, post_id: int):
#     post = db.query(PostModel).filter(PostModel.id == post_id).first()
#     if post:
#         db.delete(post)
#         db.commit()
#     return post


from sqlalchemy.orm import Session
from schemas.posts import Post as PostModel
from models.posts import PostCreate, Post as PostSchema


def get_post(db: Session, post_id: int) -> PostSchema:
    return db.query(PostModel).filter(PostModel.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(PostModel).offset(skip).limit(limit).all()


def create_post(db: Session, post: PostCreate) -> PostSchema:
    db_post = PostModel(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post_update: PostCreate):
    post_query = db.query(PostModel).filter(PostModel.id == post_id)
    db_post = post_query.first()

    if db_post is None:
        return None

    post_query.update(post_update.model_dump())
    db.commit()
    db.refresh(db_post)
    return db_post


def block_post(db: Session, post_id: int) -> PostSchema:
    post_query = db.query(PostModel).filter(PostModel.id == post_id)
    if post_query.first() is None:
        return None
    post_query.update({"is_blocked": True})
    db.commit()
    return post_query.first()


def delete_post(db: Session, post_id: int) -> PostSchema:
    post_query = db.query(PostModel).filter(PostModel.id == post_id)
    post = post_query.first()
    if post is None:
        return None
    db.delete(post)
    db.commit()
    return post
