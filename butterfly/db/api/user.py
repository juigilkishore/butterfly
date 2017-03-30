from copy import deepcopy

from api import get_db_engine, get_db_session, Table
from butterfly.db import schema


class User(Table):
    @classmethod
    def get_all(cls, **_filter):
        """Get all user rows in 'user' table

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
        engine = get_db_engine(cls.CONNECTION_STRING)
        session = get_db_session(engine)
        user_list = list()
        try:
            user_obj_list = (session.query(schema.User).filter_by(**_filter).all()
                             if _filter else session.query(schema.User).all())
            for user in user_obj_list:
                user_list.append(cls.row_object_to_dict(user))
            user_list = deepcopy(user_list)
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (GET ALL) the user table: %s" % e
            session.rollback()
        finally:
            session.close()
        return user_list

    @classmethod
    def get(cls, user_id, **_filter):
        """Get a single user row in 'user' table

        **_filter is ignored id user_id is provided

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
        engine = get_db_engine(cls.CONNECTION_STRING)
        session = get_db_session(engine)
        user = None
        try:
            user_obj = (session.query(schema.User).filter_by(id=user_id).one()
                        if user_id else
                        session.query(schema.User).filter_by(**_filter).one())
            user = deepcopy(cls.row_object_to_dict(user_obj))
            session.commit()
        except Exception as e:
            print "Exception occurred during querying (GET) the user table: %s" % e
            session.rollback()
        finally:
            session.close()
        return user

    @classmethod
    def create(cls, **values):
        """Create a user row in 'user' table

        :param values: user payload
            {"name": "testuser",
             "age": 25,
             "gender": "male",
             "email": "testuser@email.com",
             "phone": str(9897969594)}
        :return: Boolean output
        """
        engine = get_db_engine(cls.CONNECTION_STRING)
        session = get_db_session(engine)
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
    def update(cls, user_id, **values):
        """Update a single user row in 'user' table

        :param user_id: user ID (mandatory argument)
        :param values: user payload to be updated
            {"name": "newuser",
             "age": 27,
             "gender": "female",
             "email": "newuser@email.com"}
        :return: Boolean output
        """
        engine = get_db_engine(cls.CONNECTION_STRING)
        session = get_db_session(engine)
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
    def delete(cls, user_id, **_filter):
        """Delete a single user row in 'user' table

        **_filter is ignored id user_id is provided

        :param user_id: user ID
        :param _filter: 'AND' filter dictionary
            {'gender': 'male',
             'age': 25L,
             'email': 'test@email.com',
             'phone': '9897969594'}
        :return: Boolean output
        """
        engine = get_db_engine(cls.CONNECTION_STRING)
        session = get_db_session(engine)
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
