from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_engine(connection_string):
    engine = create_engine(connection_string)
    return engine


def get_db_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session(autocommit=False, expire_on_commit=True)
    return session


class Table(object):
    """Base Class for DB APIs"""
    @classmethod
    def get_all(cls, engine):
        raise NotImplemented

    @classmethod
    def get(cls, engine, id_, **kwargs):
        raise NotImplemented

    @classmethod
    def create(cls, engine, **kwargs):
        raise NotImplemented

    @classmethod
    def update(cls, engine, id_, **kwargs):
        raise NotImplemented

    @classmethod
    def delete(cls, engine, id_, **kwargs):
        raise NotImplemented

    @staticmethod
    def row_object_to_dict(obj):
        obj_dict = obj.__dict__
        obj_dict.pop('_sa_instance_state')
        return obj_dict
