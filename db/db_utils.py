import datetime
import sqlalchemy
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
    query = f"""SELECT stud_id FROM label_to_id WHERE label='{label}' LIMIT 1;"""
    result = session.execute(query)
    session.close()
    id = None
    for row in result:
        id: int = row[0]
        break
    return id

if __name__ == '__main__':
    pass
