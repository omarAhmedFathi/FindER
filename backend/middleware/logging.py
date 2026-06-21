from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
import logging
import uuid

logger = logging.getLogger("api_request_logger")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            f"req_id={request_id} method={request.method} path={request.url.path} "
            f"status={response.status_code} duration={process_time:.4f}s"
        )
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id
        return response
