import os

from api import lesson, goal, user
from api.api import get_db_connection
from api.constants import NUMBER_KEY, ID_KEY, REASON_KEY
from butterfly.utils.utils import get_dir_of, load_file
import constants
from schema import User, Lesson, Goal, ActivityLesson, ActivityGoal


def _table_generator(config, action=None):
    connection = get_db_connection(config)
    engine = connection.ENGINE

    table_set = (User, Lesson, Goal, ActivityLesson, ActivityGoal)
    for table in table_set:
        _table_action = getattr(table.metadata, action)
        _table_action(engine)


def initialize_tables(config):
    """Populate the 'lesson', 'goal', default 'user' tables. Day-Zero operation

    :param config: config object
    :return: None
    """
    connection = get_db_connection(config)

    init_data_dir = os.path.join(get_dir_of(__file__), constants.INIT_DATA_DIR)
    lesson_contents = load_file(os.path.join(init_data_dir, constants.INIT_LESSON_JSON))
    goal_contents = load_file(os.path.join(init_data_dir, constants.INIT_GOAL_JSON))
    default_users = load_file(os.path.join(init_data_dir, constants.INIT_USER_JSON))

    def _create_goal(goal_i):
        goal_reason = goal_i.get(REASON_KEY)
        if goal_reason:
            goal_i[REASON_KEY] = lesson_number_mapping.get(goal_reason)
        goal.Goal.create(connection, **goal_i)

    [lesson.Lesson.create(connection, **_lesson) for _lesson in lesson_contents]
    lesson_number_mapping = dict([(_lesson.get(NUMBER_KEY), _lesson.get(ID_KEY))
                                  for _lesson in lesson.Lesson.get_all(connection)])
    [_create_goal(_goal) for _goal in goal_contents]
    [user.User.create(connection, **_user) for _user in default_users]


def update_tables(config):
    """Update the 'lesson', 'goal', default 'user' tables

    :param config: config object
    :return:
    """
    pass


def clean_tables(config):
    """Cleans the 'user', 'lesson', 'goal' table.
    Should be executed only if 'activity_lesson' and 'activity_goal' tables are empty

    :param config: config object
    :return: None
    """
    connection = get_db_connection(config)

    DEFAULT_USER_LIST = [constants.DEFAULT_ADMIN_USER, constants.DEFAULT_TEST_USER]

    [user.User.delete(connection, None, **{"name": _user}) for _user in DEFAULT_USER_LIST]
    [goal.Goal.delete(connection, _goal.get(ID_KEY)) for _goal in goal.Goal.get_all(connection)]
    [lesson.Lesson.delete(connection, _lesson.get(ID_KEY)) for _lesson in lesson.Lesson.get_all(connection)]


def register_tables(config):
    _table_generator(config, action=constants.DB_CREATE_ACTION)
    initialize_tables(config)


def unregister_tables(config):
    _table_generator(config, action=constants.DB_DROP_ACTION)
