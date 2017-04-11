from flask import request
import json

from butterfly.api.v1 import lesson_api, connection
from butterfly.db.api.lesson import Lesson


@lesson_api.route('/lesson',  strict_slashes=False,  methods=['GET', 'POST'])
def lesson_get_all_post():
    """Function to
       1. retrieve all lessons (with/without filtering)
       2. create a lesson
    :return: lesson details
    """
    method = request.method
    values = dict()
    if request.get_data():
        values = json.loads(request.get_data())

    def get():
        lesson_details = Lesson.get_all(connection, **values)
        for lesson in lesson_details:
            lesson["url"] = "{}/{}".format(request.url, lesson.get("id"))
        return json.dumps(lesson_details)

    def post():
        if Lesson.create(connection, **values):
            lesson = Lesson.get(connection, None, **values)
            return json.dumps(lesson)
        else:
            return "Unable to create lesson !"

    if method == 'GET':
        return get()
    if method == 'POST':
        return post()


@lesson_api.route('/lesson/<lesson_id>',  strict_slashes=False,  methods=['GET', 'PUT', 'DELETE'])
def lesson_get_user_delete(lesson_id):
    """Function to
       1. retrieve a lesson
       2. edit a lesson
       3. delete a lesson
    :param lesson_id: lesson ID
    :return: lesson details
    """
    method = request.method
    values = dict()
    if request.get_data():
        values = json.loads(request.get_data())

    def get(_lesson_id):
        lesson = Lesson.get(connection, _lesson_id)
        return json.dumps(lesson)

    def put(_lesson_id):
        if Lesson.update(connection, _lesson_id, **values):
            return get(_lesson_id)
        else:
            return "Unable to update the lesson !"

    def delete(_lesson_id):
        lesson_name = Lesson.get(connection, _lesson_id).get("name")
        print lesson_name
        if Lesson.delete(connection, _lesson_id):
            return "Lesson ({}: {}) deleted successfully".format(_lesson_id, lesson_name)
        else:
            return "Unable to delete the lesson {}!".format(lesson_name)

    if method == 'GET':
        return get(lesson_id)
    if method == 'PUT':
        return put(lesson_id)
    if method == 'DELETE':
        return delete(lesson_id)
