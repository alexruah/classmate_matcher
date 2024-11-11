from sqlalchemy.orm import Session
from app.database import models
from app.schema import ClassCreate, UserCreate
from app.core.security import get_password_hash

def create_class(db: Session, class_data: ClassCreate):
    db_class = models.Class(
        name=class_data.name,
        description=class_data.description,
        teacher_id=class_data.teacher_id
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def get_class(db: Session, class_id: int):
    return db.query(models.Class).filter(models.Class.id == class_id).first()

def get_classes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Class).offset(skip).limit(limit).all()

def delete_class(db: Session, class_id: int):
    db_class = db.query(models.Class).filter(models.Class.id == class_id).first()
    if db_class:
        db.delete(db_class)
        db.commit()
    return db_class

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
        is_teacher=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def delete_user(db: Session, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def update_user_info(db: Session, email: str, info: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    student_info = db.query(models.StudentInfo).filter(models.StudentInfo.student_id == user.id).first()
    if not student_info:
        student_info = models.StudentInfo(student_id=user.id, info=info)
        db.add(student_info)
    else:
        student_info.info = info
    
    db.commit()
    db.refresh(user)
    return user