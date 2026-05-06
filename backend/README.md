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
* Hybrid retrieval (semantic + keyword)
* File-aware reranking for improved accuracy
* Local LLM support via LM Studio
* Language detection (Python, Typescript, etc.)
* Framework detection (Unity, Nuxt, FastAPI, etc.)
* Entrypoint detection
* Repository summaries
* CLI for local usage
* REST API for frontend integration

---

## Requirements

* Python **3.11+**
* **LM Studio** installed and running on port 1234
* A supported embedding model (downloaded automatically)

Recommended models:

```
Meta-Llama-3.1-8B-Instruct-GGUF
Qwen2.5-Coder-7B-Instruct-GGUF
```

Install LM Studio:

https://lmstudio.ai

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
repoclarity ask <repo> "Explain the project" --model Meta-Llama-3.1-8B-Instruct-GGUF
```

---

### List installed LM Studio models

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
  "model": "Meta-Llama-3.1-8B-Instruct-GGUF"
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
 ├ llm/            # LM Studio integration
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
chunk code (with metadata: path + positions)
↓
generate embeddings
↓
store vectors in FAISS
↓
rewrite query
↓
hybrid retrieval (semantic + keyword)
↓
rerank results (file-aware ranking)
↓
select top-k chunks
↓
generate answer with LLM
```

---

## Retrieval Improvements

The retrieval system uses a hybrid approach to improve accuracy and reduce noise:

### Hybrid Search
Combines:
- semantic vector search (FAISS)
- keyword-based matching (file paths + content)

This ensures both:
- conceptual understanding
- exact file matching

---
### Query Rewriting
Short or vague queries are automatically expanded before retrieval.

Example:
auth → Where is auth implemented in this codebase?

---

### Reranking
Retrieved chunks are re-ranked using file-aware heuristics:

- filename matches (strong signal)
- file path matches (medium signal)
- content matches (weak signal)

This prioritizes the most relevant files over loosely related ones.

---

### Metadata-Aware Chunks
Each chunk includes:

- file path
- start/end position

This enables:
- better ranking
- traceability of results

---

## Development Notes

The backend is designed to be:

* modular
* framework-agnostic
* usable via CLI or API

The frontend will interact with the API layer only.

Retrieval quality is continuously evaluated using an internal benchmarking script
based on precision@k and relevance scoring.