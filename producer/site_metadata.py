from dataclasses import dataclass


@dataclass
class SiteMetadata:
    """
    Container class for KafkaProducer message data
    Validation and custom serialization can be added here
    """
    url: str
    content: str
    response_time: float
    code: int
