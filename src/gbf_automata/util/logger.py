import logging
from gbf_automata.util.settings import settings

logging.basicConfig(
    level=settings.log_level,
    format=settings.log_format
)

def get_logger(name: str):
    return logging.getLogger(name)

