from flask import request
import json

from butterfly.api.v1 import goal_api, connection
from butterfly.db.api.goal import Goal


@goal_api.route('/goal',  strict_slashes=False,  methods=['GET', 'POST'])
def goal_get_all_post():
    """Function to
       1. retrieve all goals (with/without filtering)
       2. create a goal
    :return: goal details
    """
    method = request.method
    values = dict()
    if request.get_data():
        values = json.loads(request.get_data())

    def get():
        goal_details = Goal.get_all(connection, **values)
        for goal in goal_details:
            goal["url"] = "{}/{}".format(request.url, goal.get("id"))
        return json.dumps(goal_details)

    def post():
        if Goal.create(connection, **values):
            goal = Goal.get(connection, None, **values)
            return json.dumps(goal)
        else:
            return "Unable to create goal !"

    if method == 'GET':
        return get()
    if method == 'POST':
        return post()


@goal_api.route('/goal/<goal_id>',  strict_slashes=False,  methods=['GET', 'PUT', 'DELETE'])
def goal_get_user_delete(goal_id):
    """Function to
       1. retrieve a goal
       2. edit a goal
       3. delete a goal
    :param goal_id: goal ID
    :return: goal details
    """
    method = request.method
    values = dict()
    if request.get_data():
        values = json.loads(request.get_data())

    def get(_goal_id):
        goal = Goal.get(connection, _goal_id)
        return json.dumps(goal)

    def put(_goal_id):
        if Goal.update(connection, _goal_id, **values):
            return get(_goal_id)
        else:
            return "Unable to update the goal !"

    def delete(_goal_id):
        goal_name = Goal.get(connection, _goal_id).get("name")
        if Goal.delete(connection, _goal_id):
            return "Goal ({}: {}) deleted successfully".format(_goal_id, goal_name)
        else:
            return "Unable to delete the lesson {}!".format(goal_name)

    if method == 'GET':
        return get(goal_id)
    if method == 'PUT':
        return put(goal_id)
    if method == 'DELETE':
        return delete(goal_id)
