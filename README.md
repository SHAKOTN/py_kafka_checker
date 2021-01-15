## Kafka Consumer/Producer and Site Checker
Simple consumer-producer application to check websites and utilize Kafka to send metatata and store it to database

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
consumer/constants.py                            6      0   100%
consumer/consumer.py                            24      0   100%
consumer/database/__init__.py                    4      0   100%
consumer/database/database_session.py           36      0   100%
consumer/database/migrate.py                    18      2    89%
consumer/message_validator.py                   10      0   100%
consumer/tests/__init__.py                       0      0   100%
consumer/tests/conftest.py                      28      0   100%
consumer/tests/test_consume.py                  32      0   100%
consumer/tests/test_message_validator.py         5      0   100%
consumer/tests/test_migrate.py                  14      0   100%
consumer/tests/test_session_integration.py      31      0   100%
consumer/tests/test_session_units.py            29      0   100%
consumer_run.py                                  5      5     0%
----------------------------------------------------------------
TOTAL                                          242      7    97%
```

#### Producer:
```
Name                              Stmts   Miss  Cover
-----------------------------------------------------
producer/__init__.py                  0      0   100%
producer/constants.py                 6      0   100%
producer/producer.py                 23      4    83%
producer/site_crawler.py             19      3    84%
producer/site_metadata.py             7      0   100%
producer/tests/__init__.py            0      0   100%
producer/tests/test_crawler.py       29      1    97%
producer/tests/test_producer.py      11      0   100%
producer/utils.py                     7      0   100%
producer_run.py                       5      5     0%
-----------------------------------------------------
TOTAL                               107     13    88%
```

---

## Quickstart
### Tests
To run tests:
```bash
$ make tests
```
Check [CI runs]((https://github.com/SHAKOTN/py_kafka_checker/actions?query=workflow%3ATest)) for latest test runs

### "Production" environment
- Put kafka ssl certificates into `certificates/` folder.
- Declare ENV variables in `.env` file. Please, see ENV variables below
```bash
$ make run_production
```

---

## Overview
### Project Structure
Two separate docker services with own Dockerfiles and build instructions: `consume` and `produce`.

There is also a service which is responsible for initializing database - `migrate`. 

They also have their own dependencies, because `produce` doesn't need database to generate messages

It's not optimal and I would have two different repos for each service, but I think that would be too much for this 
assignment. Also, it saves time doing DevOps work

- Service `consume` consists of: database session implementation, 
  migrations  logic, Kafka consumer listening to kafka topic

- Service `produce` consists of: Kafka producer, website crowler and content regext parser

### Database
Postgres is running locally for local and CI environments. 

For production environment Aiven's Postgres should be used

### Kafka
For testing environment `KafkaConsumer` and `KafkaProducer` are mocked. 

For production environment Aiven's Kafka should be used


### Docker
There are 3 compose files that can be used:
- docker-compose.yml - can be used for local development(local Postgres declared as db service). However, you need
working Kafka somewhere to run it
- docker-compose.prod.yml - "production" docker compose file. Please, don't forget to put Kafka ssl certificates into `certificates/`
folder and specify ENV variables
- docker-compose-ci.yml - a compose file for CI. Doesn't need neither env variables, nor Aiven kafka and postgres. Simply run `$make tests` to run tests

---

## Kafka certificates
Kafka certificates should be present in `certificates/`

**NOTE**: Rebuild container if you changed certificates in folder

---

## ENV Variables
In order to run project, ENV variables should be specified in `.env` file:
- KAFKA_HOST 
- KAFKA_TOPIC; default: metrics
- SITE_URLS; set sites you want to check; default: `https://google.com`
- WEBSITE_CONTENT_REGEX; regex to parse site content
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- POSTGRES_PORT
- POSTGRES_HOST

---

## What can be improved?
- Split into two repos
- Utilize Kafka+Zookeeper locally for smoother development process, so Aiven service will be used only in production
- If needed, expand migration in database, so users can write their SQL migrations and script `migrate.py` will execute them in dependant order by using revisions

---
