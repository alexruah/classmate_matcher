from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import database
from app.bedrock_service.bedrock import get_user_info, generate_embeddings, create_groups

router = APIRouter()

@router.get("/bedrock/{user_id}/embeddings")
def get_user_embeddings(user_id: int, db: Session = Depends(database.get_db)):
    user_info = get_user_info(db, user_id)
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")
    embeddings = generate_embeddings(user_info)
    return {"embeddings": embeddings}

@router.post("/bedrock/groups")
def create_user_groups(user_ids: list[int], n_clusters: int = 5, db: Session = Depends(database.get_db)):
    users_embeddings = []
    for user_id in user_ids:
        user_info = get_user_info(db, user_id)
        if user_info:
            embeddings = generate_embeddings(user_info)
            users_embeddings.append(embeddings)
    groups = create_groups(users_embeddings, n_clusters)
    return {"groups": groups}