import cv2
import numpy as np
from sqlalchemy.orm import Session
from deepface import DeepFace
from .models import StudentBiometrics
from .utils.face_detection import (
    decode_base64_to_image,
    detect_faces,
    align_face
)
from .utils.embeddings import (
    generate_embedding,
    compare_embeddings
)
from fastapi import HTTPException, status

class BiometricException(HTTPException):
    """Custom exception for biometric failures"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

def register_face(db: Session, student_id: int, image_base64: str) -> StudentBiometrics:
    """
    Register a student's face by:
    1. Decoding base64 image
    2. Detecting and aligning face
    3. Generating facial embedding
    4. Storing in database
    """
    try:
        # Step 1: Image processing
        img = decode_base64_to_image(image_base64)
        if img is None:
            raise BiometricException("Invalid image format")

        # Step 2: Face detection
        faces = detect_faces(img)
        if not faces:
            raise BiometricException("No face detected in image")
        
        # Step 3: Face alignment and embedding
        aligned_face = align_face(img, faces[0])  # Use the first detected face
        embedding = generate_embedding(aligned_face)

        # Step 4: Database operations
        existing = db.query(StudentBiometrics).filter(
            StudentBiometrics.student_id == student_id
        ).first()
        
        if existing:
            # Update existing record
            existing.facial_embedding = embedding
        else:
            # Create new record
            existing = StudentBiometrics(
                student_id=student_id,
                facial_embedding=embedding,
                image_path=f"storage/{student_id}.jpg"
            )
            db.add(existing)
        
        db.commit()
        return existing

    except Exception as e:
        db.rollback()
        raise BiometricException(f"Registration failed: {str(e)}")

def verify_face(db: Session, student_id: int, image_base64: str) -> dict:
    """
    Verify a student's face by:
    1. Getting stored embedding from DB
    2. Processing new image
    3. Comparing embeddings
    """
    try:
        # Step 1: Get stored data
        stored = db.query(StudentBiometrics).filter(
            StudentBiometrics.student_id == student_id
        ).first()
        
        if not stored:
            raise BiometricException("No registered face for this student")

        # Step 2: Process new image
        img = decode_base64_to_image(image_base64)
        faces = detect_faces(img)
        if not faces:
            return {"verified": False, "confidence": 0.0, "reason": "No face detected"}
        
        aligned_face = align_face(img, faces[0])
        new_embedding = generate_embedding(aligned_face)

        # Step 3: Compare embeddings
        is_verified = compare_embeddings(
            stored.facial_embedding,
            new_embedding
        )
        
        confidence = cosine_similarity(
            np.array(stored.facial_embedding).reshape(1, -1),
            np.array(new_embedding).reshape(1, -1)
        )[0][0]

        return {
            "verified": is_verified,
            "confidence": float(confidence),
            "reason": "" if is_verified else "Face mismatch"
        }

    except Exception as e:
        raise BiometricException(f"Verification failed: {str(e)}")

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors"""
    from numpy.linalg import norm
    return np.dot(a, b.T)/(norm(a)*norm(b))
