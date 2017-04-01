from schema import User
from api.api import Connection

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

val1 = {"name": "u1", "age": 25, "gender": "male", "email": "u1@email.com", "phone": str(12345)}
val2 = {"name": "u2", "age": 25, "gender": "male", "email": "u2@email.com", "phone": str(67890)}
# connection = Connection(connection_string="mysql+mysqldb://butterfly:butterfly@localhost/butterfly")
# session = connection.SESSION

connection_string = "mysql+mysqldb://butterfly:butterfly@localhost/butterfly"
engine = create_engine(connection_string)
session_maker = sessionmaker(bind=engine)
session = session_maker(autocommit=False, expire_on_commit=False)

U1 = User(**val1)
print id(U1), U1.__dict__
U2 = User(**val2)
print id(U2), U2.__dict__

session.add(U1)
session.commit()
session.close()

session.add(U2)
session.commit()
session.close()
