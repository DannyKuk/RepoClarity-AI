from app.repo.scanner import scan_repository
from app.rag.chunker import chunk_file
from app.rag.embedder import embed_texts, embedding_dimension
from app.rag.vector_store import VectorStore
from app.rag.query_engine import answer_question


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