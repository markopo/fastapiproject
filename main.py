from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
import crud
from db import engine, Base, get_db


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ping")
def pong():
    return {"ping": "pong!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


