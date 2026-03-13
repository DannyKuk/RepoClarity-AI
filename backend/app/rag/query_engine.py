from app.rag.retriever import retrieve
from app.llm.ollama_client import ask_ollama


def answer_question(question, vector_store):

    chunks = retrieve(question, vector_store, k=5)

    context = "\n\n".join(
        f"File: {chunk['path']}\n{chunk['content']}"
        for chunk in chunks
    )

    prompt = f"""
        You are an expert software engineer analyzing a codebase.
        
        Use the provided context to answer the question.
        
        Context:
        {context}
        
        Question:
        {question}
        
        Answer clearly and reference file names if possible.
        """

    answer = ask_ollama(prompt)

    sources = list({c["path"] for c in chunks})

    return answer, sources