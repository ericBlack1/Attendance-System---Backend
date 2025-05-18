from pydantic import BaseModel
from typing import List

class BiometricCreate(BaseModel):
    student_id: int
    image_base64: str  # Base64-encoded face image

class BiometricVerify(BaseModel):
    student_id: int
    image_base64: str

class VerificationResult(BaseModel):
    is_verified: bool
    confidence: float
