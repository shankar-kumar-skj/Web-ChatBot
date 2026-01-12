# vector_store.py
import faiss
import numpy as np
import pickle
import os

DB_PATH = "vector_store.pkl"

def create_vector_store(embeddings):
    """
    Create a FAISS index from embeddings
    """
    embeddings = np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

def save_vector_store(index, chunks):
    """
    Persist FAISS index and chunk metadata
    """
    with open(DB_PATH, "wb") as f:
        pickle.dump((index, chunks), f)

def load_vector_store():
    """
    Load FAISS index and metadata
    """
    if not os.path.exists(DB_PATH):
        return None, None
    with open(DB_PATH, "rb") as f:
        return pickle.load(f)
