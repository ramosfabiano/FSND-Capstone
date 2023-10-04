from pydantic import BaseModel
from typing import List
from model.actor import Actor
from flask import jsonify

class ActorPathSchema(BaseModel):
    """ Actor path schema.
    """    
    id: int
    
class ActorViewSchema(BaseModel):
    """ Actor schema.
    """
    id: int 
    name: str 
    gender: str
    birth_date: str
    nationality: str

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
    nationality: str

class ActorSearchSchema(BaseModel):
    """ Actor search schema.
    """
    id: int

class ActorPatchSchema(BaseModel):
    """ Actor patch schema.
    """
    name: str 
    gender: str
    birth_date: str 
    nationality: str  
    
def ActorRepresentation(actor: Actor):
    """ Returns the representation of an actor.
    """    
    movies_characters = []
    for m in actor.movies:
        for a in m.associations:
            if a.actor_id == actor.id:
                movies_characters.append([m.id, m.title, a.character_name])                
    return {
        "id": actor.id,
        "name": actor.name,
        "gender": actor.gender,
        "birth_date": actor.birth_date,
        "nationality": actor.nationality,
        "movie_assocations": movies_characters   
    }

def ActorListRepresentation(actors: List[Actor]):
    """ Returns the representation of a list of actors.
    """
    return {
        "actors": [ActorRepresentation(a) for a in actors]
    }