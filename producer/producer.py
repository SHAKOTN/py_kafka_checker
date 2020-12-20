import json
import logging
import os
import threading
from time import sleep

from kafka import KafkaProducer

from producer.site_crawler import get_sites_metadata

logger = logging.getLogger(__name__)

def produce_messages() -> None:
    logger.warning(f"Started producer {threading.get_ident()}")
    kafka_producer = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_HOST'),
        security_protocol="SSL",
        # TODO: Move cert files to S3 or other storage. For now, leaving them here, but they are
        # TODO: added to .gitignore
        ssl_cafile="certificates/ca.pem",
        ssl_certfile="certificates/service.cert",
        ssl_keyfile="certificates/service.key",
        value_serializer=lambda data: json.dumps(data).encode('utf-8')
    )
    while True:
        send_message(kafka_producer)
        sleep(30)

def send_message(transport: KafkaProducer):
    sites_data = get_sites_metadata()
    if sites_data:
        for site_data in sites_data:
            transport.send(os.getenv("KAFKA_TOPIC", 'metrics'), value=site_data.__dict__)
