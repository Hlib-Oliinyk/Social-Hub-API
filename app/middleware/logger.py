import time
import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("http_logger")

class HTTPLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        log_message = (
            f"Response: {request.client.host}:{request.client.port} - "
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.4f}s"
        )
        logger.info(log_message)

        return response