from app.repo.scanner import scan_repository
from app.rag.chunker import chunk_file
from app.rag.embedder import embed_texts, embedding_dimension
from app.rag.vector_store import VectorStore
from app.rag.repo_summary import generate_repo_summary


def build_index(repo_path: str) -> VectorStore:
    """
    Build a vector index for a repository.
    """

    print("Scanning repository...")
    files = scan_repository(repo_path)
    print(f"Files found: {len(files)}")

    if not files:
        raise RuntimeError("No files found to index.")

    print("Generating repository summary...")
    summary = generate_repo_summary(files)

    print("Chunking files...")
    chunks = []

    for file in files:
        file_chunks = chunk_file(file)

        # skip empty chunk results
        if file_chunks:
            chunks.extend(file_chunks)

    print(f"Chunks generated: {len(chunks)}")

    if not chunks:
        raise RuntimeError("No chunks generated. Scanner may be filtering too aggressively.")

    # remove empty text chunks
    chunks = [c for c in chunks if c["content"].strip()]

    texts = [chunk["content"] for chunk in chunks]

    print("Generating embeddings...")
    embeddings = embed_texts(texts)

    print("Building vector store...")
    vector_store = VectorStore(embedding_dimension())
    vector_store.summary = summary
    vector_store.add(embeddings, chunks)

    print("Index built successfully.")

    return vector_store