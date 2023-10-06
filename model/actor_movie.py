from sqlalchemy import Table, ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from model.base import Base

#
# Many-to-many actor-movie association 
#
actor_movie_association = Table(
    'actor_movie_association',
    Base.metadata,
    Column('actor_id', Integer, ForeignKey('actor.id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id'), primary_key=True),
    Column('character_name', String, unique=False, nullable=False)
)

#
# Many-to-many actor-movie association proxy to allw access to character_name
#
class ActorMovieAssociation(Base):
    __tablename__ = 'actor_movie_association'
    Column('actor_id', Integer, ForeignKey('actor.id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id'), primary_key=True),
    Column('character_name', String, unique=False, nullable=False)
    actors = relationship('Actor', back_populates='associations')
    movies = relationship('Movie', back_populates='associations')