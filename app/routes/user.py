from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database import SessionLocal, get_db
from app import models, schemas
from app.schemas import user_schemas
from app import utils
from typing import List
router = APIRouter()


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(user_credentials.username == models.User.email).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    return db_user


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserOutSchema)
def register_user(user: user_schemas.UserRegisterSchema, db: Session = Depends(get_db)):
    hash_password = utils.hash_password(user.password)
    user.password = hash_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/user/{id}", response_model=user_schemas.UserOutSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(id == models.User.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")

    return user


@router.get("/users/all/", response_model=List[user_schemas.UserOutSchema])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Do not have any users in our base")

    return users