import logging
import os
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)

@dataclass
class SiteMetadata:
    url: str
    content: str
    response_time: float
    code: int

def get_site_metadata() -> SiteMetadata:
    try:
        response = requests.get(os.getenv("SITE_URL"))
        return SiteMetadata(
            url=response.url,
            content=response.text[:100],
            response_time=response.elapsed.total_seconds(),
            code=response.status_code,
        )
    except requests.ConnectionError as exc:
        logger.exception(f"Can't reach resource: {exc.response}")
