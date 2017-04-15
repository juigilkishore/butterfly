from copy import deepcopy
from sqlalchemy.orm.exc import NoResultFound

from api import Table
from butterfly.utils.utils import get_utc_time, datetime_to_string
from butterfly.db import schema
from constants import USER_ID_KEY, LESSON_ID_KEY
from constants import COMPLETED_KEY, COMPLETED_AT_KEY, OPENED_AT_KEY
from lesson import Lesson
from user import User


class ActivityLesson(Table):
    @classmethod
    def get_all(cls, connection, **_filter):
        """Get all activity rows from 'activity_lesson' table

        :param connection: DB connection object
        :param _filter: AND filter dictionary
            {
                'user_id': <user-id>,
                'lesson_id': <lesson-id>,
                'completed': True
            }
        :return: list of activities
            [{
                'user_id': <user-id>,
                'lesson_id': <lesson-id>,
                'opened_at': <datetime>,
                'completed': True (or) False,
                'completed_at': <datetime>
            }]
        """
        session = connection.SESSION
        activity_list = list()
        try:
            activity_obj_list = (session.query(schema.ActivityLesson).filter_by(**_filter).all()
                                 if _filter else session.query(schema.ActivityLesson).all())
            for activity in activity_obj_list:
                activity_dict = cls.row_object_to_dict(activity)
                activity_dict[OPENED_AT_KEY] = datetime_to_string(activity_dict.get(OPENED_AT_KEY))
                activity_dict[COMPLETED_AT_KEY] = datetime_to_string(activity_dict.get(COMPLETED_AT_KEY))
                activity_list.append(activity_dict)
            activity_list = deepcopy(activity_list)
        except Exception as e:
            print "Exception occurred during querying (GET ALL) the activity_lesson table: %s" % e
        return activity_list

    @classmethod
    def get(cls, connection, id_, **_filter):
        """Get a single activity row from 'activity_lesson' table

        :param connection: DB connection object
        :param id_: None (always)
        :param _filter: AND filter dictionary
            {
                "user_id": <user-id>,
                "lesson_id": <lesson-id>
            }
        :return: activity details
            {
                'user_id': <user-id>,
                'lesson_id': <lesson-id>,
                'opened_at': <datetime>,
                'completed': True (or) False,
                'completed_at': <datetime>
            }
        """
        session = connection.SESSION
        activity = None
        try:
            activity_obj = session.query(schema.ActivityLesson).filter_by(**_filter).one()
            activity = cls.row_object_to_dict(activity_obj)
            activity[OPENED_AT_KEY] = datetime_to_string(activity.get(OPENED_AT_KEY))
            activity[COMPLETED_AT_KEY] = datetime_to_string(activity.get(COMPLETED_AT_KEY))
        except Exception as e:
            print "Exception occurred during querying (GET) the activity_lesson table: %s" % e
        return activity

    @classmethod
    def get_by_user_name(cls, connection, user_name, completed=None):
        """Get all activities of user_name from 'activity_lesson' table

        :param connection: DB connection object
        :param user_name: user name
        :param completed: status of the activity (True/False/None)
                True - returns all the completed lessons of user_name
                False - return all the in-progress lessons of user_name
                None - return all the lessons of user_name
        :return: list of activities of user_name
            [{
                'user_id': user_id,
                'lesson_id': <lesson-id>,
                'opened_at': <datetime>,
                'completed': True (or) False,
                'completed_at': <datetime>
            }]
        """
        user_id = User.get_user_id(connection, user_name)
        return cls.get_by_user_id(connection, user_id, completed=completed)

    @classmethod
    def get_by_user_id(cls, connection, user_id, completed=None):
        """Get all activities of user_id from 'activity_lesson' table

        :param connection: DB connection object
        :param user_id: user ID
        :param completed: status of the activity (True/False/None)
                True - returns all the completed lessons of user_id
                False - return all the in-progress lessons of user_id
                None - return all the lessons of user_id
        :return:  list of activities of user ID
            [{
                'user_id': user_id,
                'lesson_id': <lesson-id>,
                'opened_at': <datetime>,
                'completed': True (or) False,
                'completed_at': <datetime>
            }]
        """
        _filter = {USER_ID_KEY: user_id, COMPLETED_KEY: completed}
        if completed is None:
            _filter.pop(COMPLETED_KEY)
        return cls.get_all(connection, **_filter)

    @classmethod
    def get_by_lesson_name(cls, connection, lesson_name, completed=None):
        """Get all activities with lesson_name from 'activity_lesson' table of all users

        :param connection: DB connection object
        :param lesson_name: lesson name
        :param completed: status of the activity (True/False/None)
                True - returns all the completed lesson_name lessons of all users
                False - return all the in-progress lesson_name lessons of all user
                None - return all the lesson_name lessons of all users
        :return: list of activities of all users with lesson_name
            [{
                'user_id': <user-id>,
                'lesson_id': lesson_id,
                'opened_at': <datetime>,
                'completed': True (or) False,
                'completed_at': <datetime>
            }]
        """
        lesson_id = Lesson.get_lesson_id(connection, lesson_name)
        return cls.get_by_lesson_id(connection, lesson_id, completed=completed)

    @classmethod
    def get_by_lesson_id(cls, connection, lesson_id, completed=None):
        """Get all activities with lesson_id from 'activity_lesson' table of all users

        :param connection: DB connection object
        :param lesson_id: lesson ID
        :param completed: status of the activity (True/False/None)
                True - returns all the completed lesson_id lessons of all users
                False - return all the in-progress lesson_id lessons of all user
                None - return all the lesson_id lessons of all users
        :return: list of activities of all users with lesson_id
            [{
                'user_id': <user-id>,
                'lesson_id': lesson_id,
                'opened_at': <datetime>,
                'completed': True (or) False,
                'completed_at': <datetime>
            }]
        """
        _filter = {LESSON_ID_KEY: lesson_id, COMPLETED_KEY: completed}
        if completed is None:
            _filter.pop(COMPLETED_KEY)
        return cls.get_all(connection, **_filter)

    @classmethod
    def get_by_user_name_and_lesson_name(cls, connection, user_name, lesson_name):
        """Get an activity with user_name, lesson_name from 'activity_lesson' table

        :param connection: DB connection object
        :param user_name: user name
        :param lesson_name: lesson name
        :return: activity details
            {
                'user_id': user_id,
                'lesson_id': lesson_id,
                'opened_at': <datetime>,
                'completed': True (or) False,
                'completed_at': <datetime>
            }
        """
        user_id = User.get_user_id(connection, user_name)
        lesson_id = Lesson.get_lesson_id(connection, lesson_name)
        return cls.get_by_user_id_and_lesson_id(connection, user_id, lesson_id)

    @classmethod
    def get_by_user_id_and_lesson_id(cls, connection, user_id, lesson_id):
        """Get an activity with user_id, lesson_id from 'activity_lesson' table

        :param connection: DB connection object
        :param user_id: user ID
        :param lesson_id: lesson ID
        :return: activity details
            {
                'user_id': user_id,
                'lesson_id': lesson_id,
                'opened_at': <datetime>,
                'completed': True (or) False,
                'completed_at': <datetime>
            }
        """
        _filter = {USER_ID_KEY: user_id, LESSON_ID_KEY: lesson_id}
        return cls.get(connection, None, **_filter)

    @classmethod
    def create(cls, connection, **values):
        raise Exception("Use create_or_update call instead of create")

    @classmethod
    def update(cls, connection, id_, **values):
        raise Exception("Use create_or_update call instead of update")

    @classmethod
    def create_or_update(cls, connection, **values):
        """ Create or Update an activity row in 'activity_lesson' table

        :param connection: DB connection object
        :param values: activity_lesson payload
            {
                "user_id": <user-id>,
                "lesson_id": <lesson-id>
            }
        :return: boolean output
        """
        session = connection.SESSION
        create_or_update = True
        try:
            activity_obj = session.query(schema.ActivityLesson).filter_by(**values).one()
            setattr(activity_obj, COMPLETED_KEY, True)
            setattr(activity_obj, COMPLETED_AT_KEY, get_utc_time())
            session.commit()
        except NoResultFound as _:
            session.add(schema.ActivityLesson(**values))
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (INSERT/UPDATE) the activity_lesson table: %s" % e
            session.rollback()
            create_or_update = False
        finally:
            session.close()
        return create_or_update

    @classmethod
    def delete(cls, connection, id_, **_filter):
        """Delete an activity row in 'activity_lesson' table

        :param connection: DB connection object
        :param id_: None (always)
        :param _filter: AND filter dictionary
            {
                "user_id": <user-id>,
                "lesson_id": <lesson-id>
            }
        :return: boolean output
        """
        session = connection.SESSION
        deleted = True
        try:
            activity_obj = session.query(schema.ActivityLesson).filter_by(**_filter).one()
            session.delete(activity_obj)
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (DELETE) the activity_lesson table: %s" % e
            session.rollback()
            deleted = False
        finally:
            session.close()
        return deleted
