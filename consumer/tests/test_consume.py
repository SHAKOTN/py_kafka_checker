from consumer.consumer import consume_messages
from consumer.database import Session


def test_consume_message_data_saved_to_db(consumer_mocked, migrate_table):
    consume_messages()
    select_sql = "SELECT content FROM website_metrics ORDER BY created_on DESC;"

    with Session() as session:
        select_results = session.fetch_one(select_sql)

    # Some random webpage content
    assert select_results == ('<!doctype html><html itemscope=""',)
