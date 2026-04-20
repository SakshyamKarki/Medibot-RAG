"""
rag_tool.py  —  MediBot RAG retrieval tool 

  - Uses all-mpnet-base-v2 
  - Retrieves k=5 chunks instead of k=3
  - Adds source page metadata to the returned context
"""

from langchain.tools import Tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# ── Embedding model ───────────────────
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

# ── Load FAISS index ──────────────────────────────────────────────────────────
db = FAISS.load_local(
    "vectorstore/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


def search_medical_docs(query: str) -> str:
    """
    Retrieve the top-5 most relevant passages from the medical encyclopedia.
    Includes page numbers to help the LLM cite sources.
    """
    docs = db.similarity_search(query, k=5)   # was k=3

    passages = []
    for i, doc in enumerate(docs, 1):
        page = doc.metadata.get("page", "?")
        passages.append(f"[Passage {i} | Page {page}]\n{doc.page_content}")

    return "\n\n".join(passages)


rag_tool = Tool(
    name="Medical Knowledge Base",
    func=search_medical_docs,
    description=(
        "Use this tool for any medical question about diseases, symptoms, "
        "treatments, medications, anatomy, or health conditions. "
        "Returns relevant passages from a medical encyclopedia."
    ),
)