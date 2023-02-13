from json import dumps
from kafka import KafkaProducer

class Kafka:
    def __init__(self, servers, api):
        self.my_producer = KafkaProducer(bootstrap_servers=servers,
                    api_version=api,
                    value_serializer=lambda x: dumps(x).encode('utf-8'))

    def get_producer(self):
        return self.my_producer