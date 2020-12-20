from unittest.mock import MagicMock

from consumer.consumer import consume_messages
from consumer.database import Session


def test_consume_message_data_saved_to_db(consumer_mocked, migrate_table):
    consume_messages()
    select_sql = "SELECT content FROM website_metrics ORDER BY created_on DESC;"
    count_sql = "SELECT COUNT(*) FROM website_metrics;"
    with Session() as session:
        select_results = session.fetch_one(select_sql)
        count_result = session.fetch_one(count_sql)

    # Some random webpage content
    assert select_results == ('<!doctype html><html itemscope=""',)
    assert count_result == (1,)

def test_consume_multiple_messages(migrate_table, consumer_mocked_multiple_messages):
    consume_messages()
    count_sql = "SELECT COUNT(*) FROM website_metrics;"
    with Session() as session:
        count_result = session.fetch_one(count_sql)
    assert count_result == (2,)

    # Check that messages were created properly
    with Session() as session:
        select_result_github = session.fetch_one(
            "SELECT code FROM website_metrics WHERE url = 'https://www.github.com/';"
        )
        select_result_google = session.fetch_one(
            "SELECT code FROM website_metrics WHERE url = 'https://www.google.com/';"
        )
        select_multiple_results = session.fetch_all(
            "SELECT code FROM website_metrics ORDER BY code DESC;"
        )
    assert select_result_github == (500,)
    assert select_result_google == (200,)
    assert select_multiple_results == [(500,), (200,)]


def test_invalid_message_data(migrate_table, mocker):
    """
    Case when one data point is missing. Message should be not saved to database
    """
    mocker.patch(
        "consumer.consumer.KafkaConsumer",
        return_value=[
            MagicMock(value={
                'url': 'https://www.google.com/',
                'response_time': 0.152716,
                'code': 200
            })
        ]
    )
    consume_messages()
    select_sql = "SELECT COUNT(*) FROM website_metrics;"
    with Session() as session:
        select_results = session.fetch_one(select_sql)

    # Message is not saved into db because it has invalid format
    assert select_results == (0,)
