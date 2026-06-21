from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from core.config import settings
from core.cache import init_cache
from middleware.cors import setup_cors
from middleware.errors import global_exception_handler
from middleware.logging import LoggingMiddleware
from api.v1.router import api_router
from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Middlewares (Optimized)
setup_cors(app)
app.add_middleware(GZipMiddleware, minimum_size=1000) # Compress responses > 1KB
app.add_middleware(LoggingMiddleware)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)

# Metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing Cache & Worker Pools...")
    await init_cache()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Graceful shutdown initiated.")
