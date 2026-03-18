import logging
import os
from sentence_transformers import SentenceTransformer

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)

os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"


class Embedder:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5", model=None):
        self._model_name = model_name
        self._model = model  # allows injection for tests

    def _get_model(self):
        if self._model is None:
            self._model = SentenceTransformer(self._model_name)
        return self._model

    def embed(self, texts, batch_size: int = 128):
        if not texts:
            return []

        model = self._get_model()

        return model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    def dimension(self):
        model = self._get_model()
        return model.get_sentence_embedding_dimension()
