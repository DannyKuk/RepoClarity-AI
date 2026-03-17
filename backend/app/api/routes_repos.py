from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.indexing_service import build_index
from app.repo.repo_registry import (
    register_repo,
    list_repos,
    get_repo,
    remove_repo,
    INDEX_DIR,
)

router = APIRouter()


class IndexRepoRequest(BaseModel):
    name: str
    path: str


class RepoResponse(BaseModel):
    name: str
    path: str
    framework: str | None = None


@router.get("/", response_model=list[RepoResponse])
def get_repos():
    repos = list_repos()

    result = []

    for name, path in repos.items():
        framework_file = INDEX_DIR / name / "framework.txt"

        framework = None
        if framework_file.exists():
            try:
                content = framework_file.read_text().strip()
                framework = content or None
            except Exception:
                pass

        result.append(
            RepoResponse(
                name=name,
                path=path,
                framework=framework
            )
        )

    return result


@router.post("/index")
def index_repo(request: IndexRepoRequest):
    """
    Index a repository and register it.
    """

    repo_path = Path(request.path)

    if not repo_path.exists():
        raise HTTPException(
            status_code=400,
            detail="Repository path does not exist"
        )

    if not repo_path.is_dir():
        raise HTTPException(
            status_code=400,
            detail="Provided path is not a directory"
        )

    try:
        vector_store = build_index(request.path)

        repo_index_dir = INDEX_DIR / request.name
        vector_store.save(repo_index_dir)

        register_repo(request.name, request.path)

        return {"status": "indexed", "repo": request.name}

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to index repository: {exc}"
        )


@router.post("/{repo}/reindex")
def reindex_repo(repo: str):
    """
    Rebuild the index for an existing repository.
    """

    repo_path = get_repo(repo)

    if not repo_path:
        raise HTTPException(status_code=404, detail="Repository not registered.")

    try:
        vector_store = build_index(repo_path)

        repo_index_dir = INDEX_DIR / repo
        vector_store.save(repo_index_dir)

        return {"status": "reindexed", "repo": repo}

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reindex repository: {exc}"
        )


@router.delete("/{repo}")
def delete_repo(repo: str):
    """
    Remove an indexed repository.
    """

    repo_path = get_repo(repo)

    if not repo_path:
        raise HTTPException(status_code=404, detail="Repository not registered.")

    try:
        remove_repo(repo)

        index_dir = INDEX_DIR / repo
        if index_dir.exists():
            import shutil
            shutil.rmtree(index_dir)

        return {"status": "removed", "repo": repo}

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to remove repository: {exc}"
        )
