import pika
import json


def send_to_backend(type, queue, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',
        5672,
        'duc_voucher',
        pika.PlainCredentials('duc_voucher', 'duc_voucher'),
    ))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True, auto_delete=False,
                          exclusive=False)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(type=type),
    )
    connection.close()

    print('message sent to backend: {}'.format(message), flush=True)


def send_to_monitor():
    pass
