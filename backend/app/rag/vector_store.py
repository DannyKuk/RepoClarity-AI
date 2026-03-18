import faiss
import numpy as np
import pickle
from pathlib import Path


class VectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
        self.summary = None
        self.framework = None
        self.entrypoints = []

    def add(self, embeddings, docs):
        if len(embeddings) != len(docs):
            raise ValueError("Embeddings and documents must have the same length")

        embeddings = np.array(embeddings).astype("float32")

        if embeddings.shape[1] != self.dimension:
            raise ValueError("Embedding dimension mismatch")

        self.index.add(embeddings)
        self.documents.extend(docs)

    def search(self, query_embedding, k=5):
        if not self.documents:
            return []

        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for idx in indices[0]:
            if 0 <= idx < len(self.documents):
                results.append(self.documents[idx])

        return results

    def save(self, path):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(path / "index.faiss"))

        with open(path / "documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)

        (path / "framework.txt").write_text(self.framework or "", encoding="utf-8")
        (path / "summary.txt").write_text(self.summary or "", encoding="utf-8")

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

        framework_file = path / "framework.txt"
        if framework_file.exists():
            store.framework = framework_file.read_text(encoding="utf-8").strip()

        summary_file = path / "summary.txt"
        if summary_file.exists():
            store.summary = summary_file.read_text(encoding="utf-8")

        entry_file = path / "entrypoints.txt"
        if entry_file.exists():
            store.entrypoints = [
                line.strip() for line in entry_file.read_text().splitlines()
            ]

        return store
