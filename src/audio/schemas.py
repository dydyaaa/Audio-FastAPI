from pydantic import BaseModel

class AudioCreate(BaseModel):
    name: str

class AudioResponse(BaseModel):
    id: int
    name: str
    file_path: str
    user_id: int

    class Config:
        from_attributes = True