from fastapi import FastAPI
from app.config.settings import settings
from app.api.router import router

from dishka.integrations.fastapi import setup_dishka
from app.container import container


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    debug=settings.debug,
    description="Task manager service",
    docs_url="/docs",
    redoc_url="/redoc",
    root_path="/api",
)

setup_dishka(container=container, app=app)
app.include_router(router=router)
