# app.py
import streamlit as st
from crawler import extract_text
from chunker import chunk_text
from embeddings import load_embedding_model
from vector_store import create_vector_store, save_vector_store, load_vector_store
from qa import get_answer

# Page setup
st.set_page_config(page_title="Website Chatbot", layout="centered")
st.title("🌐 Web ChatBot")
st.write("Ask questions strictly based on the provided website content.")

# Load model
@st.cache_resource
def load_model():
    return load_embedding_model()

model = load_model()

# URL input
url = st.text_input("Enter Website URL:")

# Session state
if "indexed" not in st.session_state:
    st.session_state.indexed = False

# Indexing button
if st.button("Index Website"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("Indexing website..."):
            text, title = extract_text(url)
            if not text:
                st.error("Unable to extract meaningful content from this website.")
            else:
                chunks = chunk_text(text, url, title)
                embeddings = model.encode([chunk.page_content for chunk in chunks])
                index = create_vector_store(embeddings)

                st.session_state.chunks = chunks
                st.session_state.index = index
                st.session_state.indexed = True

                save_vector_store(index, chunks)
                st.success("Website indexed successfully!")

# Question answering
if st.session_state.indexed:
    question = st.text_input("Ask a question:")
    if question:
        answer = get_answer(
            question,
            model,
            st.session_state.index,
            st.session_state.chunks
        )
        st.subheader("Answer")
        st.write(answer)
