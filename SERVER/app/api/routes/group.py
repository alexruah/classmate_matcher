from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import database
from SERVER.app.embeddings_service.embeddings import get_user_info, generate_embeddings, create_groups, get_chromadb_client

router = APIRouter()

@router.get("/group/{user_id}/embeddings")
def get_user_embeddings(user_id: int, db: Session = Depends(database.get_db), chromadb_client = Depends(get_chromadb_client)):
    user_info = get_user_info(db, user_id)
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")
    embeddings = generate_embeddings(user_info)
    return {"embeddings": embeddings}

@router.post("/group/groups")
def create_user_groups(class_name: str, n_clusters: int = 5, db: Session = Depends(database.get_db), chromadb_client = Depends(get_chromadb_client)):
    collection = chromadb_client.get_or_create_collection(name=f"class_{class_name}")
    all_students = collection.get()
    embeddings = all_students["embeddings"]
    student_ids = all_students["ids"]
    if len(student_ids) < n_clusters:
        raise HTTPException(status_code=400, detail="Not enough students to create groups.")
    groups = create_groups(embeddings, n_clusters)
    return {"groups": groups}