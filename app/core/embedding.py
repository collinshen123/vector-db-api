from sentence_transformers import SentenceTransformer
from typing import List

# Load the model once when the module is imported
# This avoids reloading the model on every function call
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str, input_type: str = "search_document") -> List[float]:
    """
    Generate embeddings using SentenceTransformers
    
    Args:
        text: Input text to embed
        input_type: Not used with sentence transformers, kept for compatibility
        
    Returns:
        List of floats representing the embedding (384 dimensions)
    """
    # Generate embedding
    embedding = model.encode(text, convert_to_tensor=False, normalize_embeddings=True)
    
    # Convert numpy array to Python list
    return embedding.tolist()
