from app.repo.scanner import scan_repository
from app.rag.chunker import chunk_file
from app.rag.embedder import embed_texts, embedding_dimension
from app.rag.vector_store import VectorStore
from app.rag.repo_summary import generate_repo_summary


def build_index(repo_path: str) -> VectorStore:
    files = scan_repository(repo_path)
    summary = generate_repo_summary(files)

    chunks = []
    for file in files:
        chunks.extend(chunk_file(file))

    texts = [chunk["content"] for chunk in chunks]
    embeddings = embed_texts(texts)

    vector_store = VectorStore(embedding_dimension())
    vector_store.summary = summary
    vector_store.add(embeddings, chunks)

    return vector_store