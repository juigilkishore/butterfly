from flask import Blueprint
from butterfly.db.api.api import get_db_connection
from butterfly.utils.parser import config

user_api = Blueprint('user_api', __name__)
lesson_api = Blueprint('lesson_api', __name__)
goal_api = Blueprint('goal_api', __name__)
activity_lesson_api = Blueprint('activity_lesson_api', __name__)
activity_goal_api = Blueprint('activity_goal_api', __name__)

connection = get_db_connection(config)

# This line has to be at the end
from user import *
from lesson import *
from goal import *
from activity_lesson import *
from activity_goal import *
