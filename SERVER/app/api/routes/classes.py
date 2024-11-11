
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import models, database
from app.schema import ClassCreate, ClassRead, ClassReadWithStudents
from app.crud import create_class, get_class, get_classes, delete_class

router = APIRouter()

@router.post("/classes/", response_model=ClassRead)
def create_class_route(class_data: ClassCreate, db: Session = Depends(database.get_db)):
    return create_class(db, class_data)

@router.get("/classes/{class_id}", response_model=ClassReadWithStudents)
def read_class(class_id: int, db: Session = Depends(database.get_db)):
    db_class = get_class(db, class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

@router.get("/classes/", response_model=list[ClassRead])
def read_classes(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return get_classes(db, skip, limit)

@router.delete("/classes/{class_id}", response_model=ClassRead)
def delete_class_route(class_id: int, db: Session = Depends(database.get_db)):
    db_class = delete_class(db, class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class