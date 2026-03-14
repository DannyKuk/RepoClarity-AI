from app.rag.retriever import retrieve
from app.llm.ollama_client import ask_ollama


def answer_question(question, vector_store, model=None):
    chunks = retrieve(question, vector_store, k=20)

    summary = vector_store.summary or ""

    context = "\n\n".join(
        f"File: {chunk['path']}\n{chunk['content']}"
        for chunk in chunks
    )

    prompt = f"""
        You are analyzing a software repository.
    
        Use the provided context to answer the question.
    
        If the question asks about the *purpose of the project*, prefer:
    
        - README files
        - configuration files
        - project structure
    
        Ignore dependency lists unless relevant.
        
        Repository summary:
        {summary}
    
        Context:
        {context}
    
        Question:
        {question}
    
        Answer clearly.
        """

    answer = ask_ollama(prompt, model=model)
    sources = list({chunk["path"] for chunk in chunks})

    return answer, sources