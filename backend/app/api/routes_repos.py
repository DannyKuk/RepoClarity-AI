from pathlib import Path
import shutil

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()


class IndexRepoRequest(BaseModel):
    name: str
    path: str


class RepoResponse(BaseModel):
    name: str
    path: str
    framework: str | None = None


@router.get("/", response_model=list[RepoResponse])
def get_repos(request: Request):
    services = request.app.state.services

    repos = services.registry.list()
    result = []

    for name, path in repos.items():
        index_dir = services.registry.index_dir / name

        framework = None

        if index_dir.exists():
            try:
                vector_store = services.vector_store_cls.load(index_dir)
                framework = vector_store.framework
            except Exception:
                # don't break listing if one index is corrupted
                pass

        result.append(
            RepoResponse(
                name=name,
                path=path,
                framework=framework,
            )
        )

    return result


@router.post("/index")
def index_repo(body: IndexRepoRequest, request: Request):
    services = request.app.state.services

    repo_path = Path(body.path)

    if not repo_path.exists():
        raise HTTPException(400, "Repository path does not exist")

    if not repo_path.is_dir():
        raise HTTPException(400, "Provided path is not a directory")

    try:
        vector_store = services.indexing_service.build_index(body.path)

        repo_index_dir = services.registry.index_dir / body.name
        vector_store.save(repo_index_dir)

        services.registry.register(body.name, body.path)

        return {"status": "indexed", "repo": body.name}

    except Exception as exc:
        raise HTTPException(500, f"Failed to index repository: {exc}")


@router.post("/{repo}/reindex")
def reindex_repo(repo: str, request: Request):
    services = request.app.state.services

    repo_path = services.registry.get(repo)

    if not repo_path:
        raise HTTPException(404, "Repository not registered.")

    try:
        vector_store = services.indexing_service.build_index(repo_path)

        repo_index_dir = services.registry.index_dir / repo
        vector_store.save(repo_index_dir)

        return {"status": "reindexed", "repo": repo}

    except Exception as exc:
        raise HTTPException(500, f"Failed to reindex repository: {exc}")


@router.delete("/{repo}")
def delete_repo(repo: str, request: Request):
    services = request.app.state.services

    repo_path = services.registry.get(repo)

    if not repo_path:
        raise HTTPException(404, "Repository not registered.")

    try:
        services.registry.remove(repo)

        index_dir = services.registry.index_dir / repo
        if index_dir.exists():
            shutil.rmtree(index_dir)

        return {"status": "removed", "repo": repo}

    except Exception as exc:
        raise HTTPException(500, f"Failed to remove repository: {exc}")
