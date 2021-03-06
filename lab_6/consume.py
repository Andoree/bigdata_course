from argparse import ArgumentParser

import pika


def consume_message(channel, method, header, body):
    channel.basic_ack(method.delivery_tag)
    print(body)


def main():
    parser = ArgumentParser()
    parser.add_argument('--host', )
    args = parser.parse_args()

    host = args.host

    credentials = pika.PlainCredentials("user", "user")
    conn_params = pika.ConnectionParameters(host, credentials=credentials)
    conn_broker = pika.BlockingConnection(conn_params)

    channel = conn_broker.channel()
    channel.exchange_declare(exchange="rabbit_task", exchange_type="topic",
                             passive=False, durable=True, auto_delete=False)
    channel.queue_declare(queue="some_queue")
    channel.queue_bind(queue="some_queue", exchange="rabbit_task", routing_key="rabbit")
    channel.basic_consume(queue="some_queue", consumer_tag="consumer_tag", on_message_callback=consume_message)
    channel.start_consuming()


if __name__ == '__main__':
    main()
