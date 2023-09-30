from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship
from  model import Base

#
# Actor model
#
class Actor(Base):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, unique=False)
    gender = Column(String, unique=False)
    birth_date = Column(Date, unique=False)
    email = Column(String, unique=False)
        
    def __init__(self, id, name, gender, birth_date, email):
        """
        Initializes an actor.

        Arguments:
            name: actor's name.
            age: actor's age.
        """
        self.id  = id
        self.name = name
        self.gender = gender
        self.birth_date = birth_date
        self.email = email