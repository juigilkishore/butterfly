from flask import request
import json

from butterfly.api.v1 import user_api, connection
from butterfly.db.api.user import User


@user_api.route('/user', strict_slashes=False,  methods=['GET', 'POST'])
def user_get_all_post():
    """Function to
       1. retrieve all existing users (with/without filtering)
       2. create an user
    :return: user details
    """
    method = request.method
    values = dict()
    if request.get_data():
        values = json.loads(request.get_data())

    def get():
        user_details = User.get_all(connection, **values)
        for user in user_details:
            user["url"] = "{}/{}".format(request.url, user.get("id"))
        return json.dumps(user_details)

    def post():
        if User.create(connection, **values):
            user = User.get(connection, None, **values)
            return json.dumps(user)
        else:
            return "Unable to create user !"

    if method == 'GET':
        return get()
    if method == 'POST':
        return post()


@user_api.route('/user/<user_id>', strict_slashes=False, methods=['GET', 'PUT', 'DELETE'])
def user_get_put_delete(user_id):
    """Function to
       1. retrieve an user
       2. edit an user
       3. delete an user
    :param user_id: user ID
    :return: user details
    """
    method = request.method
    values = dict()
    if request.get_data():
        values = json.loads(request.get_data())

    def get(_user_id):
        user = User.get(connection, _user_id)
        return json.dumps(user)

    def put(_user_id):
        if User.update(connection, _user_id, **values):
            return get(_user_id)
        else:
            return "Unable to update the user !"

    def delete():
        username = User.get(connection, user_id).get("name")
        if User.delete(connection, user_id):
            return "user ({}: {}) deleted successfully".format(user_id, username)
        else:
            return "Unable to delete the user !"

    if method == 'GET':
        return get(user_id)
    if method == 'PUT':
        return put(user_id)
    if method == 'DELETE':
        return delete()
