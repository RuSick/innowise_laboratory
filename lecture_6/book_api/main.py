import logging
import time
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response

from .database import Base, engine
from .routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)  # Create database tables on startup

app = FastAPI(
    title="Book Collection API",
    description="A simple API to manage your book collection",
)

app.include_router(router)


@app.middleware("http")
async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:  # Log all HTTP requests with method, path, status code, and processing time
    start_time = time.time()
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response