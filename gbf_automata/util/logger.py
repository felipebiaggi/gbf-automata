import logging
from logging import Logger

from gbf_automata.util.settings import settings

logging.basicConfig(level=settings.log.level, format=settings.log.format)


def get_logger(name: str | None = None) -> Logger:
    return logging.getLogger(name)
