from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship
from  model import Base

#
# Actor model
#
class Actor(Base):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    gender = Column(String, unique=False)
    birth_date = Column(Date, unique=False)
    email = Column(String, unique=False)
    movies = relationship('Movie', secondary='actor_movie_association', back_populates='actors')
            
    def __init__(self, name, gender, birth_date, email):
        """
        Initializes an actor.

        Arguments:
            name: actor's name.
            age: actor's age.
            gender: actor's gender.
            birth_date: actor's birth date.
            email: actor's email.
        """
        self.name = name
        self.gender = gender
        self.birth_date = birth_date
        self.email = email