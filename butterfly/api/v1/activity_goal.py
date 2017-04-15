from flask import request
import json

from butterfly.api.v1 import activity_goal_api, connection
from butterfly.db.api.activity_goal import ActivityGoal
from constants import URL_KEY, GOAL_ID_KEY, USER_ID_KEY


@activity_goal_api.route('/user/<user_id>/activity/goal',
                         strict_slashes=False,  methods=['GET', 'POST'])
def activity_goal_get_all_post(user_id):
    method = request.method
    values = {"user_id": user_id}

    def get():
        activity_goal_list = ActivityGoal.get_all(connection, **values)
        for activity_goal in activity_goal_list:
            activity_goal[URL_KEY] = "{}/{}".format(request.url, activity_goal.get(GOAL_ID_KEY))
        return json.dumps(activity_goal_list)

    def post():
        values.update(json.loads(request.get_data()))
        if ActivityGoal.create_or_update(connection, **values):
            activity_goal = ActivityGoal.get(connection, None, **values)
            return json.dumps(activity_goal)
        else:
            return "Unable to create goal activity !"

    if method == 'GET':
        return get()
    if method == 'POST':
        return post()


@activity_goal_api.route('/user/<user_id>/activity/goal/<goal_id>',
                         strict_slashes=False,  methods=['GET', 'PUT', 'DELETE'])
def activity_goal_get_put_delete(user_id, goal_id):
    method = request.method
    values = {USER_ID_KEY: user_id, GOAL_ID_KEY: goal_id}

    def get(**_filter):
        activity_goal = ActivityGoal.get(connection, None, **_filter)
        return json.dumps(activity_goal)

    def put(**_values):
        if ActivityGoal.create_or_update(connection, **_values):
            return get(**_values)
        else:
            return "Unable to update the goal activity !"

    def delete(**_filter):
        if ActivityGoal.delete(connection, None, **_filter):
            return "Goal activity deleted successfully"
        else:
            return "Unable to delete the goal activity!"

    if method == 'GET':
        return get(**values)
    if method == 'PUT':
        return put(**values)
    if method == 'DELETE':
        return delete(**values)
