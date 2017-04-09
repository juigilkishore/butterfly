from flask import Flask
from v1.user import user_api

app = Flask(__name__)
app.register_blueprint(user_api)


def run(config):
    host = config.get("API").get("interface")
    port = config.get("API").get("port")
    app.run(host=None, port=port)
