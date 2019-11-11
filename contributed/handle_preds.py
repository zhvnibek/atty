import pika
import json
import redis

import logging
logging.getLogger("pika").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s: %(levelname)s %(message)s')

def get_logger(name: str):
    return logging.getLogger(name)

logger = get_logger("handle_preds")

rmq_host = 'localhost'
rmq_port = 5672
rmq_user = 'guest'
rmq_password = 'guest'

def queue_with_dlx(ch, q_name):
    """creates pair queue+dead_letters_queue"""
    q_dlx_name = 'dlx_' + q_name
    ch.queue_declare(queue=q_name, durable=True,
                     arguments={'x-dead-letter-exchange': '',
                                'x-dead-letter-routing-key': q_dlx_name,
                                'x-queue-mode': 'lazy'})

    ch.queue_declare(queue=q_dlx_name, durable=True,
                     arguments={'x-message-ttl': 7200000,
                                'x-dead-letter-exchange': '',
                                'x-dead-letter-routing-key': q_name,
                                'x-queue-mode': 'lazy'})

def send_labels(faces, time_window: int = 30):
    if faces is not None:
        for i, face in enumerate(faces):
            label = face.name
            face_bb = face.bounding_box.astype(int).tolist()
            if label is not None:
                """ TODO:
                1. Check in redis whether the label was appeared
                in previous frames in last x seconds
                    1.1. If True: skip the label
                    1.2. If False: send it to the RabbitMQ

                """
                if labels_cache.get(label) is not None:
                    # logger.info("The label has already checked recently..")
                    continue

                logger.info(f"Index: {i}, Label: {label}, Bounding Box: {face_bb}")

                channel.basic_publish(exchange='', routing_key='face_preds', body=json.dumps({
                    "task": 'prediction',
                    "face_region": face_bb,
                    "label": label,
                    "index": i
                }))
                labels_cache.set(label, 1, ex=time_window)

""" Redis """
labels_cache = redis.Redis(host='localhost', port=6379, db=0)

""" RabbitMQ """
logger.info("pika: connecting to {}:{}".format(rmq_host, rmq_port))
params = pika.ConnectionParameters(
    host=rmq_host,
    port=int(rmq_port),
    credentials=pika.credentials.PlainCredentials(rmq_user, rmq_password),
    # heartbeat_interval=int(rmq_heartbeat),
)

connection = pika.BlockingConnection(parameters=params)
channel = connection.channel()

channel.basic_qos(prefetch_count=1)

queue_with_dlx(channel, 'face_preds')
