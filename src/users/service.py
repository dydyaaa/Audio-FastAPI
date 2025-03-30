import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from src.auth.models import User

logger = logging.getLogger("app.users")

class UserService:
    @staticmethod
    async def get_user_info(db: AsyncSession, user: User) -> User:
        """Получает информацию о текущем пользователе."""
        logger.info(f"Получение информации о пользователе: {user.email}")
        return user

    @staticmethod
    async def update_user_info(db: AsyncSession, user: User, new_email: str) -> User:
        """Обновляет email текущего пользователя."""
        # Проверяем, не занят ли новый email другим пользователем
        result = await db.execute(select(User).filter_by(email=new_email))
        existing_user = result.scalars().first()
        if existing_user and existing_user.id != user.id:
            logger.warning(f"Попытка сменить email на уже занятый: {new_email}")
            raise HTTPException(status_code=400, detail="Этот email уже занят")

        # Обновляем email
        user.email = new_email
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        logger.info(f"Email пользователя обновлён: {user.email}")
        return user