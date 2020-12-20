import re
import os
from dataclasses import dataclass
from typing import List


@dataclass
class SiteMetadata:
    """
    Container class for KafkaProducer message data
    """
    url: str
    content: str
    response_time: float
    code: int


def get_sites() -> List[str]:
    return os.getenv("SITE_URLS", "https://google.com").split(",")

def parse_site_content(content: str, regex_pattern: str) -> str:
    return ";; ".join(re.findall(regex_pattern, content))