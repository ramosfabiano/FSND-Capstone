from pydantic import BaseModel
from typing import List
from model.actor import Actor

class ActorViewSchema(BaseModel):
    """ Actor schema.
    """
    id: int 
    name: str 
    age: int
    email: str

class ActorListSchema(BaseModel):
    """ Actor list schema.
    """
    Actor:List[ActorViewSchema]

class ActorAddSchema(BaseModel):
    """ Actor add schema.
    """
    id: int
    name: str 
    age: int
    email: str

class ActorSearchSchema(BaseModel):
    """ Actor search schema.
    """
    id: str

class ActorPatchSchema(BaseModel):
    """ Actor patch schema.
    """
    id: int
    name: str 
    age: int  
    email: str  
    
def ActorRepresentation(actor: Actor):
    """ Returns the representation of an actor.
    """
    return {
        "id": actor.id,
        "name": actor.name,
        "age": actor.age,
        "email": actor.email
    }

def ActorListRepresentation(actors: List[Actor]):
    """ Returns the representation of a list of actors.
    """
    return {
        "actors": [ActorRepresentation(actor) for actor in actors]
    }