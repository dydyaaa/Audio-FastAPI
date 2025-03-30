import logging
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.config import settings
from src.auth.models import User
from src.auth.utils import create_access_token
from fastapi import HTTPException


logger = logging.getLogger("app.auth")

class AuthService:
    @staticmethod
    async def yandex_callback(code: str) -> tuple[str, str]:
        async with httpx.AsyncClient() as client:

            token_response = await client.post(settings.YANDEX_TOKEN_URL, data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET
            })

            if token_response.status_code != 200:
                logger.error(f"Ошибка получения токена: {token_response.text}")
                raise HTTPException(status_code=400, detail="Ошибка получения токена")

            token_data = token_response.json()
            access_token = token_data["access_token"]

            user_response = await client.get(settings.YANDEX_USER_INFO_URL, headers={
                "Authorization": f"OAuth {access_token}"
            })

            if user_response.status_code != 200:
                logger.error(f"Ошибка получения данных пользователя: {user_response.text}")
                raise HTTPException(status_code=400, detail="Ошибка получения данных пользователя")

            user_data = user_response.json()
            yandex_id = user_data["id"]
            email = user_data.get("default_email", f"user_{yandex_id}@yandex.ru")
            
            return yandex_id, email
        
    @staticmethod
    async def register_or_login(db: AsyncSession, yandex_id: str, email: str) -> tuple[User, str]:
        result = await db.execute(select(User).filter_by(yandex_id=yandex_id))
        existing_user = result.scalars().first()
        
        if existing_user:
            logger.info(f'Пользователь уже существует: {existing_user.email}')
            jwt_token = create_access_token(str(existing_user.id))
            return existing_user, jwt_token
        
        new_user = User(yandex_id=yandex_id, email=email, is_superuser=False)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info(f'Пользователь успешно зарегистрирован: {email}')
        jwt_token = create_access_token(str(new_user.id))
        
        return new_user, jwt_token
