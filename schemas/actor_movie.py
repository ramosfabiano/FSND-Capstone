from pydantic import BaseModel
from typing import List
from model.actor_movie import ActorMovieAssociation


class ActorMovieViewSchema(BaseModel):
    """ ActorMovie view schema.
    """
    actor_id: int 
    movie_id: int 


class ActorMovieListSchema(BaseModel):
    """ ActorMovie list schema.
    """
    ActorMovieAssociation:List[ActorMovieViewSchema]
        
class ActorMovieAddSchema(BaseModel):
    """ ActorMovie add schema.
    """
    actor_id: int 
    movie_id: int 

class ActorMovieSearchSchema(BaseModel):
    """ ActorMovie search schema.
    """
    actor_id: int 
    movie_id: int 

def ActorMovieRepresentation(actorMovieAssociation: ActorMovieAssociation):
    """ Returns the representation of an actor-movie association.
    """
    return {
        "actor_id": actorMovieAssociation.actor_id,
        "movie_id": actorMovieAssociation.movie_id
    }

def ActorMovieListRepresentation(actorMovieAssociations: List[ActorMovieAssociation]):
    """ Returns the representation of a list of actor-movie associations.
    """
    return {
        "associations": [ActorMovieRepresentation(a) for a in actorMovieAssociations]
    }