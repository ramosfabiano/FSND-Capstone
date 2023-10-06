from pydantic import BaseModel
from typing import List
from model.actor import Actor
from flask import jsonify

class ActorPathSchema(BaseModel):
    """ Actor path schema.
    """    
    id: int
    
class ActorCharacterViewSchema(BaseModel):
    """ Actor character schema.
    """
    actor_id: int 
    movie_title: str 
    character_name: str
       
class ActorViewSchema(BaseModel):
    """ Actor schema.
    """
    id: int 
    name: str 
    gender: str
    birth_date: str
    nationality: str
    assocations: ActorCharacterViewSchema

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

def ActorPatchRepresentation(actor: Actor):
    """ Returns the patch representation of an actor.
    """    
    return {
        "name": actor.name,
        "gender": actor.gender,
        "birth_date": actor.birth_date,
        "nationality": actor.nationality  
    }
        
def ActorRepresentation(actor: Actor):
    """ Returns the representation of an actor.
    """    
    associations = []
    for m in actor.movies:
        for a in m.associations:
            if a.actor_id == actor.id:
                associations.append([m.id, m.title, a.character_name])                
    return {
        "id": actor.id,
        "name": actor.name,
        "gender": actor.gender,
        "birth_date": actor.birth_date,
        "nationality": actor.nationality,
        "assocations": associations   
    }

def ActorListRepresentation(actors: List[Actor]):
    """ Returns the representation of a list of actors.
    """
    return {
        "actors": [ActorRepresentation(a) for a in actors]
    }