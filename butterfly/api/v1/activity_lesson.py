from flask import request
import json

from butterfly.api.v1 import activity_lesson_api, connection
from butterfly.db.api.activity_lesson import ActivityLesson
from constants import URL_KEY, LESSON_ID_KEY, USER_ID_KEY


@activity_lesson_api.route('/user/<user_id>/activity/lesson',
                           strict_slashes=False,  methods=['GET', 'POST'])
def activity_lesson_get_all_post(user_id):
    method = request.method
    values = {"user_id": user_id}

    def get():
        activity_lesson_list = ActivityLesson.get_all(connection, **values)
        for activity_lesson in activity_lesson_list:
            activity_lesson[URL_KEY] = "{}/{}".format(request.url, activity_lesson.get(LESSON_ID_KEY))
        return json.dumps(activity_lesson_list)

    def post():
        values.update(json.loads(request.get_data()))
        if ActivityLesson.create_or_update(connection, **values):
            activity_lesson = ActivityLesson.get(connection, None, **values)
            return json.dumps(activity_lesson)
        else:
            return "Unable to create lesson activity !"

    if method == 'GET':
        return get()
    if method == 'POST':
        return post()


@activity_lesson_api.route('/user/<user_id>/activity/lesson/<lesson_id>',
                           strict_slashes=False,  methods=['GET', 'PUT', 'DELETE'])
def activity_lesson_get_put_delete(user_id, lesson_id):
    method = request.method
    values = {USER_ID_KEY: user_id, LESSON_ID_KEY: lesson_id}

    def get(**_filter):
        activity_lesson = ActivityLesson.get(connection, None, **_filter)
        return json.dumps(activity_lesson)

    def put(**_values):
        if ActivityLesson.create_or_update(connection, **_values):
            return get(**_values)
        else:
            return "Unable to update the lesson activity !"

    def delete(**_filter):
        if ActivityLesson.delete(connection, None, **_filter):
            return "Lesson activity deleted successfully"
        else:
            return "Unable to delete the lesson activity!"

    if method == 'GET':
        return get(**values)
    if method == 'PUT':
        return put(**values)
    if method == 'DELETE':
        return delete(**values)
