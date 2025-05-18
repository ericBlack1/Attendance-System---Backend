import numpy as np
from deepface import DeepFace

def generate_embedding(aligned_face: np.ndarray) -> list:
    """
    Generate 128D/512D facial embedding using FaceNet
    """
    # Using DeepFace wrapper (can replace with direct TensorFlow/Keras impl)
    result = DeepFace.represent(
        img_path=aligned_face,
        model_name="Facenet",
        enforce_detection=False
    )
    return result[0]["embedding"]  # Returns 128D vector for FaceNet

def compare_embeddings(embedding1: list, embedding2: list, threshold=0.6) -> bool:
    """
    Compare two embeddings using cosine similarity
    Returns True if match, False otherwise
    """
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Convert to numpy arrays
    e1 = np.array(embedding1).reshape(1, -1)
    e2 = np.array(embedding2).reshape(1, -1)
    
    similarity = cosine_similarity(e1, e2)[0][0]
    return similarity >= threshold
