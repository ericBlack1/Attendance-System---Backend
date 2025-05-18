from sqlalchemy import Column, Integer, String, ARRAY, Float
from app.core.database import Base

class StudentBiometrics(Base):
    __tablename__ = "student_biometrics"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, unique=True)  # Links to User table
    facial_embedding = Column(ARRAY(Float))    # Stores 128D/512D face embeddings
    image_path = Column(String)                # Optional: Path to reference image
