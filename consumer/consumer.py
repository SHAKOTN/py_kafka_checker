import json
import logging
import os
import threading

from kafka import KafkaConsumer

from consumer.database import Session
from consumer.message_validator import is_valid_consumer_message

logger = logging.getLogger(__name__)

def consume_messages() -> None:
    logger.warning(f"Started listener {threading.get_ident()}")
    kafka_consumer = KafkaConsumer(
        os.getenv('KAFKA_TOPIC', 'metrics'),
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
            logger.warning(f"Message received: {message.value}")
            if not is_valid_consumer_message(message.value):
                continue
            session.execute(
                "INSERT INTO website_metrics(url, content, response_time, code) VALUES (%s, %s, %s, %s)",
                (
                    message.value['url'],
                    message.value['content'],
                    message.value['response_time'],
                    message.value['code'])
            )
            session.commit()
