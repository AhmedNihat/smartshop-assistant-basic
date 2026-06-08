
import os
import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


loader = PyPDFLoader("smartshop_policy.pdf")
pages = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(pages)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_smartshop_db")

vector_store = Chroma.from_documents(
    documents=chunks,   
    embedding=embeddings,
    client=client,
    collection_name="smartshop_policy",
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

prompt =  PromptTemplate(
    template="""You are a helpful SmartShop assistant.
Use the following context to answer the customer's question.
If you don't know the answer, say "I don't have that information."

Context: {context}

Question: {question}

Answer:""",
    input_variables=["context", "question"]
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key =  os.environ.get("GROQ_API_KEY")
)

def format_docs(chunks):
    return "\n\n".join([chunk.page_content for chunk in chunks])

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm
)

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        answer = await chain.ainvoke(request.question)
        return ChatResponse(answer=answer.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM service unavailable: {str(e)}")