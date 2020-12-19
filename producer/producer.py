import os

import json
from kafka import KafkaProducer


def produce_messages() -> None:
    transport = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_HOST'),
        security_protocol="SSL",
        ssl_cafile="certificates/ca.pem",
        ssl_certfile="certificates/service.cert",
        ssl_keyfile="certificates/service.key",
        value_serializer=lambda data: json.dumps(data).encode('utf-8')
    )