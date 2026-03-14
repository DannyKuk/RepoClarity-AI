# RepoMind

Chat with any code repository locally using AI.

RepoMind indexes a repository, builds semantic embeddings of the codebase, and lets you ask natural language questions about the project.

Everything runs locally using:

- Ollama (LLM)
- FAISS (vector search)
- Sentence Transformers (embeddings)

No cloud APIs required.

---

## Features

- Index any repository
- Semantic code search
- Ask questions about the codebase
- Fully local AI pipeline
- Multi-repository support

---

## Example

```bash
repomind index ~/projects/my-api --name api
repomind ask --repo api "How does authentication work?"


python -m venv .venv