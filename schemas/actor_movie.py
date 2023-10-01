from pydantic import BaseModel

class ActorMovieSchema(BaseModel):
    """ ActorMovie schema.
    """
    actor_id: int 
    movie_id: int 
