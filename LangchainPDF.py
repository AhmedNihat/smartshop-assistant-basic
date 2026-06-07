import os
import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

loader = PyPDFLoader("smartshop_policy.pdf")
pages = loader.load()

print(f"Loaded {len(pages)} pages from the PDF.")
print(f"First page content:\n{pages[0].page_content[:200]}...") 

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(pages)
print(f"Split into {len(chunks)} chunks.")
print(f"First chunk content:\n{chunks[0].page_content[:200]}...")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_smartshop_db")

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    client=client,
    collection_name="smartshop_policy",
    persist_directory="./chroma_smartshop_db"
)


retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

prompt =  PromptTemplate(
    template="""You are a helpful SmartShop assistant.
Use the following context to answer the customer's question.
if you don't know the answer, say "I don't have that information."

Context : {context}

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

chain =( {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm
)

while True:
    question = input("Your question (or 'exit' to quit): ")
    if question.lower() == "exit":
        break
    try:
        answer = chain.invoke(question)
        print(f"Answer: {answer.content}\n")
    except Exception as e:
        print(f"An error occurred: {e}\n")
