from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.services import Services

from app.api.routes_repos import router as repos_router
from app.api.routes_query import router as query_router
from app.api.routes_models import router as models_router

app = FastAPI(
    title="RepoClarity AI API",
    description="Local AI assistant for exploring repositories.",
    version="1.0.0",
)

services = Services()

app.state.services = services

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repos_router, prefix="/repos", tags=["repos"])
app.include_router(query_router, prefix="/query", tags=["query"])
app.include_router(models_router, prefix="/models", tags=["models"])


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}