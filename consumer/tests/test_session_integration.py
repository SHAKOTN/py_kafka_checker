import pytest
from psycopg2 import InterfaceError

from consumer.database import Session

INSERT_SQL = """
    INSERT INTO website_metrics(url, content, response_time, code) VALUES (%s, %s, %s, %s)
"""

def test_raises_cursor_already_closed(migrate_table):
    with Session() as session:
        pass
    with pytest.raises(InterfaceError):
        session.execute("SELECT * FROM website_metrics ORDER BY created_on DESC;")

def test_raises_invalid_sql(migrate_table):
    with pytest.raises(Exception):
        with Session() as session:
            session.execute(
                "INSERT INSERT INTO website_metrics(url, content, response_time, code) VALUES (%s, %s, %s, %s)",
                ("http://another_google.com", "princess_zelda", 3.33, 201)
            )
def test_raises_insert_invalid_type(migrate_table):
    with pytest.raises(Exception):
        with Session() as session:
            session.execute(
                "INSERT INTO website_metrics(url, content, response_time, code) VALUES (%s, %s, %s, %s)",
                (123, 123, "something", 201)
            )

def test_fetch_all(populate_table_with_test_data):
    select_sql = "SELECT content FROM website_metrics ORDER BY created_on DESC;"
    with Session() as session:
        session.execute(
            INSERT_SQL,
            ("http://another_google.com", "princess_zelda", 3.33, 201)
        )
        session.commit()
        select_results = session.fetch_all(select_sql)

    assert select_results == [('princess_zelda',), ('some_content',)]

def test_fetch_one(populate_table_with_test_data):
    select_sql = "SELECT content FROM website_metrics ORDER BY created_on DESC;"

    with Session() as session:
        session.execute(
            INSERT_SQL,
            ("http://some_website", "Calamity Ganon", 1.48, 200)
        )
        session.commit()
        select_results = session.fetch_one(select_sql)

    # Ordering is done by create time descending, so we get latest record as first
    assert select_results == ('Calamity Ganon',)
