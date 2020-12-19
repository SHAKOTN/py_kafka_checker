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
    transport = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_HOST'),
        security_protocol="SSL",
        ssl_cafile="certificates/ca.pem",
        ssl_certfile="certificates/service.cert",
        ssl_keyfile="certificates/service.key",
        value_serializer=lambda data: json.dumps(data).encode('utf-8')
    )
    while True:
        sites_data = get_sites_metadata()
        if sites_data:
            for site_data in sites_data:
                transport.send(os.getenv("KAFKA_TOPIC"), value=site_data.__dict__)
        sleep(30)