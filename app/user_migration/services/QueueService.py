import pika
import json
import os

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
EXCHANGE = os.getenv("EXCHANGE_NAME", "user_migration_exchange")

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
routing_keys_by_operation = {"TRANSFER_CITIZEN": "transferCitizen_queue", "CONFIRM_TRANSFER": "confirmCitizen_queue"}


class QueueService:

    @staticmethod
    def get_connection():
        return pika.BlockingConnection(parameters)

    @staticmethod
    def publish_message(message, operation):
        connection = QueueService.get_connection()
        channel = connection.channel()

        channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct', durable=True)

        #channel.queue_declare(queue=routing_keys_by_operation[operation], durable=True)
        #channel.queue_bind(exchange=EXCHANGE, queue=routing_keys_by_operation[operation],
        #                   routing_key=routing_keys_by_operation[operation])

        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=routing_keys_by_operation[operation],
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

        connection.close()
