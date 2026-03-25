class Retriever:
    def __init__(self, embedder):
        self.embedder = embedder

    def deduplicate(self, docs):
        seen = set()
        unique = []

        for doc in docs:
            path = doc.get("metadata", {}).get("path")

            if path not in seen:
                unique.append(doc)
                seen.add(path)

        return unique

    def rewrite_query(self, query: str) -> str:
        query = query.strip()

        # simple heuristic rewrite for vague queries
        if len(query.split()) < 3:
            return f"Where is {query} implemented in this codebase?"

        return query

    def rerank(self, query: str, docs):
        query_terms = set(query.lower().split())

        scored = []

        for doc in docs:
            content = doc.get("content", "").lower()
            path = doc.get("metadata", {}).get("path", "").lower()

            filename = path.split("\\")[-1]  # Windows-safe

            score = 0

            # STRONG filename match (priority)
            if any(term in filename for term in query_terms):
                score += 10

            # path match (medium)
            if any(term in path for term in query_terms):
                score += 5

            # content match (weak)
            overlap = sum(1 for term in query_terms if term in content)
            score += overlap

            scored.append((score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [doc for _, doc in scored]

    def retrieve(self, query: str, vector_store, k: int = 5):
        # rewrite query
        rewritten_query = self.rewrite_query(query)

        # embed rewritten query
        query_embedding = self.embedder.embed([rewritten_query])[0]

        # hybrid retrieval (semantic + keyword)
        candidates = vector_store.search_hybrid(
            rewritten_query,
            query_embedding,
            k=k * 2,
        )

        # rerank
        ranked = self.rerank(query, candidates)
        ranked = self.deduplicate(ranked)

        # return top-k
        return ranked[:k]