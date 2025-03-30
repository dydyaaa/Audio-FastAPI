import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import text
from fastapi import HTTPException
from src.auth.models import User
from src.audio.models import AudioFile
import os


logger = logging.getLogger("app.super_users")

class SuperUserService:
    @staticmethod
    async def get_user_info(db: AsyncSession, user_id: int) -> User:
        """Получает информацию о пользователе по его ID."""
        result = await db.execute(select(User).filter_by(id=user_id))
        user = result.scalars().first()
        if not user:
            logger.warning(f"Пользователь с ID {user_id} не найден")
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        logger.info(f"Информация о пользователе получена: {user.email}")
        return user

    @staticmethod
    async def get_user_audio_files(db: AsyncSession, user_id: int) -> list[AudioFile]:
        """Получает список аудиофайлов пользователя по его ID."""
        result = await db.execute(select(User).filter_by(id=user_id))
        user = result.scalars().first()
        if not user:
            logger.warning(f"Пользователь с ID {user_id} не найден")
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        result = await db.execute(select(AudioFile).filter_by(user_id=user_id))
        audio_files = result.scalars().all()
        logger.info(f"Получено {len(audio_files)} аудиофайлов для пользователя {user.email}")
        return audio_files

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> None:
        """Удаляет пользователя и все его аудиофайлы."""
        result = await db.execute(select(User).filter_by(id=user_id))
        user = result.scalars().first()
        if not user:
            logger.warning(f"Пользователь с ID {user_id} не найден")
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        if user.is_superuser:
            logger.warning(f"Попытка удалить суперпользователя {user.email}")
            raise HTTPException(status_code=403, detail="Нельзя удалить суперпользователя")

        result = await db.execute(select(AudioFile).filter_by(user_id=user_id))
        audio_files = result.scalars().all()
        for audio in audio_files:
            try:
                if os.path.exists(audio.file_path):
                    os.remove(audio.file_path)
                    logger.info(f"Удалён файл: {audio.file_path}")
            except Exception as e:
                logger.error(f"Ошибка при удалении файла {audio.file_path}: {str(e)}")
        
        if audio_files:
            await db.execute(
                text("DELETE FROM audio_files WHERE user_id = :user_id"), 
                {"user_id": user_id})
        await db.delete(user)
        await db.commit()
        
        logger.info(f"Пользователь {user.email} и его файлы удалены")