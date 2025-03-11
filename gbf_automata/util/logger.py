import logging
from logging import Logger

from gbf_automata.util.application_settings import settings

logging.basicConfig(level=settings.log_level, format=settings.log_format)


def get_logger(name: str | None = None) -> Logger:
    return logging.getLogger(name)
