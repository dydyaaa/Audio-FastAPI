import os
import logging
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.auth.models import User
from src.audio.models import AudioFile
from src.config import settings


logger = logging.getLogger("app.audio")

class AudioService:
    @staticmethod
    async def upload_audio(db: AsyncSession, file: UploadFile, name: str, user: User) -> AudioFile:
        """Сохраняет аудио файл на сервере и в базе данных."""
        user_dir = os.path.join(settings.UPLOAD_DIR, "audio", user.email)
        os.makedirs(user_dir, exist_ok=True)

        if not file.filename.lower().endswith(('.mp3', '.wav', '.ogg')):
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат аудио")

        file_extension = os.path.splitext(file.filename)[1]
        file_path = os.path.join(user_dir, f"{name}{file_extension}")

        try:
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
        except Exception as e:
            logger.error(f"Ошибка при сохранении файла: {str(e)}")
            raise HTTPException(status_code=500, detail="Ошибка при сохранении файла")

        audio = AudioFile(name=name, file_path=file_path, user_id=user.id)
        db.add(audio)
        await db.commit()
        await db.refresh(audio)
        
        logger.info(f"Аудио файл загружен: {name} для пользователя {user.email}")
        return audio

    @staticmethod
    async def get_user_audio_files(db: AsyncSession, user: User) -> list[AudioFile]:
        """Возвращает список аудио файлов пользователя."""
        result = await db.execute(select(AudioFile).filter_by(user_id=user.id))
        audio_files = result.scalars().all()
        return audio_files

    @staticmethod
    async def delete_audio_file(db: AsyncSession, audio_id: int, user: User) -> None:
        """Удаляет аудио файл пользователя."""
        result = await db.execute(select(AudioFile).filter_by(id=audio_id, user_id=user.id))
        audio = result.scalars().first()

        if not audio:
            raise HTTPException(status_code=404, detail="Файл не найден или не принадлежит пользователю")

        try:
            if os.path.exists(audio.file_path):
                os.remove(audio.file_path)
        except Exception as e:
            logger.error(f"Ошибка при удалении файла с диска: {str(e)}")
            raise HTTPException(status_code=500, detail="Ошибка при удалении файла")

        await db.delete(audio)
        await db.commit()
        
        logger.info(f"Аудио файл удален: {audio.name} для пользователя {user.email}")