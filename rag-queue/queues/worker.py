from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_qdrant import QdrantVectorStore



load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview", api_key=api_key)

vectorstore = QdrantVectorStore.from_existing_collection(url="http://localhost:6333", collection_name="rag-collection", embedding=embeddings_model)


def process(user_query: str):
    search_result = vectorstore.similarity_search(user_query)

    context = "\n\n\n".join([f"Page Content: {doc.page_content}\nPage Number: {doc.metadata.get('page_label')} \n{doc.metadata.get('source')}\n File Name: {doc.metadata.get('file_name')}" for doc in search_result])

    SYSTEM_PROMPT = """
    You are an expert AI assistant who answers user queries based on the provided context. 
    You will use the context to generate a response to the user's question based on the provided context.
     
    Context:
    {context}
    
    Response:
    """

    client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

    response = client.chat.completions.create(
                model="gemini-3.6-flash",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_query},
                ]                
            )

    print(response.choices[0].message.content)
    return response.choices[0].message.content


