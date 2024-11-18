from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import models, database
from app.schema import UserCreate, UserRead, UserReadWithClasses, StudentInfoUpdate
from app.crud import create_user, get_user_by_email, get_users, delete_user, update_user_info
from SERVER.app.embeddings_service.embeddings import update_student_data

router = APIRouter()

@router.post("/users/", response_model=UserRead)
def create_user_route(user: UserCreate, db: Session = Depends(database.get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = create_user(db, user)
    update_student_data(created_user.id, user.info, user.class_name)  # Update embeddings
    return created_user

@router.get("/users/{email}", response_model=UserReadWithClasses)
def read_user(email: str, db: Session = Depends(database.get_db)):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{email}/info", response_model=UserRead)
def update_user_info_route(email: str, info_update: StudentInfoUpdate, db: Session = Depends(database.get_db)):
    user = update_user_info(db, email, info_update.info)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_student_data(user.id, info_update.info, user.class_name)  # Update embeddings
    return user

@router.get("/users/", response_model=list[UserRead])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return get_users(db, skip, limit)

@router.delete("/users/{email}", response_model=UserRead)
def delete_user_route(email: str, db: Session = Depends(database.get_db)):
    user = delete_user(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user