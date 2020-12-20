## Kafka Consumer/Producer and Site Checker

---

## CI and Tests
| CI Status: ![Test](https://github.com/SHAKOTN/py_kafka_checker/workflows/Test/badge.svg) | Latest CI runs - [Link](https://github.com/SHAKOTN/py_kafka_checker/actions?query=workflow%3ATest)|
|---|---:

---

### Test Coverage:
#### Consumer:
```
Name                                         Stmts   Miss  Cover
----------------------------------------------------------------
consumer/__init__.py                             0      0   100%
consumer/consumer.py                            18      0   100%
consumer/database/__init__.py                    2      0   100%
consumer/database/database_session.py           36      0   100%
consumer/database/migrate.py                    18      2    89%
consumer/message_validator.py                   10      0   100%
consumer/tests/__init__.py                       0      0   100%
consumer/tests/conftest.py                      28      0   100%
consumer/tests/test_consume.py                  32      0   100%
consumer/tests/test_message_validator.py         5      0   100%
consumer/tests/test_session_integration.py      31      0   100%
consumer/tests/test_session_units.py            29      0   100%
consumer_run.py                                  5      5     0%
----------------------------------------------------------------
TOTAL                                          214      7    97%
```

#### Producer:
```
Name                              Stmts   Miss  Cover
-----------------------------------------------------
producer/__init__.py                  0      0   100%
producer/producer.py                 18      4    78%
producer/site_crawler.py             18      3    83%
producer/site_metadata.py             7      0   100%
producer/tests/__init__.py            0      0   100%
producer/tests/test_crawler.py       29      1    97%
producer/tests/test_producer.py      11      0   100%
producer/utils.py                     7      0   100%
producer_run.py                       5      5     0%
-----------------------------------------------------
TOTAL                                95     13    86%
```