# qa.py
def _clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text

def _structure_text(context: str) -> str:
    """
    Structures the retrieved context into readable answer
    """
    sentences = context.split(". ")
    intro = []
    points = []

    for i, s in enumerate(sentences):
        s = s.strip()
        if not s:
            continue
        if i < 2:
            intro.append(s + ".")
        else:
            points.append(s + ".")

    answer = "### 📌 Answer\n\n"
    if intro:
        answer += "**Overview:**\n" + " ".join(intro) + "\n\n"
    if points:
        answer += "**Key Points:**\n" + "".join(f"- {p}\n" for p in points)

    return answer.strip()

def get_answer(question, model, index, chunks, k=4, threshold=1.0):
    """
    Get answer strictly from FAISS + embeddings
    """
    import numpy as np

    question_embedding = model.encode([question]).astype("float32")
    distances, indices = index.search(question_embedding, k)

    # Check relevance
    if distances[0][0] > threshold:
        return "The answer is not available on the provided website."

    # Build context
    context = " ".join(chunks[i].page_content for i in indices[0])
    context = _clean_text(context)

    if not context.strip():
        return "The answer is not available on the provided website."

    return _structure_text(context)
