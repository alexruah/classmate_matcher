import ollama 
import chromadb
import requests

from sqlalchemy.orm import Session
from app.database import models
from sklearn.cluster import KMeans, linkage, fcluster
import numpy as np


client = chromadb.PersistentClient("./chroma_storage")

def update_student_data(student_id, student_info, class_name):
    """
    Update or create a vector embedding for a student in a class-specific collection.
    Args:
        student_id (str): Unique ID for the student.
        student_info (str): Information submitted by the student.
        class_name (str): Name of the class.
    """
    # Retrieve class collection
    collection = get_class_collection(class_name)

    # Generate embedding using Ollama's model
    response = ollama.embeddings(model="mxbai-embed-large", prompt=student_info)
    embedding = response["embedding"]

    # Check if the student ID exists in the collection
    existing_student = collection.get(ids=[student_id])
    if existing_student["ids"]:
        # Update existing vector
        collection.update(
            ids=[student_id],
            embeddings=[embedding],
            metadatas=[{"info": student_info}]
        )
        print(f"Updated embedding for student ID: {student_id} in class: {class_name}")
    else:
        # Add a new entry
        collection.add(
            ids=[student_id],
            embeddings=[embedding],
            metadatas=[{"info": student_info}]
        )
        print(f"Created embedding for student ID: {student_id} in class: {class_name}")


def get_class_collection(class_name):
    """
    Retrieve or create a ChromaDB collection for a specific class.
    Args:
        class_name (str): Name of the class.
    Returns:
        ChromaDB Collection
    """
    return client.get_or_create_collection(name=f"class_{class_name}")

def create_groups(users_embeddings: list, n_clusters: int):
    embeddings_matrix = np.array(users_embeddings)
    Z = linkage(embeddings_matrix, 'ward')
    labels = fcluster(Z, n_clusters, criterion='maxclust')
    groups = {}
    for idx, label in enumerate(labels):
        if label not in groups:
            groups[label] = []
        groups[label].append(users_embeddings[idx])
    return groups

def get_chromadb_client():
    return client