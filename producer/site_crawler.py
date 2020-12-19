import logging
import os
from dataclasses import dataclass
from typing import List

import requests

logger = logging.getLogger(__name__)

@dataclass
class SiteMetadata:
    url: str
    content: str
    response_time: float
    code: int

def get_sites_metadata() -> List[SiteMetadata]:
    site_urls = os.getenv("SITE_URLS").split(",")
    sites = []
    for url in site_urls:
        try:
            response = requests.get(url)
        except requests.ConnectionError as exc:
            logger.exception(f"Can't reach resource: {exc.response}")
            continue
        else:
            sites.append(SiteMetadata(
                url=response.url,
                content=response.text[:100],
                response_time=response.elapsed.total_seconds(),
                code=response.status_code,
            ))
    return sites