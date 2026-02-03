from sqlalchemy.orm import Session
from . import models

# ----- USER -----
def create_user(db: Session, name: str, email: str):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user

# ----- POST -----
def create_post(db: Session, title: str, content: str, user_id: int):
    post = models.Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db: Session, user_id: int = None):
    query = db.query(models.Post)
    if user_id:
        query = query.filter(models.Post.user_id == user_id)
    return query.all()

def delete_post(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        return None
    db.delete(post)
    db.commit()
    return post

# ----- COMMENT -----
def create_comment(db: Session, text: str, post_id: int):
    comment = models.Comment(text=text, post_id=post_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments(db: Session, post_id: int = None):
    query = db.query(models.Comment)
    if post_id:
        query = query.filter(models.Comment.post_id == post_id)
    return query.all()

def delete_comment(db: Session, comment_id: int):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        return None
    db.delete(comment)
    db.commit()
    return comment
