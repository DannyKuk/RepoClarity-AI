import logging
import os
from sentence_transformers import SentenceTransformer

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)

os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def embed_texts(texts, batch_size: int = 128):
    if not texts:
        return []

    return model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )


def embedding_dimension():
    return model.get_sentence_embedding_dimension()