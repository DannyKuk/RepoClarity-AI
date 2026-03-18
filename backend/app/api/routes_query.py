from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from pathlib import Path

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
def ask(body: AskRequest, request: Request):
    services = request.app.state.services

    repo_path = services.registry.get(body.repo)
    if not repo_path:
        raise HTTPException(status_code=404, detail="Repository not registered.")

    index_dir = services.registry.index_dir / body.repo
    if not index_dir.exists():
        raise HTTPException(status_code=404, detail="Repository index not found.")

    try:
        vector_store = services.vector_store_cls.load(index_dir)

        answer, sources = services.query_engine.answer(
            body.question,
            vector_store,
            model=body.model,
        )

        return AskResponse(
            answer=answer,
            sources=sources,
            framework=vector_store.framework,
            entrypoints=vector_store.entrypoints,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to answer question: {exc}",
        )
