# embeddings.py
import streamlit as st

from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_embedding_model():
    """
    Load sentence-transformers embedding model
    """
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return model
