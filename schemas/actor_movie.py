from pydantic import BaseModel

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
