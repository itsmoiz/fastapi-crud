from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from . import schemas, crud, models
from fastapi import (
    FastAPI,
    Depends,
    UploadFile,
    File,
    Form,
    BackgroundTasks
)
import os
import shutil

from . import crud, schemas
from .background_tasks import process_uploaded_file

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
async def create_post_with_file(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    file_path = f"app/uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    post = crud.create_post(
        db=db,
        title=title,
        content=content,
        user_id=user_id,
        file_path=file_path
    )

    background_tasks.add_task(
        process_uploaded_file,
        file_path
    )

    return post



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
