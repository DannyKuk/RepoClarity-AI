# RepoClarity AI Backend

The backend provides:

* a **CLI** for indexing and querying repositories
* a **FastAPI server** for frontend integrations
* a **RAG pipeline** (scan → chunk → embed → retrieve → LLM)

Everything runs **locally**.

---

## Features

* Repository indexing with semantic embeddings
* FAISS vector search
* Local LLM support via Ollama
* Framework detection (Unity, Nuxt, FastAPI, etc.)
* Entrypoint detection
* Repository summaries
* CLI for local usage
* REST API for frontend integration

---

## Requirements

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

## Setup

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

## Running the API server

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

## CLI Usage

RepoClarity AI also provides a CLI for local interaction.

### List indexed repositories

```bash
repoclarity repos
```

---

### Index a repository

```bash
repoclarity index <path> --name <repo-name>
```

Example:

```bash
repoclarity index "C:\projects\website" --name website
```

---

### Ask a question

```bash
repoclarity ask <repo> "question"
```

Example:

```bash
repoclarity ask website "What does this project do?"
```

---

### Interactive mode

```bash
repoclarity ask <repo>
```

Example:

```bash
repoclarity ask website
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

### Select a model

You can override the default LLM:

```bash
repoclarity ask <repo> "Explain the project" --model qwen2.5-coder
```

---

### List installed Ollama models

```bash
repoclarity models
```

---

### Reindex a repository

```bash
repoclarity reindex <repo>
```

Example:

```bash
repoclarity reindex website
```

---

### Remove a repository

```bash
repoclarity remove <repo>
```

Example:

```bash
repoclarity remove website
```

---

## API Endpoints

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
  "name": "website",
  "path": "C:/projects/website"
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
  "repo": "website",
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

## Project Structure

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

## RAG Pipeline

RepoClarity AI uses a standard RAG architecture:

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

## Development Notes

The backend is designed to be:

* modular
* framework-agnostic
* usable via CLI or API

The frontend will interact with the API layer only.

