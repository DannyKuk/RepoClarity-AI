from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.embedder import embedding_dimension
from app.rag.query_engine import answer_question
from app.rag.vector_store import VectorStore
from app.repo.repo_registry import INDEX_DIR, get_repo

router = APIRouter()


class AskRequest(BaseModel):
    repo: str
    question: str
    model: str | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    framework: str | None = None
    entrypoints: list[str] = []


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """
    Ask a question about an indexed repository.
    """

    repo_path = get_repo(request.repo)
    if not repo_path:
        raise HTTPException(status_code=404, detail="Repository not registered.")

    index_dir = INDEX_DIR / request.repo
    if not index_dir.exists():
        raise HTTPException(status_code=404, detail="Repository index not found.")

    try:
        vector_store = VectorStore(embedding_dimension())
        vector_store.load(index_dir)

        answer, sources = answer_question(
            request.question,
            vector_store,
            model=request.model,
        )

        return AskResponse(
            answer=answer,
            sources=sources,
            framework=vector_store.framework,
            entrypoints=vector_store.entrypoints,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {exc}")
