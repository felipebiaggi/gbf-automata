import random
import time

from gbf_automata.util.logger import get_logger

logger = get_logger()


def random_delay(min_delay=1.0, max_delay=2.5, variation=0.2) -> None:
    base_delay = random.uniform(min_delay, max_delay)
    jitter = random.uniform(-variation, variation) * base_delay
    final_delay = max(min_delay, base_delay + jitter)

    logger.info(f"[DELAY] {final_delay}")
    time.sleep(final_delay)
