import faiss
import numpy as np
import pickle
from pathlib import Path


class VectorStore:

    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
        self.summary = None
        self.framework = None

    def add(self, embeddings, docs):
        """
        Add embeddings and associated documents.
        """

        embeddings = np.array(embeddings).astype("float32")

        self.index.add(embeddings)
        self.documents.extend(docs)

    def search(self, query_embedding, k=5):
        """
        Search the vector store for the nearest documents.
        """

        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])

        return results

    def save(self, path):
        """
        Persist the FAISS index, documents, and summary.
        """

        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        # Save FAISS index
        faiss.write_index(self.index, str(path / "index.faiss"))

        # Save documents metadata
        with open(path / "documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)

        with open(path / "framework.txt", "w", encoding="utf-8") as f:
            f.write(self.framework or "")

        # Save summary
        with open(path / "summary.txt", "w", encoding="utf-8") as f:
            f.write(self.summary or "")

    def load(self, path):
        """
        Load the FAISS index, documents, and summary.
        """

        path = Path(path)

        # Load FAISS index
        self.index = faiss.read_index(str(path / "index.faiss"))

        # Load documents
        documents_file = path / "documents.pkl"
        if documents_file.exists():
            with open(documents_file, "rb") as f:
                self.documents = pickle.load(f)

        framework_file = path / "framework.txt"
        if framework_file.exists():
            with open(framework_file, "r", encoding="utf-8") as f:
                self.framework = f.read().strip()

        # Load summary
        summary_file = path / "summary.txt"
        if summary_file.exists():
            with open(summary_file, "r", encoding="utf-8") as f:
                self.summary = f.read()