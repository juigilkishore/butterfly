from copy import deepcopy

from api import Table
from butterfly.db import schema
from constants import NAME_KEY, ID_KEY


class User(Table):
    @classmethod
    def get_all(cls, connection, **_filter):
        """Get all user rows from 'user' table

        :param connection: DB connection object
        :param _filter: 'AND' filter dictionary
            {'gender': 'male',
             'age': 25L}
        :return: List of user details
            [{'name': 'testuser',
              'gender': 'male',
              'age': 25L,
              'email': 'test@email.com',
              'phone': '9897969594',
              'id': '7d3710b0-802c-40f7-bbf1-a7d6a8e6d02c'}]
        """
        session = connection.SESSION
        user_list = list()
        try:
            user_obj_list = (session.query(schema.User).filter_by(**_filter).all()
                             if _filter else session.query(schema.User).all())
            for user in user_obj_list:
                user_list.append(cls.row_object_to_dict(user))
            user_list = deepcopy(user_list)
        except Exception as e:
            print "Exception occurred during querying (GET ALL) the user table: %s" % e
        return user_list

    @classmethod
    def get(cls, connection, user_id, **_filter):
        """Get a single user row from 'user' table

        **_filter is ignored id user_id is provided

        :param connection: DB connection object
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
        session = connection.SESSION
        user = None
        try:
            user_obj = (session.query(schema.User).filter_by(id=user_id).one()
                        if user_id else
                        session.query(schema.User).filter_by(**_filter).one())
            user = deepcopy(cls.row_object_to_dict(user_obj))
        except Exception as e:
            print "Exception occurred during querying (GET) the user table: %s" % e
        return user

    @classmethod
    def get_user_id(cls, connection, user_name):
        """Get user ID for user_name from 'user' table

        :param connection: DB connection object
        :param user_name: user name
        :return: user ID
        """
        user = cls.get(connection, None, **{NAME_KEY: user_name})
        return user.get(ID_KEY)

    @classmethod
    def create(cls, connection, **values):
        """Create a user row in 'user' table

        :param connection: DB connection object
        :param values: user payload
            {"name": "testuser",
             "age": 25,
             "gender": "male",
             "email": "testuser@email.com",
             "phone": str(9897969594)}
        :return: Boolean output
        """
        session = connection.SESSION
        created = True
        try:
            session.add(schema.User(**values))
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (INSERT) the user table: %s" % e
            session.rollback()
            created = False
        finally:
            session.close()
        return created

    @classmethod
    def update(cls, connection, user_id, **values):
        """Update a single user row from 'user' table

        :param connection: DB connection object
        :param user_id: user ID (mandatory argument)
        :param values: user payload to be updated
            {"name": "newuser",
             "age": 27,
             "gender": "female",
             "email": "newuser@email.com"}
        :return: Boolean output
        """
        session = connection.SESSION
        updated = True
        try:
            if not user_id:
                raise Exception("user ID is required for update operation")
            user_obj = session.query(schema.User).filter_by(id=user_id).one()
            [setattr(user_obj, attr, new_val) for attr, new_val in values.iteritems()]
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (UPDATE) the user table: %s" % e
            session.rollback()
            updated = False
        finally:
            session.close()
        return updated

    @classmethod
    def delete(cls, connection, user_id, **_filter):
        """Delete a single user row from 'user' table

        **_filter is ignored id user_id is provided

        :param connection: DB connection object
        :param user_id: user ID
        :param _filter: 'AND' filter dictionary
            {'gender': 'male',
             'age': 25L,
             'email': 'test@email.com',
             'phone': '9897969594'}
        :return: Boolean output
        """
        session = connection.SESSION
        deleted = True
        try:
            user_obj = (session.query(schema.User).filter_by(id=user_id).one()
                        if user_id else
                        session.query(schema.User).filter_by(**_filter).one())
            session.delete(user_obj)
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (DELETE) the user table: %s" % e
            session.rollback()
            deleted = False
        finally:
            session.close()
        return deleted
