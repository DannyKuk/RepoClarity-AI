from pathlib import Path

import typer
from rich import print

from app.rag.indexing_service import build_index
from app.rag.embedder import embedding_dimension
from app.rag.vector_store import VectorStore
from app.rag.query_engine import answer_question

app = typer.Typer(help="RepoMind CLI - chat with a codebase locally")

DEFAULT_INDEX_DIR = Path("./index")


@app.command()
def index(repo_path: str, index_dir: str = str(DEFAULT_INDEX_DIR)):
    """
    Scan a repository, build embeddings, and persist the index.
    """
    print(f"[bold blue]Indexing repository:[/bold blue] {repo_path}")

    vector_store = build_index(repo_path)
    vector_store.save(index_dir)

    print(f"[bold green]Index saved to:[/bold green] {index_dir}")


@app.command()
def ask(question: str, index_dir: str = str(DEFAULT_INDEX_DIR)):
    """
    Ask a question against an existing persisted index.
    """
    index_path = Path(index_dir)

    if not index_path.exists():
        print("[bold red]No index found.[/bold red] Run `repomind index <repo_path>` first.")
        raise typer.Exit(code=1)

    vector_store = VectorStore(embedding_dimension())
    vector_store.load(index_dir)

    answer, sources = answer_question(question, vector_store)

    print("\n[bold cyan]Question:[/bold cyan]")
    print(question)

    print("\n[bold green]Answer:[/bold green]")
    print(answer)

    print("\n[bold magenta]Sources:[/bold magenta]")
    for source in sources:
        print(f"- {source}")


if __name__ == "__main__":
    app()