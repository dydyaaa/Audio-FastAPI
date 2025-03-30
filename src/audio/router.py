from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.audio.service import AudioService
from src.audio.schemas import AudioCreate, AudioResponse
from src.auth.utils import get_current_user
from src.auth.models import User

router = APIRouter()

@router.post("/upload/", response_model=AudioResponse)
async def upload_audio(
    file: UploadFile = File(...),
    name: str = Form(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Загружает новый аудио файл."""
    return await AudioService.upload_audio(db, file, name, user)

@router.get("/files/", response_model=list[AudioResponse])
async def get_audio_files(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получает список аудио файлов пользователя."""
    return await AudioService.get_user_audio_files(db, user)

@router.delete("/delete/{audio_id}", status_code=204)
async def delete_audio(
    audio_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Удаляет указанный аудио файл."""
    await AudioService.delete_audio_file(db, audio_id, user)
    return None