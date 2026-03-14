import logging
import os
from sentence_transformers import SentenceTransformer

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)

os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

model = SentenceTransformer("BAAI/bge-base-en-v1.5")


def embed_texts(texts):
    return model.encode(texts)


def embedding_dimension():
    return model.get_sentence_embedding_dimension()