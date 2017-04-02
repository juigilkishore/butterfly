from copy import deepcopy

from api import Table
from butterfly.db import schema
from constants import NAME_KEY, ID_KEY


class Lesson(Table):
    @classmethod
    def get_all(cls, connection, **_filter):
        """Get all lesson rows from 'lesson' table

        :param connection: DB connection object
        :param _filter: 'AND' filter dictionary
            {
                'name': <lesson-name>,
                'content': <lesson-content>,
                'week': <week-number>,
                'number': <lesson-number>,
                'is_active': True
            }
        :return: List of lesson details
            [{
                'name': 'Calories',
                'content': <lesson-content>,
                'week': 1,
                'number': 3,
                'is_active': True,
                'id': 'a97196c9-ead8-4e6f-8b0c-a76fbefaafa0'
            }]
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
        """Get a single lesson row from 'lesson' table

        _filter is ignored if lesson_id is provided

        :param connection: DB connection object
        :param lesson_id: lesson ID
        :param _filter: 'AND' filter dictionary
             {
                'name': <lesson-name>,
                'content': <lesson-content>,
                'week': <week-number>,
                'number': <lesson-number>,
                'is_active': True
            }
        :return: Lesson detail
            {
                'name': 'Calories',
                'content': <lesson-content>,
                'week': 1,
                'number': 3,
                'is_active': True,
                'id': 'a97196c9-ead8-4e6f-8b0c-a76fbefaafa0'
            }
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
    def get_lesson_id(cls, connection, lesson_name):
        """Get the lesson ID from lesson name

        :param connection: DB connection object
        :param lesson_name: lesson name
        :return: lesson ID
        """
        lesson = cls.get(connection, None, **{NAME_KEY: lesson_name})
        return lesson.get(ID_KEY)

    @classmethod
    def get_lesson_from_week(cls, connection, week_start, week_end):
        """Get all lessons from 'lesson' table between weeks week_start and week_end

        :param connection: DB connection object
        :param week_start: start week-number
        :param week_end: end week-number
        :return: list of lesson details
        """
        session = connection.SESSION
        lesson_list = list()
        try:
            lesson_obj_list = session.query(schema.Lesson).filter(
                schema.Lesson.week >= week_start,
                schema.Lesson.week <= week_end).all()
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
    def create(cls, connection, **values):
        """Create a lesson row in 'lesson' table

        :param connection: DB connection object
        :param values: lesson payload
             {
                'name': <lesson-name>,
                'content': <lesson-content>,
                'week': <week-number>,
                'number': <lesson-number>,
                'is_active': True
            }
        :return: boolean output
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
        """Update a single lesson row from 'lesson' table

        :param connection: DB connection object
        :param lesson_id: lesson ID
        :param values:
             {
                'name': <lesson-name-modified>,
                'week': <week-number-new>
            }
        :return: boolean output
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

        :param connection: DB connection object
        :param lesson_id: lesson ID
        :param _filter: AND filter dictionary
             {
                'name': <lesson-name>,
                'content': <lesson-content>,
                'week': <week-number>,
                'number': <lesson-number>,
                'is_active': True
            }
        :return: boolean output
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
