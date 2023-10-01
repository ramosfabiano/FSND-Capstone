from sqlalchemy import Table, ForeignKey, Column, Integer
from model.base import Base

#
# Many-to-many actor-movie association 
#
actor_movie = Table(
    'actor_movie',
    Base.metadata,
    Column('actor_id', Integer, ForeignKey('actor.id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id'), primary_key=True)
)