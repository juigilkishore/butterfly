from ast import literal_eval
from copy import deepcopy
from sqlalchemy.orm.exc import NoResultFound

from api import Table
from butterfly.utils.utils import get_utc_time
from butterfly.db import schema
from constants import USER_ID_KEY, GOAL_ID_KEY, COUNT_KEY, FREQUENCY_KEY
from constants import COMPLETED_KEY, COMPLETED_ON_KEY, TIME_FORMAT, LAST_UPDATED_AT_KEY
from goal import Goal
from user import User


class ActivityGoal(Table):
    @classmethod
    def get_all(cls, connection, **_filter):
        """Get all activity rows from 'activity_goal' table

        :param connection: DB connection object
        :param _filter: AND filter dictionary
            {
                'user_id': <user-id>,
                'goal_id': <goal-id>,
                'frequency': <number-of-times-goal-performed> (3),
                'last_updated': <datetime>,
                'completed_on': {1: <datetime>, 2: <datetime>, 3: <datetime>},
                'completed': True (or) False
            }
        :return: list of activities
            [{
                'user_id': <user-id>,
                'goal_id': <goal-id>,
                'frequency': <number-of-times-goal-performed> (3),
                'last_updated': <datetime>,
                'completed_on': {1: <datetime>, 2: <datetime>, 3: <datetime>},
                'completed': True (or) False
            }]
        """
        session = connection.SESSION
        activity_list = list()
        try:
            activity_obj_list = (session.query(schema.ActivityGoal).filter_by(**_filter).all()
                                 if _filter else session.query(schema.ActivityGoal).all())
            for activity in activity_obj_list:
                activity_list.append(cls.row_object_to_dict(activity))
            activity_list = deepcopy(activity_list)
        except Exception as e:
            print "Exception occurred during querying (GET ALL) the activity_goal table: %s" % e
        return activity_list

    @classmethod
    def get(cls, connection, id_, **_filter):
        """Get a single activity row from 'activity_goal' table

        :param connection: DB connection object
        :param id_: None (always)
        :param _filter: AND filter dictionary
            {
                'user_id': <user-id>,
                'goal_id': <goal-id>
            }
        :return: activity details
            {
                'user_id': <user-id>,
                'goal_id': <goal-id>,
                'frequency': <number-of-times-goal-performed> (3),
                'last_updated': <datetime>,
                'completed_on': {1: <datetime>, 2: <datetime>, 3: <datetime>},
                'completed': True (or) False
            }
        """
        session = connection.SESSION
        activity = None
        try:
            activity_obj = session.query(schema.ActivityGoal).filter_by(**_filter).one()
            activity = cls.row_object_to_dict(activity_obj)
        except Exception as e:
            print "Exception occurred during querying (GET) the activity_goal table: %s" % e
        return activity

    @classmethod
    def get_by_user_name(cls, connection, user_name, completed=None):
        """Get all activities of user_name from 'activity_goal' table

        :param connection: DB connection object
        :param user_name: user name
        :param completed: status of the activity (True/False/None)
                True - returns all the completed goals of user_name
                False - return all the in-progress goals of user_name
                None - return all the goals of user_name
        :return: list of activities of user_name
            [{
                'user_id': <user-id>,
                'goal_id': <goal-id>,
                'frequency': <number-of-times-goal-performed> (3),
                'last_updated': <datetime>,
                'completed_on': {1: <datetime>, 2: <datetime>, 3: <datetime>},
                'completed': True (or) False
            }]
        """
        user_id = User.get_user_id(connection, user_name)
        return cls.get_by_user_id(connection, user_id, completed=completed)

    @classmethod
    def get_by_user_id(cls, connection, user_id, completed=None):
        """Get all activities of user_id from 'activity_goal' table

        :param connection: DB connection object
        :param user_id: user ID
        :param completed: status of the activity (True/False/None)
                True - returns all the completed goals of user_id
                False - return all the in-progress goals of user_id
                None - return all the goals of user_id
        :return: list of activities of user_id
            [{
                'user_id': user_id,
                'goal_id': <goal-id>,
                'frequency': <number-of-times-goal-performed> (3),
                'last_updated': <datetime>,
                'completed_on': {1: <datetime>, 2: <datetime>, 3: <datetime>},
                'completed': True (or) False
            }]
        """
        _filter = {USER_ID_KEY: user_id, COMPLETED_KEY: completed}
        if completed is None:
            _filter.pop(COMPLETED_KEY)
        return cls.get_all(connection, **_filter)

    @classmethod
    def get_by_goal_name(cls, connection, goal_name, week, completed=None):
        """Get all activities with goal_name from 'activity_goal' table on <week> of all users

        :param connection: DB connection object
        :param goal_name: goal name
        :param week: week number
        :param completed: status of the activity (True/False/None)
                True - returns all the completed goal_name goals of all users
                False - return all the in-progress goal_name goals of all user
                None - return all the goals_name goals of all users
        :return: list of activities of all users with goal_name
            [{
                'user_id': <user-id>,
                'goal_id': <goal-id>,
                'frequency': <number-of-times-goal-performed> (3),
                'last_updated': <datetime>,
                'completed_on': {1: <datetime>, 2: <datetime>, 3: <datetime>},
                'completed': True (or) False
            }]
        """
        goal_id = Goal.get_goal_id(connection, goal_name, week)
        return cls.get_by_goal_id(connection, goal_id, completed=completed)

    @classmethod
    def get_by_goal_id(cls, connection, goal_id, completed=None):
        """Get all activities with goal_id from 'activity_goal' table of all users

        :param connection: DB connection object
        :param goal_id: goal ID
        :param completed: status of the activity (True/False/None)
                True - returns all the completed goal_id goals of all users
                False - return all the in-progress goal_id goals of all user
                None - return all the goals_id goals of all users
        :return: list of activities of all users with goal_id
            [{
                'user_id': <user-id>,
                'goal_id': goal_id,
                'frequency': <number-of-times-goal-performed> (3),
                'last_updated': <datetime>,
                'completed_on': {1: <datetime>, 2: <datetime>, 3: <datetime>},
                'completed': True (or) False
            }]
        """
        _filter = {GOAL_ID_KEY: goal_id, COMPLETED_KEY: completed}
        if completed is None:
            _filter.pop(COMPLETED_KEY)
        return cls.get_all(connection, **_filter)

    @classmethod
    def create(cls, connection, **values):
        raise Exception("Use create_or_update call instead of create")

    @classmethod
    def update(cls, connection, id_, **values):
        raise Exception("Use create_or_update call instead of update")

    @classmethod
    def create_or_update(cls, connection, **values):
        """Create or Update an activity row in 'activity_goal' table

        :param connection: DB connection object
        :param values: activity_goal payload
            {
                'user_id': <user-id>,
                'goal_id': <goal-id>,
            }
        :return: boolean output
        """
        session = connection.SESSION
        create_or_update = True
        try:
            activity_obj = session.query(schema.ActivityGoal).filter_by(**values).one()
            goal_count = Goal.get(connection, values.get(GOAL_ID_KEY)).get(COUNT_KEY)

            if goal_count < activity_obj.frequency + 1:
                raise Exception("Reached the required goal count")

            setattr(activity_obj, FREQUENCY_KEY, activity_obj.frequency + 1)
            completed_on = literal_eval(activity_obj.completed_on)
            completed_on[str(activity_obj.frequency)] = get_utc_time().strftime(TIME_FORMAT)
            setattr(activity_obj, COMPLETED_ON_KEY, completed_on)
            setattr(activity_obj, LAST_UPDATED_AT_KEY, get_utc_time())

            if goal_count == activity_obj.frequency:
                setattr(activity_obj, COMPLETED_KEY, True)
            session.commit()
        except NoResultFound as _:
            values[COMPLETED_ON_KEY] = dict([(str(1), get_utc_time().strftime(TIME_FORMAT))])
            session.add(schema.ActivityGoal(**values))
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (INSERT/UPDATE) the activity_goal table: %s" % e
            session.rollback()
            create_or_update = False
        finally:
            session.close()
        return create_or_update

    @classmethod
    def delete(cls, connection, id_, **_filter):
        """Delete an activity row in 'activity_goal' table

        :param connection: DB connection object
        :param id_: None (always)
        :param _filter: AND filter dictionary
        :return: boolean output
        """
        session = connection.SESSION
        deleted = True
        try:
            activity_obj = session.query(schema.ActivityGoal).filter_by(**_filter).one()
            session.delete(activity_obj)
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (DELETE) the activity_goal table: %s" % e
            session.rollback()
            deleted = False
        finally:
            session.close()
        return deleted
