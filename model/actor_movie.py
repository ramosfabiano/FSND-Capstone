from sqlalchemy import ForeignKey, Column, String, Integer, Date
from sqlalchemy.orm import relationship
from  model import Base

#
# Many-to-many actor-movie association model
#
class ActorMovieAssociation(Base):
    __tablename__ = 'actor_movie_association'

    actor_id = Column(Integer, ForeignKey('actor.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id'), primary_key=True)
        
    def __init__(self, actor_id, movie_id):
        """
        Initializes an many-to-many actor-movie association.

        Arguments:
            actor_id: actor's id.
            movie_id: movies's id.
        """
        self.actor_id = actor_id
        self.movie_id = movie_id