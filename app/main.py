from fastapi import FastAPI
from app.modules.auth.routes import router as auth_router
from app.core.database import Base, engine

app = FastAPI()

# Create tables (only for dev; use migrations in production)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Attendance System API"}
