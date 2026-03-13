import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension: int):
        """
        Initialize FAISS index.
        """
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add(self, embeddings, docs):
        """
        Add embeddings + metadata.
        """

        embeddings = np.array(embeddings).astype("float32")

        self.index.add(embeddings)
        self.documents.extend(docs)

    def search(self, query_embedding, k=5):
        """
        Search most similar chunks.
        """

        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for idx in indices[0]:
            results.append(self.documents[idx])

        return results