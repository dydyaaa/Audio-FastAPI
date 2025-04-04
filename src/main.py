import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from src.audio.router import router as audio_router
from src.auth.router import router as auth_router
from src.users.router import router as users_router
from src.super_users.router import router as super_users_router
from logging.config import fileConfig
from src.logging_config import setup_logging
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(
    title="Referral System API",
    description="API для управления реферальной системой",
    version="1.0.0",
)

instrumentator = Instrumentator().instrument(app)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(audio_router, prefix="/audio", tags=["audio"])
app.include_router(users_router, prefix='/users', tags=["users"])
app.include_router(super_users_router, prefix="/super_users", tags=["super_users"])

@app.on_event("startup")
async def startup_event():
    fileConfig("logging.ini", disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    setup_logging(test_mode=False)
    logger.info("Application starting up")
    instrumentator.expose(app, endpoint="/metrics", include_in_schema=True)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger = logging.getLogger(__name__)
    logger.error(f"Internal Server Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )