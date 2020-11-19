from argparse import ArgumentParser

import pika


def consume_message(channel, method, header, body):
    channel.basic_ack(method.delivery_tag)
    print(body)


def main():
    parser = ArgumentParser()
    parser.add_argument('--host', )
    parser.add_argument('--num_messages', type=int)
    args = parser.parse_args()

    host = args.host
    num_messages = args.num_messages

    credentials = pika.PlainCredentials("guest", "guest")
    conn_params = pika.ConnectionParameters(host, credentials=credentials)
    conn_broker = pika.BlockingConnection(conn_params)

    channel = conn_broker.channel()
    channel.exchange_declare(exchange="rabbit_task", type="topic",
                             passive=False, durable=True, auto_delete=False)
    message_properties = pika.BasicProperties()
    message_properties.content_type = "text/plain"
    for i in range(num_messages):
        message = f"Message_{i}"
        channel.basic_publish(body=message, exchange="rabbit_task",
                              properties=message_properties, routing_key="rabbit")


if __name__ == '__main__':
    main()
