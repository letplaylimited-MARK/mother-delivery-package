"""
Ghost Hub SDK Logging Configuration
Structured logging with rotation
"""

import logging
import json
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional


class JSONFormatter(logging.Formatter):
    """JSON log formatter"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data)


class StructuredFormatter(logging.Formatter):
    """Human-readable structured formatter"""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        level = record.levelname.ljust(8)
        logger = record.name.ljust(30)

        message = record.getMessage()
        if record.exc_info:
            message += f"\n{self.formatException(record.exc_info)}"

        return f"{timestamp} | {level} | {logger} | {message}"


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = False,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:
    """Setup structured logging"""

    logger = logging.getLogger("ghost_hub_sdk")
    logger.setLevel(getattr(logging, level.upper()))
    logger.handlers.clear()

    formatter = JSONFormatter() if json_format else StructuredFormatter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get logger for module"""
    return logging.getLogger(f"ghost_hub_sdk.{name}")


class LogContext:
    """Context manager for adding extra log data"""

    def __init__(self, logger: logging.Logger, **kwargs):
        self.logger = logger
        self.extra = kwargs
        self.old_factory = None

    def __enter__(self):
        self.old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            record.extra = self.extra
            return record

        logging.setLogRecordFactory(record_factory)
        return self

    def __exit__(self, *args):
        if self.old_factory:
            logging.setLogRecordFactory(self.old_factory)


class AuditLogger:
    """Audit logging for compliance"""

    def __init__(self, log_file: str = "audit.log"):
        self.logger = logging.getLogger("ghost_hub_sdk.audit")
        self.logger.setLevel(logging.INFO)

        handler = TimedRotatingFileHandler(
            log_file, when="midnight", interval=1, backupCount=30, encoding="utf-8"
        )
        handler.setFormatter(JSONFormatter())
        self.logger.addHandler(handler)

    def log_action(
        self,
        action: str,
        user: str,
        resource: str,
        result: str,
        details: Optional[dict] = None,
    ):
        """Log audit action"""
        self.logger.info(
            "Audit event",
            extra={
                "audit_action": action,
                "audit_user": user,
                "audit_resource": resource,
                "audit_result": result,
                "audit_details": details or {},
            },
        )

    def log_access(self, user: str, resource: str, granted: bool):
        """Log resource access"""
        self.log_action(
            action="access",
            user=user,
            resource=resource,
            result="granted" if granted else "denied",
        )

    def log_config_change(self, user: str, setting: str, old_value, new_value):
        """Log configuration change"""
        self.log_action(
            action="config_change",
            user=user,
            resource=f"setting:{setting}",
            result="changed",
            details={"old": str(old_value), "new": str(new_value)},
        )


audit_logger = AuditLogger()
