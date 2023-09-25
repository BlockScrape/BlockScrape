import pika
import json


def send_message(messages, connection, exchange_name):
    if connection.is_open:
        print("connection is open")
    else:
        print("connection is closed")
    channel = connection.channel()
    for message in messages:
        dumped_message = message.model_dump()
        print(f" [x] Sent '{dumped_message}'")
        publish_message = {'job_id': dumped_message['job_id'], 'result': json.dumps(dumped_message)}
        channel.basic_publish(exchange=exchange_name, routing_key='', body=json.dumps(publish_message))
    channel.close()
