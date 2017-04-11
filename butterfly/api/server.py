from flask import Flask
from v1.user import user_api
from v1.lesson import lesson_api
from v1.goal import goal_api


app = Flask(__name__)
app.register_blueprint(user_api)
app.register_blueprint(lesson_api)
app.register_blueprint(goal_api)


def run(config):
    host = config.get("API").get("interface")
    port = config.get("API").get("port")
    app.run(host=None, port=port)
