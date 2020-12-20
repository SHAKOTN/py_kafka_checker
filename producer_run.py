import logging
from producer.producer import produce_messages

logging.basicConfig(level=logging.WARNING)

if __name__ == '__main__':
    produce_messages()
