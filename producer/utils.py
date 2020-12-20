import re
import os
from typing import List


def get_sites_urls() -> List[str]:
    return os.getenv("SITE_URLS", "https://google.com").split(",")

def parse_site_content(content: str, regex_pattern: str) -> str:
    return ";; ".join(re.findall(regex_pattern, content))
