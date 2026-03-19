# RepoClarity AI

RepoClarity AI is a **local AI-powered assistant for understanding codebases**.

It indexes your repository, builds a semantic understanding, and lets you **ask questions about your code** using local LLMs.

Everything runs **fully local** - no cloud, no data leaks.

---

<p align="center">
  <strong>Watch the Demo on YouTube</strong><br><br>
  <a href="https://www.youtube.com/watch?v=lZbKBxYY6Jo">
    <img src="https://img.youtube.com/vi/lZbKBxYY6Jo/0.jpg" width="300">
  </a>
</p>

---

## 🚀 What it does

- Analyze any codebase
- Detect frameworks and entrypoints
- Generate repository summaries
- Answer questions about code structure and logic
- Provide a clean UI + CLI access

---

## 🧩 Project Structure

repoclarity-ai/ <br/>
├ frontend/   # Nuxt UI (user interface) <br/>
└ backend/    # FastAPI + RAG pipeline + CLI <br/>

---

## ⚙️ How it works

RepoClarity uses a **RAG (Retrieval-Augmented Generation)** pipeline:

repository → chunking → embeddings → vector search → LLM answers

- Embeddings + vector search via FAISS  
- Local LLMs via Ollama  
- No external APIs required  

---

## 🖥️ Tech Stack

### Backend
- FastAPI
- FAISS
- Ollama (local LLMs)
- Python 3.11+

### Frontend
- Nuxt 3
- Vue
- REST API integration

---

## 📦 Requirements

- Python 3.11+
- Node.js (for frontend)
- Ollama installed

👉 https://ollama.com

Recommended models:
```
qwen2.5-coder
llama3.1
deepseek-coder
```

---

## ▶️ Quick Start

### 1. Clone repo
```
git clone https://github.com/DannyKuk/RepoClarity-AI
cd repoclarity
```

---

### 2. Start Backend
```
cd backend

python -m venv .venv
source .venv/bin/activate  # or Windows (.venv\Scripts\activate)

pip install -r requirements.txt
pip install -e .

uvicorn app.main:app --reload
```

Backend runs at:
http://localhost:8000

---

### 3. Start Frontend
```
cd frontend
npm install
npm run dev
```

Frontend runs at:
http://localhost:3000

---

## 💬 Usage

You can interact in **two ways**:

### 1. UI
- Open the frontend
- Index a repository
- Ask questions visually

### 2. CLI (see backend/README.md for more information)
```
repoclarity --help
repoclarity index <path> myrepo
repoclarity ask myrepo "What does this project do?"
```
---

## 🔌 API

The frontend communicates with the backend via REST.

Main endpoints:

- POST /repos/index
- POST /query/ask
- GET /repos
- GET /models

Full API docs:
http://localhost:8000/docs

---

## 📚 Documentation

- Backend → backend/README.md
- Frontend → frontend/README.md

---

## 🎯 Design Goals

- Fully local AI
- No vendor lock-in
- Fast semantic search over code
- Simple developer workflow

---

## 📄 License

MIT
