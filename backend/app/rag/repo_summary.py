from app.llm.ollama_client import ask_ollama


def generate_repo_summary(files, model=None):
    """
    Generate a high-level summary of the repository.
    """

    important_files = []

    for f in files:
        path = f["path"].lower()

        if (
            "readme" in path
            or "package.json" in path
            or "nuxt.config" in path
            or "main.py" in path
        ):
            important_files.append(f)

    context = "\n\n".join(
        f"File: {f['path']}\n{f['content'][:2000]}"
        for f in important_files[:5]
    )

    prompt = f"""
        You are analyzing a software repository.
        
        Using the following key files, summarize:
        
        1. What the project is
        2. What framework or technology it uses
        3. What the user sees when starting the project
        4. The main purpose of the project
        
        Context:
        {context}
        
        Provide a concise summary.
        """

    return ask_ollama(prompt, model=model)