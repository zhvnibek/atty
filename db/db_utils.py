import datetime
import sqlalchemy
from sqlalchemy.orm import sessionmaker, relationship

from conf import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER
from conf import get_logger

logger = get_logger('postgre_to_neo')

def connect(user, password, database_name, host='localhost', port=5432):
    """Returns a connection and a metadata object"""
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, database_name)
    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    return con, meta

con, db_meta = connect(user=POSTGRES_USER,
                      password=POSTGRES_PASSWORD,
                      database_name=POSTGRES_DB,
                      host=POSTGRES_HOST,
                      port=POSTGRES_PORT)

Session = sessionmaker(bind=con)
session = Session()

def test():
    date = datetime.datetime.utcnow().date()
    query = """SELECT count(*) FROM student;"""
    # query = f"""INSERT INTO student (fullname, email, created_on) VALUES ('Zhanibek Darimbekov', 'zhanibek.darimbekov@mail.ru', '{date}');"""
    result = session.execute(query)
    session.close()
    for row in result:
        print(row)

if __name__ == '__main__':
    test()
