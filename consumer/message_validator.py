import logging
from typing import Dict

logger = logging.getLogger(__name__)


REQUIRED_MESSAGE_POINTS = ['url', 'content', 'response_time', 'code']

def is_valid_consumer_message(consumer_message: Dict) -> bool:
    is_valid = True
    if not all (key in consumer_message.keys() for key in REQUIRED_MESSAGE_POINTS):
        logger.error(
            f"Message required to contain {REQUIRED_MESSAGE_POINTS} keys. "
            f"Received {consumer_message.keys()} instead"
        )
        is_valid = False
    return is_valid