from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_engine(connection_string):
    engine = create_engine(connection_string)
    return engine


def get_db_session(engine):
    session_maker = sessionmaker(bind=engine)
    session = session_maker(autocommit=False, expire_on_commit=True)
    return session


class Table(object):
    """Base Class for DB APIs"""

    CONNECTION_STRING = None

    @classmethod
    def set_connection_string(cls, connection_string):
        cls.CONNECTION_STRING = connection_string

    @classmethod
    def get_connection_string(cls):
        return cls.CONNECTION_STRING

    @classmethod
    def get_all(cls, **kwargs):
        raise NotImplemented

    @classmethod
    def get(cls, id_, **kwargs):
        raise NotImplemented

    @classmethod
    def create(cls, **kwargs):
        raise NotImplemented

    @classmethod
    def update(cls, id_, **kwargs):
        raise NotImplemented

    @classmethod
    def delete(cls, id_, **kwargs):
        raise NotImplemented

    @staticmethod
    def row_object_to_dict(obj):
        obj_dict = obj.__dict__
        obj_dict.pop('_sa_instance_state')
        return obj_dict
