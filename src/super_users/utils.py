from src.auth.utils import get_current_user
from fastapi import HTTPException, Depends
from src.auth.models import User

# Проверка на суперпользователя
async def get_super_user(user: User = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Требуются права суперпользователя")
    return user