import time
import logging
import uuid

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
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        if process_time > 1.0:
            logger.warning(
                f"[{request_id}] Slow request {request.method} {request.url.path}: {process_time:.2f}s"
            )

        log_message = (
            f"[{request_id}] {request.client.host}:{request.client.port} - "
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.4f}s"
        )
        logger.info(log_message)

        return response