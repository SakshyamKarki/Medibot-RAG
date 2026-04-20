from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ── Load PDF ──────────────────────────────────────────────────────────────────
loader    = PyPDFLoader("data/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf")
documents = loader.load()
print(f"Loaded {len(documents)} pages.")

# ── Split into chunks ─────────────────────────────────────────────────────────
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,       # larger window = more context per chunk
    chunk_overlap=128,    # more overlap prevents info loss at boundaries
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""]
)
docs = splitter.split_documents(documents)
print(f"Split into {len(docs)} chunks.")

# all-mpnet-base-v2: 768-dim, significantly better than all-MiniLM-L6-v2 (384-dim)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": "cpu"},     
    encode_kwargs={"normalize_embeddings": True}
)

# ── Build & save FAISS index ──────────────────────────────────────────────────
print("Building FAISS index (this may take a few minutes)…")
db = FAISS.from_documents(docs, embeddings)
db.save_local("vectorstore/faiss_index")

print("Vector store created and saved to vectorstore/faiss_index")