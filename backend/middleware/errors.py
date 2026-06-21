from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("error_logger")

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Error: {str(exc)} | Path: {request.url.path}")
    
    # Catch all exception wrapper to prevent info leakage
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred. Our engineers have been notified."},
    )
