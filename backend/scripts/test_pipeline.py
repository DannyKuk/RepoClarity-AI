from pathlib import Path

from app.repo.scanner import scan_repository
from app.rag.chunker import chunk_file
from app.rag.embedder import embed_texts, embedding_dimension
from app.rag.vector_store import VectorStore
from app.rag.query_engine import answer_question


repo_path = "../"
index_path = "./index"

vector_store = VectorStore(embedding_dimension())

# If index exists → load it
if Path(index_path).exists():

    print("Loading existing index...")
    vector_store.load(index_path)

else:

    print("Building index...")

    files = scan_repository(repo_path)

    chunks = []

    for file in files:
        chunks.extend(chunk_file(file))

    texts = [c["content"] for c in chunks]

    embeddings = embed_texts(texts)

    vector_store.add(embeddings, chunks)

    vector_store.save(index_path)

    print("Index saved.")

while True:

    question = input("\nAsk a question (or 'exit'): ")

    if question == "exit":
        break

    answer, sources = answer_question(question, vector_store)

    print("\nAnswer:\n")
    print(answer)

    print("\nSources:")
    for s in sources:
        print("-", s)