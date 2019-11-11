import pika
from conf import RMQ_HOST, RMQ_PORT, RMQ_USER, RMQ_PASSWORD
from conf import get_logger

logger = get_logger("rmq_utils")

params = pika.ConnectionParameters(
    host=RMQ_HOST,
    port=int(RMQ_PORT),
    credentials=pika.credentials.PlainCredentials(RMQ_USER, RMQ_PASSWORD),
    # heartbeat_interval=int(rmq_heartbeat),
)


def get_channel(params = params, prefetch_count: int = 1):
    """ Connect to RabbitMQ and return a channel """
    connection = pika.BlockingConnection(parameters=params)
    channel = connection.channel()
    channel.basic_qos(prefetch_count=prefetch_count)

    return channel

    # channel.basic_consume(on_message_callback=message_handler, queue='face_preds', auto_ack=False)
    # channel.start_consuming()
