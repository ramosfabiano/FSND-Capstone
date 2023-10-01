from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship
from model.base import Base
from model.actor_movie import actor_movie

#
# Movie model
#
class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    genre = Column(String, unique=False)
    release_date = Column(Date, unique=False)
    actors = relationship('Actor', secondary=actor_movie, back_populates='movies')
        
    def __init__(self, title, genre, release_date):
        """
        Initializes a movie.

        Arguments:
            name: movie's name.
            title: movie's title.
            genre: movie's genre.
            release_date: movie's release date.
        """
        self.title = title
        self.genre = genre
        self.release_date = release_date
