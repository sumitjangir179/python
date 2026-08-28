from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

pdf_path = Path(__file__).parent / "sample.pdf"

print(f"Loading PDF from: {pdf_path}")

loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

# for i, doc in enumerate(docs):
#     print(f"Document {i + 1}:")
#     print(f"Page Content: {doc.page_content[:100]}...")  # Print first 100 characters of the page content
#     print(f"Metadata: {doc.metadata}")
#     print("\n")


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(documents = docs)


api_key = os.getenv("GEMINI_API_KEY")
embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview", api_key=api_key)

vectorstore = QdrantVectorStore.from_documents(
    docs,
    embeddings_model,
    url="http://localhost:6333",
    collection_name="rag-collection",
)

print(f"Indexing completed. Total chunks indexed: {len(chunks)}")
