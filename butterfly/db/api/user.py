import copy

from api import get_db_session, Table
from butterfly.db import schema


class User(Table):
    @classmethod
    def get_all(cls, engine):
        """Get all user rows in 'user' table

        :param engine: DB engine instance
        :return: List of user details
            [{'name': 'testuser',
              'gender': 'male',
              'age': 25L,
              'email': 'test@email.com',
              'phone': '9897969594',
              'id': '7d3710b0-802c-40f7-bbf1-a7d6a8e6d02c'}]
        """
        session = get_db_session(engine)
        user_list = list()
        try:

            for user in session.query(schema.User).all():
                user_list.append(cls.row_object_to_dict(user))
            user_list = copy.deepcopy(user_list)
            session.commit()
        except Exception as e:
            print "Exception Occurred during GET ALL query: %s" % e
        finally:
            session.close()
        return user_list

    @classmethod
    def get(cls, engine, user_id, **_filter):
        """Get a single user row in 'user' table

        **_filter is ignored id user_id is provided

        :param engine: DB engine instance
        :param user_id: user ID
        :param _filter: 'AND' filter dictionary
            {'gender': 'male',
             'age': 25L,
             'email': 'test@email.com',
             'phone': '9897969594'}
        :return: user details
            {'name': 'testuser',
             'gender': 'male',
             'age': 25L,
             'email': 'test@email.com',
             'phone': '9897969594',
             'id': '7d3710b0-802c-40f7-bbf1-a7d6a8e6d02c'}
        """

        session = get_db_session(engine)
        user = None
        try:
            user_obj = (session.query(schema.User).filter_by(id=user_id).one()
                        if user_id else
                        session.query(schema.User).filter_by(**_filter).one())
            user = cls.row_object_to_dict(user_obj)
        except Exception as e:
            print "Exception Occurred during GET query: %s" % e
        finally:
            session.close()
        return user

    @classmethod
    def create(cls, engine, **values):
        """Create a user row in 'user' table

        :param engine: DB engine instance
        :param values: user payload
            {"name": "testuser",
             "age": 25,
             "gender": "male",
             "email": "testuser@email.com",
             "phone": str(9897969594)}
        :return: Boolean output
        """
        session = get_db_session(engine)
        created = None
        try:
            session.add(schema.User(**values))
            session.commit()
            created = True
        except Exception as e:
            print "Exception Occurred during INSERT query: %s" % e
            session.rollback()
            created = False
        finally:
            session.close()
            return created

    @classmethod
    def update(cls, engine, user_id, **values):
        """Update the user row in 'user' table

        :param engine: DB engine instance
        :param user_id: user ID (mandatory argument)
        :param values: user payload to be updated
            {"name": "newuser",
             "age": 27,
             "gender": "female",
             "email": "newuser@email.com"}
        :return: Boolean output
        """
        session = get_db_session(engine)
        updated = None
        try:
            if not user_id:
                raise Exception("user ID is required for update operation")
            user_obj = session.query(schema.User).filter_by(id=user_id).one()
            [setattr(user_obj, attr, new_val) for attr, new_val in values.iteritems()]
            session.commit()
            updated = True
        except Exception as e:
            print "Exception Occurred during UPDATE query %s" % e
            session.rollback()
            updated = False
        finally:
            session.close()
            return updated

    @classmethod
    def delete(cls, engine, user_id, **_filter):
        """Delete a single user row in 'user' table

        **_filter is ignored id user_id is provided

        :param engine: DB engine instance
        :param user_id: user ID
        :param _filter: 'AND' filter dictionary
            {'gender': 'male',
             'age': 25L,
             'email': 'test@email.com',
             'phone': '9897969594'}
        :return: Boolean output
        """
        session = get_db_session(engine)
        deleted = None
        try:
            user_obj = (session.query(schema.User).filter_by(id=user_id).one()
                        if user_id else
                        session.query(schema.User).filter_by(**_filter).one())
            session.delete(user_obj)
            session.commit()
            deleted = True
        except Exception as e:
            print "Exception Occurred during DELETE query %s" % e
            session.rollback()
            deleted = False
        finally:
            session.close()
            return deleted
