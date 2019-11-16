import datetime
import sqlalchemy
from enum import Enum
from datetime import datetime
from conf import get_logger


logger = get_logger('db_utils')

def connect(user, password, database_name, host='localhost', port=5432):
    """Returns a connection and a metadata object"""
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, database_name)
    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    return con, meta


def get_id(session, label: str):
    """ Get id of a person by a label """
    id = None
    query = f"""SELECT stud_id FROM label_to_id WHERE label='{label}' LIMIT 1;"""
    result = session.execute(query)
    session.close()
    for row in result:
        id: int = row[0]
        break
    return id

def get_course_id_by_name(session, course_name):
    id = None
    query = f"""SELECT course_id FROM course WHERE course_name='{course_name}';"""
    result = session.execute(query)
    session.close()
    for row in result:
        id: int = row[0]
        break
    return id

def add_course_session(session, course_name: str, date: str):
    course_date_id = None
    course_id = get_course_id_by_name(session, course_name)
    if course_id is not None:
        select_query = \
        f"""SELECT id
            FROM course_date
            WHERE course_id={course_id} AND date_held='{date}'
        """
        result = session.execute(select_query)
        for row in result:
            course_date_id: int = row[0]
            break
        if course_date_id is not None:
            session.close()
            return course_date_id
        insert_query = \
        f"""
            INSERT INTO course_date(course_id, date_held)
            SELECT {course_id}, '{date}'
            RETURNING id;
        """
        result = session.execute(insert_query)
        session.commit()
        session.close()
        for row in result:
            course_date_id: int = row[0]
            break
        return course_date_id

def check_student_at_course_session(session, stud_label: str, course_name: str, date: str) -> bool:
    """Update student_course_date table"""
    # logger.info(f"label={stud_label}, course_name={course_name}, date={date}")
    stud_id: int = get_id(session, stud_label)
    if stud_id is not None:
        course_date_id: int = add_course_session(session, course_name, date)
        insert_query = \
        f"""
            INSERT INTO student_course_date(course_date_id, stud_id)
            VALUES ({course_date_id}, {stud_id});
        """
        try:
            result = session.execute(insert_query)
            session.commit()
            # logger.info(f"{stud_label}:{stud_id} has been checked at {course_name} at {date}")
            return True
        except sqlalchemy.exc.IntegrityError as ie:
            # logger.error(f'{ie}')
            # logger.info(f"{stud_label}:{stud_id} has already been checked at {course_name} at {date}")
            return False
        finally:
            # logger.info("Closing session")
            session.close()

class Course(Enum):
    DL = "Deep Learning"
    DM = "Data Mining and Decision Support"
    AS = "Astronomy 1"


if __name__ == '__main__':
    from conf import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER
    from sqlalchemy.orm import sessionmaker

    """ Create a session with the Postgre database """
    con, db_meta = connect(user=POSTGRES_USER,
                          password=POSTGRES_PASSWORD,
                          database_name=POSTGRES_DB,
                          host=POSTGRES_HOST,
                          port=POSTGRES_PORT)

    Session = sessionmaker(bind=con)
    session = Session()

    # course_id = get_course_id_by_name(session, 'Astronomy 1')
    # logger.info(course_id)
    # course_date_id: int = add_course_session(session, 'Deep Learning', '2019-12-13')
    # logger.info(course_date_id)

    label = 'aslan'
    course = Course.DM.value
    date = str(datetime.utcnow().date())
    s = check_student_at_course_session(session=session, stud_label=label, course_name=course, date=date)
    logger.info(s)
