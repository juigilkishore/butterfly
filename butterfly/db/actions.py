import api
from schema import User, Lesson, Goal, ActivityLesson, ActivityGoal


def _table_operator(config, action=None):
    connection_string = config.get("Database").get("connection")
    engine = api.get_db_engine(connection_string)

    table_set = (User, Lesson, Goal, ActivityLesson, ActivityGoal)
    for table in table_set:
        _table_action = getattr(table.metadata, action)
        _table_action(engine)


def register_tables(config):
    _table_operator(config, action="create_all")


def unregister_tables(config):
    _table_operator(config, action="drop_all")


def initialize_tables():
    pass
