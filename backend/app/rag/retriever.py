class Retriever:
    def __init__(self, embedder):
        self.embedder = embedder

    def retrieve(self, query: str, vector_store, k: int = 5):
        query_embedding = self.embedder.embed([query])[0]
        return vector_store.search(query_embedding, k=k)
