from fastapi import FastAPI
from app.config.settings import settings
from app.api.router import router

from dishka.integrations.fastapi import setup_dishka
from app.container import container


def create_app():
    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
        debug=settings.debug,
        description="Task manager service",
        docs_url="/docs",
        redoc_url="/redoc",
        root_path="/api",
    )
    app.include_router(router=router)
    return app


def create_production_app():
    app = create_app()
    setup_dishka(container, app)
    return app
