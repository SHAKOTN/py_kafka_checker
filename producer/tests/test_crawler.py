import os
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from producer.site_crawler import get_sites_metadata
from producer.site_crawler import parse_site_content
from producer.site_metadata import SiteMetadata


@patch('producer.site_crawler.get_sites_urls', return_value=["https://whatever.com"])
@patch('producer.site_crawler.requests.get')
@patch.dict(os.environ, {"WEBSITE_CONTENT_REGEX": 'href=\"(http://.*?)\"'})
@pytest.mark.parametrize("status_code,response_time", [(200, 1.00), (400, 3.14), (500, 0.24)])
def test_crawler_parametrized_with_regex(get_mock, __, status_code, response_time):
    get_mock.return_value = MagicMock(
        url="https://hyrule.com",
        status_code=status_code,
        text='<p><a href="http://example/knob.html">Somet content</a></p>',
        elapsed=MagicMock(total_seconds=MagicMock(return_value=response_time))
    )
    expected_site_meta = SiteMetadata(
        url="https://hyrule.com",
        code=status_code,
        content="http://example/knob.html",
        response_time=response_time
    )
    assert get_sites_metadata()[0] == expected_site_meta

@patch('producer.site_crawler.get_sites_urls', return_value=["https://whatever.com"])
@patch('producer.site_crawler.requests.get')
def test_crawler_parametrized_without_regex(get_mock, __):
    get_mock.return_value = MagicMock(
        url="https://hyrule.com",
        status_code=200,
        text='<p><a href="http://example/knob.html">Somet content</a></p>',
        elapsed=MagicMock(total_seconds=MagicMock(return_value=0.25))
    )
    expected_site_meta = SiteMetadata(
        url="https://hyrule.com",
        code=200,
        content='<p><a href="http://example/knob.html">Somet content</a></p>',
        response_time=0.25
    )
    assert get_sites_metadata()[0] == expected_site_meta


@patch.dict(os.environ, {"WEBSITE_CONTENT_REGEX": 'href=\"(http://.*?)\"'})
@patch('producer.site_crawler.requests.get')
def get_site_metadata_with_regex(get_mock):
    get_mock.return_value = MagicMock(
        url="https://hyrule.com",
        status_code=200,
        text='<p><a href="http://example/knob.html">Somet content</a></p>',
        elapsed=MagicMock(total_seconds=MagicMock(return_value=0.25))
    )

@pytest.mark.parametrize(
    "regex,result",
    [('href=\"(http://.*?)\"', 'http://example/knob.html;; http://htmlbook.com/example/knob.html'),
     ('<title>(.*?)</title>', 'Attributes'),]
)
def test_parse_site_content(regex, result):
    parsed_content = parse_site_content(
        content="""
        <!DOCTYPE HTML>
        <html>
         <head>
          <meta charset="utf-8">
          <title>Attributes</title>
         </head>
         <body>
          <p><a href="http://example/knob.html">Some content</a></p>
          <p><a href="http://htmlbook.com/example/knob.html">Some content again</a></p>
    """,
        regex_pattern=regex
    )
    assert result == parsed_content
