from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship
from model.base import Base
from model.actor_movie import actor_movie_association

#
# Actor model
#
class Actor(Base):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    gender = Column(String, unique=False)
    birth_date = Column(Date, unique=False)
    nationality = Column(String, unique=False)
    associations = relationship('ActorMovieAssociation', back_populates='actors')
    movies = relationship('Movie', secondary=actor_movie_association, back_populates='actors', overlaps="actors, movies, associations")
            
    def __init__(self, name, gender, birth_date, nationality):
        """
        Initializes an actor.

        Arguments:
            name: actor's name.
            age: actor's age.
            gender: actor's gender.
            birth_date: actor's birth date.
            nationality: actor's nationality.
        """
        self.name = name
        self.gender = gender
        self.birth_date = birth_date
        self.nationality = nationality
    