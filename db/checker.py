from datetime import datetime
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from conf import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER
from conf import get_logger
from db_utils import connect, get_id
from rmq_utils import get_channel
from utils import Face, FaceGrouping

logger = get_logger('checker')

""" Create a session with the Postgre database """
con, db_meta = connect(user=POSTGRES_USER,
                      password=POSTGRES_PASSWORD,
                      database_name=POSTGRES_DB,
                      host=POSTGRES_HOST,
                      port=POSTGRES_PORT)

Session = sessionmaker(bind=con)
session = Session()

""" Create a channel to RabbitMQ """
channel = get_channel()

""" Create a FaceGrouping """
face_grouping = FaceGrouping(threshold=0.5)

""" Message handler """
def message_handler(ch, method, properties, body):
    msg = json.loads(body)
    task = msg.get('task')
    if task == 'quit':
        logger.info("Quitting...")
        """ Send the best labels to another queue? """
        best_labels = face_grouping.best_labels()
        logger.info(f"Best labels: {best_labels}")
        ch.basic_publish(exchange='', routing_key='best_labels', body=json.dumps({
            "task": 'best_labels',
            "labels": list(best_labels),
            'date': str(datetime.utcnow().date()),
            "timestamp": str(datetime.utcnow())
        }))
        channel.stop_consuming()
    if task == 'prediction':
        index: int = msg.get('index')
        label: str = msg.get('label')
        face_bb: list = msg.get('face_region')
        """ Get id of a student """
        id: int = get_id(session, label)
        if id is not None:
            # logger.info(f"ID: {id}, Label: {label}, Face Region: {face_bb}, Index: {index}")
            face = Face(id, label, face_bb)
            logger.info(face)
            face_grouping.merge_face(face)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_reading(channel, handler = message_handler, queue: str = 'face_preds'):
    """ Start consuming from RabbitMQ channel """
    logger.info(f"Started consuming from queue {queue}")
    channel.basic_consume(on_message_callback=handler, queue=queue, auto_ack=False)
    channel.start_consuming()

if __name__ == '__main__':
    start_reading(channel)
