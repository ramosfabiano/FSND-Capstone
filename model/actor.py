from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from  model import Base

#
# Actor model
#
class Actor(Base):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(128), unique=False)
    age = Column(Integer, unique=False)
    email = Column(String(128), unique=False)
    #movies = relationship("Movie", back_populates="actor")
        
    def __init__(self, id:int, name:str, age:int, email:str):
        """
        Initializes an actor.

        Arguments:
            name: actor's name.
            age: actor's age.
        """
        self.id  = id
        self.name = name
        self.age = age
        self.email = email