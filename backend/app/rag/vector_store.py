import faiss
import numpy as np
import pickle
from pathlib import Path


class VectorStore:

    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add(self, embeddings, docs):

        embeddings = np.array(embeddings).astype("float32")

        self.index.add(embeddings)
        self.documents.extend(docs)

    def search(self, query_embedding, k=5):

        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])

        return results

    def save(self, path):

        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(path / "index.faiss"))

        with open(path / "documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)

    def load(self, path):

        path = Path(path)

        self.index = faiss.read_index(str(path / "index.faiss"))

        with open(path / "documents.pkl", "rb") as f:
            self.documents = pickle.load(f)