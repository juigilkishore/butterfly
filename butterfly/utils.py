from functools import wraps
import json
import os

from uuid import uuid4


def get_uuid():
    return str(uuid4())


def get_dir_of(_file):
    return os.path.dirname(os.path.abspath(_file))


def load_file(_file):
    with open(_file, mode='r') as fp:
        data = json.load(fp)
    return data


def singleton(my_class):
    instance = dict()

    @wraps(my_class)
    def my_class_wrapper(*args, **kwargs):
        if not instance.get(my_class):
            instance[my_class] = my_class(*args, **kwargs)
        return instance.get(my_class)
    return my_class_wrapper
