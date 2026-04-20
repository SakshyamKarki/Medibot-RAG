from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings         
from langchain_community.vectorstores import FAISS

loader = PyPDFLoader("data/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=350, #reduced chunk size for better context handling
    chunk_overlap=100 #increased overlap to maintain context across chunks
)
docs = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_documents(docs, embeddings)
db.save_local("vectorstore/faiss_index")

print("Vector DB created successfully")
