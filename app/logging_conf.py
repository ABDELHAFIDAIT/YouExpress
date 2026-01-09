import logging
import logging.config
import os
import sys


if not os.path.exists("logs"):
    os.makedirs("logs")

def configure_logging():
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        
        # 1 - FORMAT DES MESSAGES ---
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "%(levelname)s: %(message)s",
            },
        },
        
        # 2 - DESTINATIONS (HANDLERS) ---
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": sys.stdout,
            },
            "file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "standard",
                "filename": "logs/app.log",
                "maxBytes": 10 * 1024 * 1024,
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        
        # 3 - CONFIGURATION DES LOGGERS ---
        "loggers": {
            "root": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "app": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": ["console"],
                "level": "WARNING", 
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(LOGGING_CONFIG)