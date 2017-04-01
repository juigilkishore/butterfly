from copy import deepcopy

from api import Table
from butterfly.db import schema


class Lesson(Table):
    @classmethod
    def get_all(cls, connection, **_filter):
        """Get all lesson rows in 'lesson' table

        :param _filter:
        :return:
        """
        session = connection.SESSION
        lesson_list = list()
        try:
            lesson_obj_list = (session.query(schema.Lesson).filter_by(**_filter).all()
                               if _filter else session.query(schema.Lesson).all())
            for lesson in lesson_obj_list:
                lesson_list.append(cls.row_object_to_dict(lesson))
            lesson_list = deepcopy(lesson_list)
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (GET ALL) the lesson table: %s" % e
            session.rollback()
        finally:
            session.close()
        return lesson_list

    @classmethod
    def get(cls, connection, lesson_id, **_filter):
        """Get a single lesson row in 'lesson' table

        :param lesson_id:
        :param _filter:
        :return:
        """
        session = connection.SESSION
        lesson = None
        try:
            lesson_obj = (session.query(schema.Lesson).filter_by(id=lesson_id).one()
                          if lesson_id else
                          session.query(schema.Lesson).filter_by(**_filter).one())
            lesson = deepcopy(cls.row_object_to_dict(lesson_obj))
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (GET) the lesson table: %s" % e
            session.rollback()
        finally:
            session.close()
        return lesson

    @classmethod
    def create(cls, connection, **values):
        """Create a lesson row in 'lesson' table

        :param values:
        :return:
        """
        session = connection.SESSION
        created = True
        try:
            session.add(schema.Lesson(**values))
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (INSERT) the lesson table: %s" % e
            session.rollback()
            created = False
        finally:
            session.close()
        return created

    @classmethod
    def update(cls, connection, lesson_id, **values):
        """Update a single lesson row in 'lesson' table

        :param lesson_id:
        :param values:
        :return:
        """
        session = connection.SESSION
        updated = True
        try:
            if not lesson_id:
                raise Exception("lesson ID is required for update operation")
            lesson_obj = session.query(schema.Lesson).filter_by(id=lesson_id).one()
            [setattr(lesson_obj, attr, new_val) for attr, new_val in values.iteritems()]
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (UPDATE) the lesson table: %s" % e
            session.rollback()
            updated = False
        finally:
            session.close()
        return updated

    @classmethod
    def delete(cls, connection, lesson_id, **_filter):
        """Delete a single lesson row in 'lesson' table

        :param lesson_id:
        :param _filter:
        :return:
        """
        session = connection.SESSION
        deleted = True
        try:
            lesson_obj = (session.query(schema.Lesson).filter_by(id=lesson_id).one()
                          if lesson_id else
                          session.query(schema.Lesson).filter_by(**_filter).one())
            session.delete(lesson_obj)
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (DELETE) the lesson table: %s" % e
            session.rollback()
            deleted = False
        finally:
            session.close()
        return deleted
