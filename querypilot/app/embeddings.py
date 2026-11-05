import math
import ollama
from app.config import EMBED_MODEL

def embed(text):
    response = ollama.embed(model=EMBED_MODEL, input=text)
    return response["embeddings"][0]

def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    len_a = math.sqrt(sum(x * x for x in a))
    len_b = math.sqrt(sum(x * x for x in b))
    if len_a == 0 or len_b == 0:
        return 0.0
    return dot_product / (len_a * len_b)

if __name__ == "__main__":
    sentences = [
        "Who must approve software purchases?",
        "Manager approval is needed for software expenses above ₹10,000.",
        "The office kitchen is cleaned every Friday."
    ]

    embeddings = [embed(s) for s in sentences]

    sim_1_2 = cosine_similarity(embeddings[0], embeddings[1])
    sim_1_3 = cosine_similarity(embeddings[0], embeddings[2])
    sim_2_3 = cosine_similarity(embeddings[1], embeddings[2])

    print(f"Similarity (1, 2): {sim_1_2:.4f}")
    print(f"Similarity (1, 3): {sim_1_3:.4f}")
    print(f"Similarity (2, 3): {sim_2_3:.4f}")
