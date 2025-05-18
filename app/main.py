from fastapi import FastAPI
from app.modules.auth.routes import router as auth_router
from app.core.database import Base, engine
from app.modules.biometrics.routes import router as biometrics_router

app = FastAPI(
    title="Attendance System API",
    description="Facial Recognition Attendance System",
    version="1.0.0"
)

# Create tables (only for dev; use migrations in production)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(biometrics_router)

@app.get("/")
def home():
    return {
        "message": "Attendance System API",
        "endpoints": {
            "auth": "/auth",
            "biometrics": "/biometrics"
        }
    }
    
@app.on_event("startup")
def test_db_connection():
    try:
        with engine.connect() as conn:
            print("✅ Database connection successful")
    except Exception as e:
        print("❌ Database connection failed")
        raise e
