import shutil
from typing import Optional

import typer
from rich import print
from rich.prompt import Prompt

from app.core.services import Services

app = typer.Typer(help="RepoClarity CLI - chat with a codebase locally")

services = Services()


@app.command()
def index(repo_path: str, name: str):
    print(f"[bold blue]Indexing repository:[/bold blue] {repo_path}")

    vector_store = services.indexing_service.build_index(repo_path)

    repo_index_dir = services.registry.index_dir / name
    vector_store.save(repo_index_dir)

    services.registry.register(name, repo_path)

    print(f"[bold green]Repository indexed as:[/bold green] {name}")


@app.command()
def ask(
        repo: str,
        question: Optional[str] = typer.Argument(None),
        model: Optional[str] = typer.Option(None, "--model", "-m"),
):
    repo_path = services.registry.get(repo)

    if not repo_path:
        print(f"[bold red]Repo '{repo}' not registered.[/bold red]")
        raise typer.Exit(code=1)

    index_dir = services.registry.index_dir / repo

    if not index_dir.exists():
        print(f"[bold red]Repo '{repo}' not indexed.[/bold red]")
        raise typer.Exit(code=1)

    vector_store = services.vector_store_cls.load(index_dir)

    model_name = model or services.llm.default_model

    if question:
        answer, sources = services.query_engine.answer(
            question,
            vector_store,
            model=model,
        )

        print("\n[bold cyan]Question:[/bold cyan]")
        print(question)

        print(f"\n[bold green]Answer[/bold green] [dim]({model_name})[/dim]:")
        print(answer)

        print("\n[bold magenta]Sources:[/bold magenta]")
        for s in sources:
            print(f"- {s}")
        return

    # --- interactive ---
    print(f"[bold blue]RepoClarity chat[/bold blue] ([bold]{repo}[/bold])")
    print(f"[bold blue]Model:[/bold blue] {model_name}")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "q"}:
            print("Bye.")
            break

        answer, sources = services.query_engine.answer(
            user_input,
            vector_store,
            model=model,
        )

        print(f"\n[bold green]RepoClarity[/bold green] [dim]({model_name})[/dim]:")
        print(answer)

        print("\n[bold magenta]Sources:[/bold magenta]")
        for s in sources:
            print(f"- {s}")

        print()


@app.command()
def repos():
    repos_list = services.registry.list()

    if not repos_list:
        print("[bold red]No repositories indexed.[/bold red]")
        return

    print("[bold blue]Indexed repositories:[/bold blue]")

    for name, path in repos_list.items():
        print(f"- {name}: {path}")


@app.command()
def reindex(repo: str):
    repo_path = services.registry.get(repo)

    if not repo_path:
        print(f"[bold red]Repository '{repo}' not registered.[/bold red]")
        raise typer.Exit(code=1)

    print(f"[bold blue]Reindexing repository:[/bold blue] {repo}")

    vector_store = services.indexing_service.build_index(repo_path)

    repo_index_dir = services.registry.index_dir / repo
    vector_store.save(repo_index_dir)

    print("[bold green]Index updated.[/bold green]")


@app.command()
def remove(repo: str):
    repo_path = services.registry.get(repo)

    if not repo_path:
        print(f"[bold red]Repository '{repo}' not registered.[/bold red]")
        raise typer.Exit(code=1)

    print(f"[bold yellow]Removing repository:[/bold yellow] {repo}")

    services.registry.remove(repo)

    index_dir = services.registry.index_dir / repo
    if index_dir.exists():
        shutil.rmtree(index_dir)

    print("[bold green]Repository removed.[/bold green]")


@app.command()
def models():
    try:
        models = services.llm.list_models()

        print("[bold blue]Available Ollama models:[/bold blue]\n")
        for m in models:
            print(m)

    except Exception as exc:
        print("[bold red]Failed to list models.[/bold red]")
        print(exc)


if __name__ == "__main__":
    app()