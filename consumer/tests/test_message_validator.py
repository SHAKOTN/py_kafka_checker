from consumer.message_validator import is_valid_consumer_message

def test_is_valid_consumer_message__valid():
    assert is_valid_consumer_message(
        {
            'url': 'https://www.google.com/',
            'content': '<!doctype html><html itemscope=""',
            'response_time': 0.152716,
            'code': 200
        }
    )

def test_is_valid_consumer_message__invalid():
    assert not is_valid_consumer_message(
        {
            'url': 'https://www.google.com/',
            'content': '<!doctype html><html itemscope=""',
            'response_time': 0.152716,
        }
    )
