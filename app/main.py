from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from . import schemas, crud, models

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----- USERS -----
@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.name, user.email)

@app.get("/users", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

# ----- POSTS -----
@app.post("/posts", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post.title, post.content, post.user_id)

@app.get("/posts", response_model=list[schemas.PostOut])
def list_posts(user_id: int = None, db: Session = Depends(get_db)):
    return crud.get_posts(db, user_id)

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.delete_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted"}

# ----- COMMENTS -----
@app.post("/comments", response_model=schemas.CommentOut)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db, comment.text, comment.post_id)

@app.get("/comments", response_model=list[schemas.CommentOut])
def list_comments(post_id: int = None, db: Session = Depends(get_db)):
    return crud.get_comments(db, post_id)

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = crud.delete_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted"}
