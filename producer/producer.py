import os

import json
from time import sleep

from kafka import KafkaProducer

from producer.site_crawler import get_site_metadata


def produce_messages() -> None:
    transport = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_HOST'),
        security_protocol="SSL",
        ssl_cafile="certificates/ca.pem",
        ssl_certfile="certificates/service.cert",
        ssl_keyfile="certificates/service.key",
        value_serializer=lambda data: json.dumps(data).encode('utf-8')
    )
    while True:
        site_data = get_site_metadata()
        if site_data:
            transport.send(os.getenv("KAFKA_TOPIC"), value=site_data.__dict__)
        sleep(60)