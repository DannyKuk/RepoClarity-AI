import faiss
import numpy as np
import pickle
from pathlib import Path


class VectorStore:
    STOPWORDS = {"the", "is", "in", "at", "of", "and", "to", "a"}

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)

        self.documents = []

        # Repo-level metadata
        self.summary = None
        self.languages = []
        self.framework = None
        self.entrypoints = []

    def add(self, embeddings, docs):
        if len(embeddings) != len(docs):
            raise ValueError("Embeddings and documents must have the same length")

        embeddings = np.array(embeddings).astype("float32")

        if embeddings.ndim != 2 or embeddings.shape[1] != self.dimension:
            raise ValueError("Embedding dimension mismatch")

        # Normalize for cosine similarity via L2
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.documents.extend(docs)

    def search(self, query_embedding, k=5):
        if not self.documents:
            return []

        k = min(k, len(self.documents))

        query_embedding = np.array([query_embedding]).astype("float32")
        faiss.normalize_L2(query_embedding)

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for dist, idx in zip(distances[0], indices[0]):
            if 0 <= idx < len(self.documents):
                doc = dict(self.documents[idx])
                doc["_score"] = float(dist)
                results.append(doc)

        return results

    def search_keyword(self, query: str, k: int = 5):
        if not self.documents:
            return []

        query_terms = [
            term for term in query.lower().split()
            if term not in self.STOPWORDS and len(term) > 2
        ]

        scored = []

        for doc in self.documents:
            content = doc.get("content", "").lower()
            path = doc.get("metadata", {}).get("path", "").lower()

            filename = path.replace("\\", "/").split("/")[-1]

            score = 0

            # 🔥 STRONG filename match (key change)
            for term in query_terms:
                if term in filename:
                    score += 10

            # medium: path match
            for term in query_terms:
                if term in path:
                    score += 5

            # weak: content match
            score += sum(1 for term in query_terms if term in content)

            if score > 0:
                doc_copy = dict(doc)
                doc_copy["_keyword_score"] = score
                scored.append((score, doc_copy))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [doc for _, doc in scored[:k]]

    def _get_doc_id(self, doc):
        return doc.get("id") or (
            doc.get("metadata", {}).get("path", "")
            + str(doc.get("metadata", {}).get("start", ""))
        )

    def search_hybrid(self, query: str, query_embedding, k: int = 5):
        semantic_results = self.search(query_embedding, k=k)
        keyword_results = self.search_keyword(query, k=k)

        combined = []
        seen = set()

        # interleave results (better balance)
        for i in range(max(len(semantic_results), len(keyword_results))):
            if i < len(semantic_results):
                doc = semantic_results[i]
                doc_id = self._get_doc_id(doc)
                if doc_id not in seen:
                    combined.append(doc)
                    seen.add(doc_id)

            if i < len(keyword_results):
                doc = keyword_results[i]
                doc_id = self._get_doc_id(doc)
                if doc_id not in seen:
                    combined.append(doc)
                    seen.add(doc_id)

        return combined[:k]

    def save(self, path):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        # Save FAISS index
        faiss.write_index(self.index, str(path / "index.faiss"))

        with open(path / "documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)

        # Save metadata
        (path / "languages.txt").write_text(
            "\n".join(self.languages), encoding="utf-8"
        )

        (path / "framework.txt").write_text(
            self.framework or "", encoding="utf-8"
        )

        (path / "summary.txt").write_text(
            self.summary or "", encoding="utf-8"
        )

        with open(path / "entrypoints.txt", "w", encoding="utf-8") as f:
            for ep in self.entrypoints:
                f.write(ep + "\n")

    @classmethod
    def load(cls, path):
        path = Path(path)

        index = faiss.read_index(str(path / "index.faiss"))
        dimension = index.d

        store = cls(dimension)
        store.index = index

        documents_file = path / "documents.pkl"
        if documents_file.exists():
            with open(documents_file, "rb") as f:
                store.documents = pickle.load(f)

        languages_file = path / "languages.txt"
        if languages_file.exists():
            store.languages = [
                line.strip()
                for line in languages_file.read_text().splitlines()
                if line.strip()
            ]

        framework_file = path / "framework.txt"
        if framework_file.exists():
            store.framework = framework_file.read_text(
                encoding="utf-8"
            ).strip()

        summary_file = path / "summary.txt"
        if summary_file.exists():
            store.summary = summary_file.read_text(encoding="utf-8")

        entry_file = path / "entrypoints.txt"
        if entry_file.exists():
            store.entrypoints = [
                line.strip()
                for line in entry_file.read_text().splitlines()
                if line.strip()
            ]

        return store