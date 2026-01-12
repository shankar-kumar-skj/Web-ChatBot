# chunker.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def chunk_text(text, url="unknown_url", title="Untitled Page"):
    """
    Splits website text into semantic chunks with metadata.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    return [
        Document(
            page_content=chunk,
            metadata={
                "source": url,
                "title": title
            }
        )
        for chunk in chunks
    ]
