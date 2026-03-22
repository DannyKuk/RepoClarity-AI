import faiss
import numpy as np
import pickle
from pathlib import Path


class VectorStore:
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
                doc = dict(self.documents[idx])  # shallow copy
                doc["_score"] = float(dist)
                results.append(doc)

        return results

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