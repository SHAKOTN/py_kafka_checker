import json
import logging
import os
import threading
from typing import Dict

from kafka import KafkaConsumer

from consumer.database import Session

logger = logging.getLogger(__name__)

def insert_metadata_to_db(message: Dict) -> None:
    pass

def consume_messages() -> None:
    logger.warning(f"Started listener process {threading.get_ident()}")
    kafka_consumer = KafkaConsumer(
        os.getenv('KAFKA_TOPIC'),
        bootstrap_servers=os.getenv('KAFKA_HOST'),
        enable_auto_commit=True,
        value_deserializer=lambda data: json.loads(data.decode('utf8')),
        group_id="metrics_consumer",
        security_protocol="SSL",
        # TODO: Move cert files to S3 or other storage. For now, leaving them here, but they are
        # TODO: added to .gitignore
        ssl_cafile="certificates/ca.pem",
        ssl_certfile="certificates/service.cert",
        ssl_keyfile="certificates/service.key"
    )

    # Acquire session so it will stay alive while fetching new messages
    with Session() as session:
        for message in kafka_consumer:
            session.execute(
                "INSERT INTO website_metrics(url, content, response_time, code) VALUES (%s, %s, %s, %s)",
                (message['url'], message['content'], message['response_time'], message['code'])
            )
            session.commit()
