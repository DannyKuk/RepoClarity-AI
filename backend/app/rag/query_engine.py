from app.rag.retriever import retrieve
from app.llm.ollama_client import ask_ollama


def answer_question(question, vector_store, model=None):
    """
    Answer a question about the indexed repository.
    """

    # Retrieve the most relevant chunks
    chunks = retrieve(question, vector_store, k=20)

    framework = vector_store.framework or "unknown"
    summary = vector_store.summary or ""

    # Build context but limit chunk size to avoid huge prompts
    context = "\n\n".join(
        f"File: {chunk['path']}\n{chunk['content'][:800]}"
        for chunk in chunks
    )

    # Detect high-level project questions
    if is_overview_question(question):
        prompt = f"""
            You are analyzing a software repository.
            
            Detected framework: {framework}

            Repository summary:
            {summary}

            Relevant repository context:
            {context}

            The user asked a high-level question about the project.

            Explain the purpose of the project, what the application does,
            and how it works at a high level.

            Question:
            {question}

            Answer clearly.
            """
    else:
        prompt = f"""
            You are analyzing a software repository.
            
            Detected framework: {framework}
            
            Repository summary:
            {summary}
            
            Relevant repository context:
            {context}
            
            Use the provided information to answer the question.
            
            Question:
            {question}
            
            Answer clearly and reference the code structure when helpful.
            """

    answer = ask_ollama(prompt, model=model)

    # Remove duplicate source paths
    sources = sorted({chunk["path"] for chunk in chunks})

    return answer, sources


def is_overview_question(question: str) -> bool:
    """
    Detect questions about the overall project rather than specific code.
    """

    q = question.lower()

    keywords = {
        "what is this project",
        "what does this project",
        "what does the app",
        "what is the app",
        "what does it do",
        "what happens when",
        "how does it start",
        "what framework",
        "what is this repository",
        "what does this repo",
    }

    return any(k in q for k in keywords)
