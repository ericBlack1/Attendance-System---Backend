from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
