from copy import deepcopy

from api import Table
from butterfly.db import schema
from constants import NAME_KEY, ID_KEY, WEEK_KEY, COUNT_KEY


class Goal(Table):
    @classmethod
    def get_all(cls, connection, **_filter):
        """Get all goal rows in 'goal' table

        :param connection: DB connection object
        :param _filter: AND filter dictionary
            {
                'name': <goal-name>,
                'description': <goal-description>,
                'reason': <lesson-id> (or) None,
                'week': <week-number>,
                'count': <number-of-counts-of-goal>
            }
        :return: List of goal details
            [
            {
                'name': 'Walk',
                'description': 'Walk for 15 minutes for at least 3 days',
                'week': 2,
                'count': 3,
                'reason': 'a97196c9-ead8-4e6f-8b0c-a76fbefaafa0',
                'effect': {
                    "calories_burnt": 75,
                    "healthy_calories_consumed": None,
                     "unhealthy_calories_avoided": None
                },
                'id': '0a32b6ec-79c0-4149-a253-838c72bdd71c'}
            ]
        """
        session = connection.SESSION
        goal_list = list()
        try:
            goal_obj_list = (session.query(schema.Goal).filter_by(**_filter).all()
                             if _filter else session.query(schema.Goal).all())
            for goal in goal_obj_list:
                goal_list.append(cls.row_object_to_dict(goal))
            goal_list = deepcopy(goal_list)
        except Exception as e:
            print "Exception occurred during querying (GET ALL) the goal table: %s" % e
        return goal_list

    @classmethod
    def get(cls, connection, goal_id, **_filter):
        """Get a single goal row in 'goal' table

        _filter is ignored if goal_id is provided

        :param connection: DB connection object
        :param goal_id: goal ID
        :param _filter: AND filter dictionary
            {
                'name': <goal-name>,
                'description': <goal-description>,
                'reason': <lesson-id> (or) None,
                'week': <week-number>,
                'count': <number-of-counts-of-goal>
            }
        :return:
            {
                'name': 'Walk',
                'description': 'Walk for 15 minutes for at least 3 days',
                'week': 2,
                'count': 3,
                'reason': 'a97196c9-ead8-4e6f-8b0c-a76fbefaafa0',
                'effect': {
                    "calories_burnt": 75,
                    "healthy_calories_consumed": None,
                     "unhealthy_calories_avoided": None
                },
                'id': '0a32b6ec-79c0-4149-a253-838c72bdd71c'}
        """
        session = connection.SESSION
        goal = None
        try:
            goal_obj = (session.query(schema.Goal).filter_by(id=goal_id).one()
                        if goal_id else
                        session.query(schema.Goal).filter_by(**_filter).one())
            goal = deepcopy(cls.row_object_to_dict(goal_obj))
        except Exception as e:
            print "Exception occurred during querying (GET) the goal table: %s" % e
        return goal

    @classmethod
    def get_goal_id(cls, connection, goal_name, week):
        """Get the goal ID from goal name

        :param connection: DB connection object
        :param goal_name: goal name
        :param week: week number
        :return: goal ID
        """
        goal = cls.get(connection, None, **{NAME_KEY: goal_name, WEEK_KEY: week})
        return goal.get(ID_KEY)

    @classmethod
    def get_goal_from_week(cls, connection, week_start, week_end):
        """Get all goals from 'goal' table between weeks week_start and week_end

        :param connection: DB connection object
        :param week_start: start week-number
        :param week_end: end week-number
        :return: list of goal details
        """
        session = connection.SESSION
        goal_list = list()
        try:
            goal_obj_list = session.query(schema.Goal).filter(
                schema.Goal.week >= week_start,
                schema.Goal.week <= week_end).all()
            for goal in goal_obj_list:
                goal_list.append(cls.row_object_to_dict(goal))
            goal_list = deepcopy(goal_list)
        except Exception as e:
            print "Exception occurred during querying (GET ALL) the goal table: %s" % e
        return goal_list

    @classmethod
    def create(cls, connection, **values):
        """Create a goal row in 'goal' table

        :param connection: DB connection object
        :param values: goal payload
            {
                'name': 'Walk',
                'description': 'Walk for 15 minutes for at least 3 days',
                'week': 2,
                'count': 3,
                'reason': 'a97196c9-ead8-4e6f-8b0c-a76fbefaafa0' (or) None,
                'effect': {
                    "calories_burnt": 75,
                    "healthy_calories_consumed": None,
                     "unhealthy_calories_avoided": None
                }
            }
        :return: boolean output
        """
        session = connection.SESSION
        created = True
        try:
            session.add(schema.Goal(**values))
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (INSERT) the goal table: %s" % e
            session.rollback()
            created = False
        finally:
            session.close()
        return created

    @classmethod
    def update(cls, connection, goal_id, **values):
        """Update a single goal row in 'goal' table

        :param connection: DB connection object
        :param goal_id: goal ID
        :param values: new goal payload
            {
                'name': 'Walk-New',
                'description': 'Walk for 20 minutes for at least 5 days',
                'week': 5,
                'count': 4
            }
        :return: boolean output
        """
        session = connection.SESSION
        updated = True
        try:
            if not goal_id:
                raise Exception("goal ID is required for update operation")
            goal_obj = session.query(schema.Goal).filter_by(id=goal_id).one()
            [setattr(goal_obj, attr, new_val) for attr, new_val in values.iteritems()]
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (UPDATE) the goal table: %s" % e
            session.rollback()
            updated = False
        finally:
            session.close()
        return updated

    @classmethod
    def delete(cls, connection, goal_id, **_filter):
        """Delete a single goal row in 'goal' table

        :param connection: DB connection object
        :param goal_id: goal ID
        :param _filter:
            {
               'name': <goal-name>,
               'description': <goal-description>,
               'reason': <lesson-id> (or) None,
               'week': <week-number>,
               'count': <number-of-counts-of-goal>
            }
        :return: boolean output
        """
        session = connection.SESSION
        deleted = True
        try:
            goal_obj = (session.query(schema.Goal).filter_by(id=goal_id).one()
                        if goal_id else
                        session.query(schema.Goal).filter_by(**_filter).one())
            session.delete(goal_obj)
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (DELETE) the goal table: %s" % e
            session.rollback()
            deleted = False
        finally:
            session.close()
        return deleted
