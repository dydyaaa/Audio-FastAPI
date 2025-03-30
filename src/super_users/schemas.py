from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    id: int
    email: EmailStr
    is_superuser: bool

    class Config:
        from_attributes = True

class AudioFileInfo(BaseModel):
    id: int
    name: str
    file_path: str
    user_id: int

    class Config:
        from_attributes = True