from datetime import datetime, timedelta
from src.config import settings
from jose import jwt

def create_access_token(user_id: str) -> str:
    expires = datetime.utcnow() + timedelta(seconds=settings.JWT_ACCESS_TOKEN_EXPIRES)
    to_encode = {"sub": user_id, "exp": expires}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")