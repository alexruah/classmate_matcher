from sqlalchemy.orm import Session
from app.database import models
import boto3
from scipy.cluster.hierarchy import linkage, fcluster
import numpy as np

def get_user_info(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    student_info = db.query(models.StudentInfo).filter(models.StudentInfo.student_id == user_id).first()
    return {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "info": student_info.info if student_info else ""
    }

def generate_embeddings(user_info: dict):
    # Assuming you have set up AWS Bedrock and have the necessary credentials
    client = boto3.client('bedrock')
    response = client.generate_embeddings(
        Text=user_info["info"]
    )
    return response["Embeddings"]

def create_groups(users_embeddings: list, n_clusters: int = 5):
    embeddings_matrix = np.array(users_embeddings)
    Z = linkage(embeddings_matrix, 'ward')
    labels = fcluster(Z, n_clusters, criterion='maxclust')
    groups = {}
    for idx, label in enumerate(labels):
        if label not in groups:
            groups[label] = []
        groups[label].append(users_embeddings[idx])
    return groups