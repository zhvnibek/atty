from datetime import datetime
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker, relationship

from conf import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER
from conf import get_logger
from db_utils import connect, get_id, check_student_at_course_session
from rmq_utils import get_channel

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


""" Message handler """
def message_handler(ch, method, properties, body):
    msg = json.loads(body)
    task = msg.get('task')
    if task == 'best_labels':
        """Save the best labels into the attendance table"""
        labels: list = msg.get('labels')
        ts: str = msg.get('timestamp')
        date: str = msg.get('date')
        course_id: int = msg.get('course_id')
        for label in labels:
            if check_student_at_course_session( \
                    session=session, stud_label=label, \
                    course_id=course_id, date=date):
                logger.info(f"{label} has been checked at {course_id} at {ts}")
            else:
                logger.info(f"{label} has already been checked at {course_id}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # else:
            # logger.error("Something went wrong while checking the recognized students!")
            # ch.basic_nack(delivery_tag=method.delivery_tag)

    # ch.basic_ack(delivery_tag=method.delivery_tag)

def start_reading(channel, handler = message_handler, queue: str = 'best_labels'):
    """ Start consuming from RabbitMQ channel """
    logger.info(f"Started consuming from queue {queue}")
    channel.basic_consume(on_message_callback=handler, queue=queue, auto_ack=False)
    channel.start_consuming()

if __name__ == '__main__':
    start_reading(channel)
