from flask import Blueprint
from butterfly.db.api.api import get_db_connection
from butterfly.utils.parser import config

user_api = Blueprint('user_api', __name__)

connection = get_db_connection(config)

# This line has to be at the end
from user import *
