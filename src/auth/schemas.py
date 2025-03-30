from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    yandex_id: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_superuser: bool

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    message: str
    user_id: int
    jwt_token: str