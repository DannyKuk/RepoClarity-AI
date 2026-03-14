import shutil
from pathlib import Path

import typer
from rich import print
from rich.prompt import Prompt

from app.rag.indexing_service import build_index
from app.rag.embedder import embedding_dimension
from app.rag.vector_store import VectorStore
from app.rag.query_engine import answer_question
from app.repo.repo_registry import register_repo, INDEX_DIR, list_repos, get_repo, remove_repo

app = typer.Typer(help="RepoMind CLI - chat with a codebase locally")

DEFAULT_INDEX_DIR = Path("./index")


@app.command()
def index(repo_path: str, name: str):
    """
    Index a repository and register it.
    """

    print(f"[bold blue]Indexing repository:[/bold blue] {repo_path}")

    vector_store = build_index(repo_path)

    repo_index_dir = INDEX_DIR / name

    vector_store.save(repo_index_dir)

    register_repo(name, repo_path)

    print(f"[bold green]Repository indexed as:[/bold green] {name}")


@app.command()
def ask(repo: str, question: str | None = None):
    """
    Ask a question about an indexed repository.

    If no question is provided, start interactive chat mode.
    """

    index_dir = INDEX_DIR / repo

    if not index_dir.exists():
        print(f"[bold red]Repo '{repo}' not indexed.[/bold red]")
        raise typer.Exit(code=1)

    vector_store = VectorStore(embedding_dimension())
    vector_store.load(index_dir)

    if question is not None:
        answer, sources = answer_question(question, vector_store)

        print("\n[bold cyan]Question:[/bold cyan]")
        print(question)

        print("\n[bold green]Answer:[/bold green]")
        print(answer)

        print("\n[bold magenta]Sources:[/bold magenta]")
        for source in sources:
            print(f"- {source}")

        return

    print(f"[bold blue]RepoMind chat[/bold blue] ([bold]{repo}[/bold])")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "q"}:
            print("Bye.")
            break

        answer, sources = answer_question(user_input, vector_store)

        print("\n[bold green]RepoMind:[/bold green]")
        print(answer)

        print("\n[bold magenta]Sources:[/bold magenta]")
        for source in sources:
            print(f"- {source}")

        print()

@app.command()
def repos():
    """
    List all indexed repositories.
    """

    repos_list = list_repos()

    if not repos_list:
        print("[bold red]No repositories indexed.[/bold red]")
        return

    print("[bold blue]Indexed repositories:[/bold blue]")

    for name, path in repos_list.items():
        print(f"- {name}: {path}")

@app.command()
def reindex(repo: str):
    """
    Rebuild the index for an already registered repository.
    """

    repo_path = get_repo(repo)

    if not repo_path:
        print(f"[bold red]Repository '{repo}' not registered.[/bold red]")
        raise typer.Exit(code=1)

    print(f"[bold blue]Reindexing repository:[/bold blue] {repo}")

    vector_store = build_index(repo_path)

    repo_index_dir = INDEX_DIR / repo

    vector_store.save(repo_index_dir)

    print("[bold green]Index updated.[/bold green]")

@app.command()
def remove(repo: str):
    """
    Remove an indexed repository.
    """

    index_dir = INDEX_DIR / repo

    if not index_dir.exists():
        print(f"[bold red]Repo '{repo}' not found.[/bold red]")
        raise typer.Exit(code=1)

    print(f"[bold yellow]Removing repository:[/bold yellow] {repo}")

    # remove FAISS index directory
    shutil.rmtree(index_dir)

    # remove registry entry
    remove_repo(repo)

    print("[bold green]Repository removed.[/bold green]")

if __name__ == "__main__":
    app()