from api import get_db_session, Table
from butterfly.db import schema


class Lesson(Table):
    @classmethod
    def get_all(cls):
        pass

    @classmethod
    def get(cls, id_, **kwargs):
        pass

    @classmethod
    def create(cls, **kwargs):
        pass

    @classmethod
    def update(cls, id_, **kwargs):
        pass

    @classmethod
    def delete(cls, id_, **kwargs):
        pass
