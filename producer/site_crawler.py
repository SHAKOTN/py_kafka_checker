import logging
import os
from typing import List

import requests

from producer.constants import WEBSITE_CONTENT_REGEX_ENV
from producer.site_metadata import SiteMetadata
from producer.utils import get_sites_urls
from producer.utils import parse_site_content

logger = logging.getLogger(__name__)


def get_sites_metadata() -> List[SiteMetadata]:
    sites_metadata = []
    for url in get_sites_urls():
        try:
            response = requests.get(url)
        except requests.ConnectionError as exc:
            logger.exception(f"Can't reach resource: {exc.response}")
            continue
        else:
            sites_metadata.append(
                SiteMetadata(
                    url=response.url,
                    content=parse_site_content(response.text, os.getenv(WEBSITE_CONTENT_REGEX_ENV))
                        if os.getenv(WEBSITE_CONTENT_REGEX_ENV) else response.text[:4000],
                    response_time=response.elapsed.total_seconds(),
                    code=response.status_code,
                ))
    return sites_metadata
