from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.biometrics.schemas import (  # Import all required schemas
    BiometricCreate,
    BiometricVerify,
    VerificationResult
)
from app.modules.biometrics.services import (
    register_face,
    verify_face
)

router = APIRouter(prefix="/biometrics", tags=["Biometrics"])

@router.post("/register", response_model=VerificationResult)
async def register_biometrics(
    data: BiometricCreate, 
    db: Session = Depends(get_db)
):
    try:
        register_face(db, data.student_id, data.image_base64)
        return {"is_verified": True, "confidence": 1.0}
    except Exception as e:
        return {"is_verified": False, "confidence": 0.0}

@router.post("/verify", response_model=VerificationResult)
async def verify_biometrics(
    data: BiometricVerify, 
    db: Session = Depends(get_db)
):
    is_verified = verify_face(db, data.student_id, data.image_base64)
    return {"is_verified": is_verified, "confidence": 0.95 if is_verified else 0.0}
