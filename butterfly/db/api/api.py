from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from butterfly.utils.utils import singleton


@singleton
class Connection(object):
    """Database Connection class defines db engine and db session"""

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.ENGINE = self._get_db_engine(self.connection_string)
        self.SESSION = self._get_db_session(self.ENGINE)

    def _get_db_engine(self, connection_string):
        engine = create_engine(connection_string)
        return engine

    def _get_db_session(self, engine):
        session_maker = sessionmaker(bind=engine)
        session = session_maker(autocommit=False, expire_on_commit=False)
        return session


def get_db_connection(config):
    connection_string = config.get("Database").get("connection")
    connection = Connection(connection_string)
    return connection


class Table(object):
    """Base Class for DB APIs"""

    @classmethod
    def get_all(cls, connection, **_filter):
        raise NotImplemented

    @classmethod
    def get(cls, connection, id_, **_filter):
        raise NotImplemented

    @classmethod
    def create(cls, connection, **values):
        raise NotImplemented

    @classmethod
    def update(cls, connection, id_, **values):
        raise NotImplemented

    @classmethod
    def delete(cls, connection, id_, **_filter):
        raise NotImplemented

    @staticmethod
    def row_object_to_dict(obj):
        """converts the DB table object to dictionary

        :param obj: object
        :return: dictionary of DB table object
        """
        obj_dict = obj.__dict__
        obj_dict.pop('_sa_instance_state')
        return obj_dict
