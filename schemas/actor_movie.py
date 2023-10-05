from pydantic import BaseModel
from model.actor_movie import ActorMovieAssociation

class ActorMovieSchema(BaseModel):
    """ ActorMovie schema.
    """
    actor_id: int 
    movie_id: int 
    character_name: str

class ActorMovieDeleteSchema(BaseModel):
    """ ActorMovie deletion schema.
    """
    actor_id: int 
    movie_id: int 

def ActorMovieRepresentation(actor_movie: ActorMovieAssociation):
    """ Returns the representation of an actor-movie association.
    """    
    return {
        "actor_id": actor_movie.actor_id,
        "movie_id": actor_movie.movie_id,
        "character_name": actor_movie.character_name 
    }
