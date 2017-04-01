from copy import deepcopy

from api import Table
from butterfly.db import schema


class Goal(Table):
    @classmethod
    def get_all(cls, connection, **_filter):
        """Get all goal rows in 'goal' table

        :param _filter:
        :return:
        """
        session = connection.SESSION
        goal_list = list()
        try:
            goal_obj_list = (session.query(schema.Goal).filter_by(**_filter).all()
                             if _filter else session.query(schema.Goal).all())
            for goal in goal_obj_list:
                goal_list.append(cls.row_object_to_dict(goal))
            goal_list = deepcopy(goal_list)
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (GET ALL) the goal table: %s" % e
            session.rollback()
        finally:
            session.close()
        return goal_list

    @classmethod
    def get(cls, connection, goal_id, **_filter):
        """Get a single goal row in 'goal' table

        :param goal_id:
        :param _filter:
        :return:
        """
        session = connection.SESSION
        goal = None
        try:
            goal_obj = (session.query(schema.Goal).filter_by(id=goal_id).one()
                          if goal_id else
                          session.query(schema.Goal).filter_by(**_filter).one())
            goal = deepcopy(cls.row_object_to_dict(goal_obj))
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (GET) the goal table: %s" % e
            session.rollback()
        finally:
            session.close()
        return goal

    @classmethod
    def create(cls, connection, **values):
        """Create a goal row in 'goal' table

        :param values:
        :return:
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

        :param goal_id:
        :param values:
        :return:
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

        :param goal_id:
        :param _filter:
        :return:
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
