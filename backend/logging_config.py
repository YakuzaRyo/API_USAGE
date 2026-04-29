import json
import logging
import os
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_RETENTION_DAYS = 30


class _JsonFormatter(logging.Formatter):
    def format(self, record):
        obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info and record.exc_info[1]:
            obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(obj, ensure_ascii=False)


class _ChunkedFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, maxBytes=LOG_MAX_BYTES, backupCount=LOG_RETENTION_DAYS, **kwargs):
        super().__init__(filename, when="midnight", interval=1, backupCount=backupCount, **kwargs)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        if super().shouldRollover(record):
            return 1
        if self.stream and os.path.isfile(self.baseFilename):
            if os.path.getsize(self.baseFilename) >= self.maxBytes:
                return 1
        return 0


def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = str(LOG_DIR / "app.log")

    root_logger = logging.getLogger("backend")
    root_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    if root_logger.handlers:
        return root_logger

    # File: JSON format with daily + size rotation
    file_handler = _ChunkedFileHandler(log_file)
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setFormatter(_JsonFormatter())
    root_logger.addHandler(file_handler)

    # Console: human-readable
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    root_logger.addHandler(console_handler)

    # Silence noisy third-party loggers
    for name in ("uvicorn.access", "sqlalchemy.engine"):
        logging.getLogger(name).setLevel(logging.WARNING)

    return root_logger
