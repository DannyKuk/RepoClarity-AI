from app.rag.chunker import chunk_file
from app.repo.scanner import scan_repository

repo_path = "../"

files = scan_repository(repo_path)

all_chunks = []

for file in files:
    chunks = chunk_file(file)
    all_chunks.extend(chunks)

print(f"Files: {len(files)}")
print(f"Chunks: {len(all_chunks)}")

print(all_chunks[0]["path"])