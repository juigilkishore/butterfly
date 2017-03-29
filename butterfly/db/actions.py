from api import api
from schema import User, Lesson, Goal, ActivityLesson, ActivityGoal


def _table_operator(config, action=None):
    connection_string = config.get("Database").get("connection")
    engine = api.get_db_engine(connection_string)

    table_set = (User, Lesson, Goal, ActivityLesson, ActivityGoal)
    for table in table_set:
        _table_action = getattr(table.metadata, action)
        _table_action(engine)


def initialize_tables(config):
    connection_string = config.get("Database").get("connection")
    api.Table.set_connection_string(connection_string)
    # TODO(juigil): Populate the lesson and goal tables


def register_tables(config):
    _table_operator(config, action="create_all")
    initialize_tables(config)


def unregister_tables(config):
    _table_operator(config, action="drop_all")
