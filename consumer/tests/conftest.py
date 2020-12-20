from unittest.mock import MagicMock

import pytest

from consumer.database import Session
from consumer.database.migrate import drop_metrics_table
from consumer.database.migrate import migrate_metrics_table


@pytest.fixture
def psycopg2_connect_fixture(mocker):
    mocker.patch(
        "consumer.database.database_session.psycopg2.connect",
        return_value=MagicMock()
    )


@pytest.fixture
def psycopg2_session_exception_on_commit(mocker, psycopg2_connect_fixture):
    mocker.patch(
        "consumer.database.database_session.Session.commit",
        side_effect=Exception("")
    )


@pytest.fixture
def migrate_table():
    drop_metrics_table()
    migrate_metrics_table()
    yield
    drop_metrics_table()


@pytest.fixture
def populate_table_with_test_data(migrate_table):
    with Session() as session:
        session.execute(
            """
            INSERT INTO website_metrics(url, content, response_time, code) VALUES (%s, %s, %s, %s)
            """,
            ("http://google.com", "some_content", 1.42, 200)
        )
        session.commit()


@pytest.fixture
def consumer_mocked(mocker):
    mocker.patch(
        "consumer.consumer.KafkaConsumer",
        return_value=[
            MagicMock(value={
                'url': 'https://www.google.com/',
                'content': '<!doctype html><html itemscope=""',
                'response_time': 0.152716,
                'code': 200
            })
        ]
    )

@pytest.fixture
def consumer_mocked_multiple_messages(mocker):
    mocker.patch(
        "consumer.consumer.KafkaConsumer",
        return_value=[
            MagicMock(value={
                'url': 'https://www.google.com/',
                'content': '<!doctype html><html itemscope=""',
                'response_time': 0.152716,
                'code': 200
            }),
            MagicMock(value={
                'url': 'https://www.github.com/',
                'content': 'INTERNAL SERVER ERROR',
                'response_time': 1.24,
                'code': 500
            })
        ]
    )