from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.auth.models import User
from src.auth.utils import get_current_user
from src.users.service import UserService
from src.users.schemas import UserInfo, UserUpdate

router = APIRouter()

@router.get("/me/", response_model=UserInfo)
async def get_me(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о текущем пользователе."""
    return await UserService.get_user_info(db, user)

@router.post("/me/", response_model=UserInfo)
async def update_me(
    user_update: UserUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить информацию о текущем пользователе."""
    return await UserService.update_user_info(db, user, user_update.email)