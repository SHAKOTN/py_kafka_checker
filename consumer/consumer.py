import json
import logging
import os
import threading

from kafka import KafkaConsumer

from consumer.database import Session

logger = logging.getLogger(__name__)

def insert_to_database() -> None:
    pass

def consume_messages() -> None:
    logger.warning(f"Started listener process {threading.get_ident()}")
    kafka_consumer = KafkaConsumer(
        os.getenv('KAFKA_TOPIC'),
        bootstrap_servers=os.getenv('KAFKA_HOST'),
        enable_auto_commit=True,
        value_deserializer=lambda payload: json.loads(payload.decode('utf8')),
        group_id="metrics_consumer",
        security_protocol="SSL",
        # TODO: Move cert files to S3 or other storage. For now, leaving them here, but they are
        # TODO: added to .gitignore
        ssl_cafile="certificates/ca.pem",
        ssl_certfile="certificates/service.cert",
        ssl_keyfile="certificates/service.key"
    )
    with Session() as session:
        while True:
            for message in kafka_consumer:
                pass

# if __name__ == '__main__':
#     consume_messages()
