import os
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import call


from producer.producer import send_message


@patch('producer.site_crawler.requests.get')
def test_message_send(get_mock):
    kafka_producer_mock = MagicMock()
    get_mock.return_value = MagicMock(
        url="https://hyrule.com",
        status_code=200,
        text='<p>Random Website Content</p>',
        elapsed=MagicMock(total_seconds=MagicMock(return_value=0.25))
    )
    send_message(kafka_producer_mock)
    # Number of calls eq to number of sites to check
    assert kafka_producer_mock.send.call_count == len(os.getenv("SITE_URLS", "https://google.com").split(","))
    # Assert KafkaProducer is called with proper
    kafka_producer_mock.send.assert_called_with(
        'metrics',
        value={
            'url': 'https://hyrule.com',
            'content': '<p>Random Website Content</p>',
            'response_time': 0.25, 'code': 200}
    )