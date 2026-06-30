from pathlib import Path
import sys

from loguru import logger


Path("logs").mkdir(
    exist_ok=True
)

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

logger.add(
    "logs/application.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
)

app_logger = logger