from app.rag.embedder import embed_texts


def retrieve(query: str, vector_store, k=5):

    query_embedding = embed_texts([query])[0]

    results = vector_store.search(query_embedding, k=k)

    return results