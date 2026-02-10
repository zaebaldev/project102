import uvicorn

from app.api.api_v1 import router as api_v1_router
from app.api.middlewares.cors_middleware import register_cors_middleware
from app.create_app import create_app
from app.rate_limiter import limiter
from core.config import settings

main_app = create_app()
main_app.state.limiter = limiter
main_app.include_router(
    api_v1_router,
    prefix=settings.api.prefix,
)
register_cors_middleware(main_app)
if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.gunicorn.host,
        port=settings.gunicorn.port,
        reload=True,
    )
