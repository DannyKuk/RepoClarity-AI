import logging
from sentence_transformers import SentenceTransformer

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):
    return model.encode(texts)


def embedding_dimension():
    return model.get_sentence_embedding_dimension()