import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
SIMILARITY_THRESHOLD = 0.8


def generate_embedding(text: str) -> str:
    """Converts prompt text into a stringified JSON list of floats."""
    embedding = model.encode(text)
    return str(embedding.tolist())


def calculate_similarity(embedding_a: str, embedding_b: str) -> float:
    """Calculates cosine similarity between two stringified embeddings."""
    vec_a = np.array(eval(embedding_a))
    vec_b = np.array(eval(embedding_b))

    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)

    return dot_product / (norm_a * norm_b)
