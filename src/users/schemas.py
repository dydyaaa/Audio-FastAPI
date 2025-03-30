from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: EmailStr