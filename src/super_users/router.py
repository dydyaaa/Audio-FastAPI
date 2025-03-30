from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.auth.models import User
from src.super_users.utils import get_super_user
from src.super_users.service import SuperUserService
from src.super_users.schemas import UserInfo, AudioFileInfo


router = APIRouter()

@router.get("/get_user_info/{user_id}", response_model=UserInfo)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_super_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о пользователе по ID (только для суперпользователей)."""
    return await SuperUserService.get_user_info(db, user_id)

@router.get("/get_user_audio/{user_id}", response_model=list[AudioFileInfo])
async def get_user_audio(
    user_id: int,
    current_user: User = Depends(get_super_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить список аудиофайлов пользователя по ID (только для суперпользователей)."""
    return await SuperUserService.get_user_audio_files(db, user_id)

@router.delete("/delete_user/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_super_user),
    db: AsyncSession = Depends(get_db)
):
    """Удалить пользователя и его аудиофайлы (только для суперпользователей)."""
    await SuperUserService.delete_user(db, user_id)
    return None