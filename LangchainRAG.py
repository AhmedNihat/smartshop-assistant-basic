#SmartShop Assistant- AI E-Commerce ChatBot
#Built with: LangChain, Groq, ChromaDB
#Author: Ahmed Ullah Nihat
#Date: 2026-06-03

import os
import chromadb
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

documents = [
    "We offer free delivery on orders above 500 BDT. Standard delivery takes 3-5 business days.",
    "Our return policy allows returns within 7 days of delivery. Product must be unused and in original packaging.",
    "We have over 10,000 products including electronics, clothing, and home appliances.",
    "Customer support is available 24/7 via chat, email at support@smartshop.com, or call 01800-SHOP.",
    "Payment methods accepted: bKash, Nagad, credit card, debit card, and cash on delivery."
]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

docs = [
    Document(page_content=documents[0], metadata={"topic": "delivery"}),
    Document(page_content=documents[1], metadata={"topic": "return"}),
    Document(page_content=documents[2], metadata={"topic": "products"}),
    Document(page_content=documents[3], metadata={"topic": "support"}),
    Document(page_content=documents[4], metadata={"topic": "payment"}),
]

client = chromadb.PersistentClient(path="./chroma_db")

vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="smartshop",
    client=client,
    persist_directory="./my_chroma_db"
)


retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 2, "score_threshold": 0.5}
)

prompt = PromptTemplate(
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
    api_key=os.environ.get("GROQ_API_KEY")
)

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])
    


chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm
)

while True:
    question = input("Your question (or 'exit' to quit): ")
    if question.lower() == "exit":
        break
    try:
        response = chain.invoke(question)
        print(response.content)
    except Exception as e:
        print("Something went wrong. Please try again.")
