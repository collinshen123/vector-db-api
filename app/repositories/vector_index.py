import numpy as np
from app.models.chunk import Chunk
from typing import List
import random


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def knn_search(chunks: List[Chunk], query_embedding: List[float], k: int = 5) -> List[Chunk]:
    scored_chunks = [
        (chunk, cosine_similarity(query_embedding, chunk.embedding))
        for chunk in chunks
    ]
    # Sort by similarity (high to low), return top-k
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    return [chunk for chunk, _ in scored_chunks[:k]]

def centroid_based_search(
    chunks: List[Chunk], query_embedding: List[float], k: int = 5, num_clusters: int = 2
) -> List[Chunk]:
    if len(chunks) <= num_clusters:
        return knn_search(chunks, query_embedding, k)  # fallback

    # Step 1: randomly assign chunks to clusters (simplified)
    clusters = [[] for _ in range(num_clusters)]
    for chunk in chunks:
        idx = random.randint(0, num_clusters - 1)
        clusters[idx].append(chunk)

    # Step 2: compute centroids
    centroids = []
    for cluster in clusters:
        if not cluster:
            centroids.append([0.0] * len(query_embedding))
            continue
        vectors = [np.array(c.embedding) for c in cluster]
        centroid = np.mean(vectors, axis=0)
        centroids.append(centroid)

    # Step 3: find closest centroid
    query_vec = np.array(query_embedding)
    best_cluster_idx = max(
        range(len(centroids)),
        key=lambda i: np.dot(query_vec, centroids[i]) / (np.linalg.norm(query_vec) * np.linalg.norm(centroids[i]) + 1e-8)
    )

    # Step 4: search only in that cluster
    return knn_search(clusters[best_cluster_idx], query_embedding, k)

