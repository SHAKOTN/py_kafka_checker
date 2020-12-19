# Test suite with basic unittest for database session. It checks that all psycopg2
# calls are done as expected. No database calls, everything is mocked in pytest fixtures

import pytest

from consumer.database import Session


def test_connection_is_called_on_session_open(psycopg2_connect_fixture):
    with Session() as session:
        pass

    assert session._connection.cursor.call_count == 1
    assert session._connection.close.call_count == 1
    assert session._cursor.close.call_count == 1

def test_rollback_called_on_exception(psycopg2_session_exception_on_commit):
    with pytest.raises(Exception):
        with Session() as session:
            session.commit()

    # Make sure rollback is called on failed commit
    assert 1 == session._connection.rollback.call_count

def test_connection_commit_is_called(psycopg2_connect_fixture):
    with Session() as session:
        session.commit()

    assert session._connection.commit.call_count == 2

def test_cursor_execute_is_called(psycopg2_connect_fixture):
    with Session() as session:
        session.execute("SELECT * FROM imaginary_table")

    assert session._cursor.execute.call_count == 1

def test_cursor_execute_is_called__on_fetchall(psycopg2_connect_fixture):
    with Session() as session:
        session.fetch_all("SELECT * FROM imaginary_table")

    assert session._cursor.execute.call_count == 1

def test_cursor_execute_is_called__on_fetchone(psycopg2_connect_fixture):
    with Session() as session:
        session.fetch_one("SELECT * FROM imaginary_table")

    assert session._cursor.execute.call_count == 1