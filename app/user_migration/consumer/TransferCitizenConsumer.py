import json
import os
import pika
import sys

from app.user_migration.processors.TransferCitizenConsumerProcessor import TransferCitizenConsumerProcessor
from app.user_migration.services.QueueService import QueueService

EXCHANGE = os.getenv("EXCHANGE_NAME", "user_migration_exchange")
QUEUE_NAME = 'transferCitizen_queue'
RETRY_QUEUE_NAME = 'transferCitizen_retry_queue'
DLX_NAME = 'user_migration_dead_letter_exchange'
DLQ_NAME = 'dead_letter_transferCitizen_queue'

BASE_DELAY = 5000
MAX_RETRIES = 3

def callback(ch, method, properties, body):
    """
    Función de callback para procesar los mensajes de la cola.
    """
    try:
        message = json.loads(body)
        result = TransferCitizenConsumerProcessor.process(message)
        print(f"Processed message: {result}")

        # Acknowledge el mensaje después de procesarlo exitosamente
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}", file=sys.stderr)

        # Obtener el contador de reintentos desde los headers
        headers = properties.headers or {}
        retries = headers.get('x-retries', 0)
        retries += 1  # Incrementar el contador de reintentos

        if retries <= MAX_RETRIES:
            # Publicar el mensaje en la Cola de Reintentos con el contador actualizado
            ch.basic_publish(
                exchange=DLX_NAME,
                routing_key=RETRY_QUEUE_NAME,
                body=body,
                properties=pika.BasicProperties(
                    headers={'x-retries': retries},
                    delivery_mode=2  # Hacer que el mensaje sea persistente
                )
            )
            print(f"Requeued message to '{RETRY_QUEUE_NAME}' with retry {retries}")
        else:
            # Enviar el mensaje a la Dead Letter Queue
            ch.basic_publish(
                exchange=DLX_NAME,
                routing_key=DLQ_NAME,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2  # Hacer que el mensaje sea persistente
                )
            )
            print(f"Message sent to Dead Letter Queue after {MAX_RETRIES} retries")

        # Acknowledge el mensaje actual para evitar que quede bloqueado
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    """
    Inicia el consumidor de RabbitMQ.
    """
    connection = QueueService.get_connection()
    channel = connection.channel()

    # Configurar Prefetch Count para procesar un mensaje a la vez
    channel.basic_qos(prefetch_count=1)

    # Consumir mensajes con ACKs manuales
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    print(f"[*] Esperando mensajes en la cola '{QUEUE_NAME}'. Para salir presiona CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupción manual, cerrando consumidor...")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == '__main__':
    start_consumer()
