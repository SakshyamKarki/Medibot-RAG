from langchain.tools import Tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstore/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

def search_medical_docs(query: str) -> str:
    docs = db.similarity_search(query, k=3) #retrieving top 3 relevant chunks for better context
    return "\n".join([d.page_content for d in docs])

rag_tool = Tool(
    name="Medical Knowledge Base",
    func=search_medical_docs,
    description=(
        "Use this tool for any medical question about diseases, treatments, "
        "medications, anatomy, or health conditions."
    ),
)