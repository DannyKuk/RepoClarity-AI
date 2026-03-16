# RepoMind Backend

RepoMind is a **local AI assistant for exploring code repositories**.
It indexes a repository, builds a semantic vector index, and lets you **ask questions about the codebase** using local
LLMs via **Ollama**.

The backend provides:

* a **CLI** for indexing and querying repositories
* a **FastAPI server** for frontend integrations
* a **RAG pipeline** (scan → chunk → embed → retrieve → LLM)

Everything runs **locally**.

---

# Features

* Repository indexing with semantic embeddings
* FAISS vector search
* Local LLM support via Ollama
* Framework detection (Unity, Nuxt, FastAPI, etc.)
* Entrypoint detection
* Repository summaries
* CLI for local usage
* REST API for frontend integration

---

# Requirements

* Python **3.11+**
* **Ollama** installed
* A supported embedding model (downloaded automatically)

Recommended models:

```
qwen2.5-coder
llama3.1
deepseek-coder
```

Install Ollama:

https://ollama.com

---

# Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the backend as an editable package:

```bash
pip install -e .
```

---

# Running the API server

Start the backend server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://localhost:8000
```

Interactive API docs:

```
http://localhost:8000/docs
```

Health check:

```
GET /health
```

---

# CLI Usage

RepoMind also provides a CLI for local interaction.

## List indexed repositories

```bash
repomind repos
```

---

## Index a repository

```bash
repomind index <path> --name <repo-name>
```

Example:

```bash
repomind index "C:\projects\klyra" --name klyra
```

---

## Ask a question

```bash
repomind ask <repo> "question"
```

Example:

```bash
repomind ask klyra "What does this project do?"
```

---

## Interactive mode

```bash
repomind ask <repo>
```

Example:

```bash
repomind ask klyra
```

Then ask questions interactively:

```
You: What framework does this project use?
You: How does the app start?
```

Exit with:

```
exit
```

---

## Select a model

You can override the default LLM:

```bash
repomind ask klyra "Explain the project" --model qwen2.5-coder
```

---

## List installed Ollama models

```bash
repomind models
```

---

## Reindex a repository

```bash
repomind reindex <repo>
```

Example:

```bash
repomind reindex klyra
```

---

## Remove a repository

```bash
repomind remove <repo>
```

Example:

```bash
repomind remove klyra
```

---

# API Endpoints

### Health

```
GET /health
```

---

### List repositories

```
GET /repos
```

---

### Index repository

```
POST /repos/index
```

Body:

```json
{
  "name": "klyra",
  "path": "C:/projects/klyra"
}
```

---

### Reindex repository

```
POST /repos/{repo}/reindex
```

---

### Remove repository

```
DELETE /repos/{repo}
```

---

### Ask a question

```
POST /query/ask
```

Body:

```json
{
  "repo": "klyra",
  "question": "What does this project do?",
  "model": "qwen2.5-coder"
}
```

---

### List models

```
GET /models
```

---

# Project Structure

```
app/
 ├ api/            # FastAPI routes
 ├ cli/            # CLI commands
 ├ llm/            # Ollama integration
 ├ rag/            # Retrieval Augmented Generation pipeline
 ├ repo/           # Repository utilities
 └ main.py         # FastAPI entrypoint
```

---

# RAG Pipeline

RepoMind uses a standard RAG architecture:

```
scan repository
↓
filter irrelevant files
↓
chunk code
↓
generate embeddings
↓
store vectors in FAISS
↓
retrieve relevant chunks
↓
generate answer with LLM
```

---

# Development Notes

The backend is designed to be:

* modular
* framework-agnostic
* usable via CLI or API

The frontend will interact with the API layer only.

---

# License

MIT
