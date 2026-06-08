
# SmartShop Assistant 🛍️

> AI-powered e-commerce chatbot using Retrieval-Augmented Generation (RAG) — answers customer queries from a PDF knowledge base with LLaMA 3.1, ChromaDB, and FastAPI.

🌐 **Live Demo:** [smartshopchat.netlify.app](https://smartshopchat.netlify.app)
🔌 **API:** [Railway Deployment](https://smartshop-assistant-basic-production.up.railway.app/docs)

---

## Features

- **PDF ingestion** — loads and chunks policy documents into semantically meaningful segments
- **Semantic search** — ChromaDB vector store with HuggingFace embeddings for accurate retrieval
- **LLaMA 3.1 via Groq** — sub-second LLM inference, context-grounded responses
- **FastAPI REST endpoint** — production-ready API with auto-generated Swagger docs
- **Full RAG pipeline** — LangChain LCEL chain connecting retrieval, prompting, and generation
- **Dockerized** — containerized deployment ready for any cloud platform
- **Terminal chatbot** — interactive CLI mode for local testing

---

## Tech Stack

| Technology | Purpose |
|---|---|
| LangChain | RAG pipeline & LCEL chain |
| ChromaDB | Vector store |
| Groq (LLaMA 3.1) | LLM inference |
| HuggingFace Embeddings | Text → vectors |
| FastAPI | REST API |
| Docker | Containerization |
| Railway | Cloud deployment |
| Netlify | Frontend hosting |
| Python 3.11 | Core language |

---

## Project Structure

```
smartshop-assistant-basic/
├── 07_langchain_rag.py      # Manual RAG pipeline
├── 08_pdf_rag.py            # PDF-based RAG pipeline
├── 09_fastapi_chat.py       # FastAPI REST endpoint
├── index.html               # Frontend chatbot UI
├── Dockerfile               # Container configuration
├── smartshop_policy.pdf     # Knowledge base
├── requirements.txt         # Dependencies
└── .gitignore
```

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/AhmedNihat/smartshop-assistant-basic.git
cd smartshop-assistant-basic
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file**
```
GROQ_API_KEY=your_groq_api_key_here
```

---

## Usage

**Terminal chatbot:**
```bash
python 08_pdf_rag.py
```

**REST API:**
```bash
uvicorn 09_fastapi_chat:app --reload
```

**Docker:**
```bash
docker build -t smartshop-api .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key smartshop-api
```

---

## API Reference

**Endpoint:** `POST /chat`

**Request:**
```json
{
  "question": "What is the return policy?"
}
```

**Response:**
```json
{
  "answer": "SmartShop accepts returns within 7 calendar days..."
}
```

**Live Swagger UI:** [Railway Docs](https://smartshop-assistant-basic-production.up.railway.app/docs)

---

## How It Works

```
User Query
    │
    ▼
PDF Loader → Text Chunker → HuggingFace Embeddings
                                    │
                                    ▼
                              ChromaDB (Vector Store)
                                    │
                          Semantic Retrieval (Top-K)
                                    │
                                    ▼
                         LangChain LCEL Chain
                                    │
                          Groq API (LLaMA 3.1)
                                    │
                                    ▼
                          Grounded Answer → User
```

---

## Author

**Ahmed Ullah Nihat**
CSE Graduate — Premier University Chittagong
Aspiring ML / AI Engineer

- GitHub: [AhmedNihat](https://github.com/AhmedNihat)
- LinkedIn: [ahmed-ullah-ds](https://linkedin.com/in/ahmed-ullah-ds)
- Email: ahmedullahnihat@gmail.com

---

## License

MIT License — open source, free to use.
```

Copy koro — push koro! 💪
