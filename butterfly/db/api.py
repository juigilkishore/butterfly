from sqlalchemy import create_engine


def get_db_engine(connection_string):
    engine = create_engine(connection_string)
    return engine
