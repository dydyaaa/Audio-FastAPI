from fastapi import APIRouter, Depends, HTTPException
from src.auth.service import AuthService
from src.config import settings
from src.database import get_db
from src.auth.schemas import TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.get("/login")
def login():
    return {
        "auth_url": f"{settings.YANDEX_AUTH_URL}?response_type=code&client_id={settings.YANDEX_CLIENT_ID}"
    }
    
@router.get("/callback/", response_model=TokenResponse)
async def auth_callback(code: str, db: AsyncSession = Depends(get_db)):
    try:
        yandex_id, email = await AuthService.yandex_callback(code)
        user, jwt_token = await AuthService.register_or_login(db, yandex_id, email)
        return {
                "message": "User authorized",
                "user_id": user.id,
                "jwt_token": jwt_token
            }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
