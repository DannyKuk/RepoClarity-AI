from app.repo.scanner import scan_repository
from app.rag.chunker import chunk_file
from app.rag.embedder import embed_texts

repo_path = "../"

files = scan_repository(repo_path)

chunks = []

for file in files:
    chunks.extend(chunk_file(file))

texts = [c["content"] for c in chunks]

embeddings = embed_texts(texts)

print("Files:", len(files))
print("Chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)