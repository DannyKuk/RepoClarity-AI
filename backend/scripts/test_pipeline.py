from app.repo.scanner import scan_repository
from app.rag.chunker import chunk_file
from app.rag.embedder import embed_texts, embedding_dimension
from app.rag.vector_store import VectorStore


repo_path = "../"

files = scan_repository(repo_path)

chunks = []

for file in files:
    chunks.extend(chunk_file(file))

texts = [c["content"] for c in chunks]

embeddings = embed_texts(texts)

vector_store = VectorStore(embedding_dimension())

vector_store.add(embeddings, chunks)

print("Files:", len(files))
print("Chunks:", len(chunks))

query = "scan repository files"

query_embedding = embed_texts([query])[0]

results = vector_store.search(query_embedding, k=5)

print("\nSearch results:")
for r in results:
    print(r["path"])