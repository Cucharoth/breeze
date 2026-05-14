import logging
import sys
from rich.logging import RichHandler
from app.core.config import get_settings

settings = get_settings()

def setup_logging():
    log_level = logging.INFO if settings.IS_PROD else logging.DEBUG
    
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )
    
    # Set levels for other loggers
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

logger = logging.getLogger("breeze")
