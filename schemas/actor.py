from pydantic import BaseModel
from typing import List
from model.actor import Actor

class ActorViewSchema(BaseModel):
    """ Actor schema.
    """
    id: int 
    name: str 
    gender: str
    birth_date: str
    email: str

class ActorListSchema(BaseModel):
    """ Actor list schema.
    """
    Actor:List[ActorViewSchema]

class ActorAddSchema(BaseModel):
    """ Actor add schema.
    """
    name: str 
    gender: str
    birth_date: str
    email: str

class ActorSearchSchema(BaseModel):
    """ Actor search schema.
    """
    id: int

class ActorPatchSchema(BaseModel):
    """ Actor patch schema.
    """
    id: int
    name: str 
    gender: str
    birth_date: str 
    email: str  
    
def ActorRepresentation(actor: Actor):
    """ Returns the representation of an actor.
    """
    return {
        "id": actor.id,
        "name": actor.name,
        "gender": actor.gender,
        "birth_date": actor.birth_date,
        "email": actor.email
    }

def ActorListRepresentation(actors: List[Actor]):
    """ Returns the representation of a list of actors.
    """
    return {
        "actors": [ActorRepresentation(actor) for actor in actors]
    }