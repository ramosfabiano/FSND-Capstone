from pydantic import BaseModel
from typing import List
from model.movie import Movie

class MoviePathSchema(BaseModel):
    """ Movie path schema.
    """    
    id: int
    
class MovieCharacterViewSchema(BaseModel):
    """ Movie character schema.
    """
    actor_id: int 
    actor_name: str 
    character_name: str
        
class MovieViewSchema(BaseModel):
    """ Movie schema.
    """
    id: int 
    title: str 
    genre: str
    release_date: str
    assocations: MovieCharacterViewSchema

class MovieListSchema(BaseModel):
    """ Movie list schema.
    """
    Movie:List[MovieViewSchema]

class MovieAddSchema(BaseModel):
    """ Movie add schema.
    """
    title: str 
    genre: str
    release_date: str

class MovieSearchSchema(BaseModel):
    """ Movie search schema.
    """
    id: int

class MoviePatchSchema(BaseModel):
    """ Movie patch schema.
    """
    title: str 
    genre: str
    release_date: str
 
 
def MoviePatchRepresentation(movie: Movie):
    """ Returns the patch representation of a movie.
    """
    return {
        "title": movie.title,
        "genre": movie.genre,
        "release_date": movie.release_date
    }
       
def MovieRepresentation(movie: Movie):
    """ Returns the representation of a movie.
    """
    associations = [] 
    for a in movie.actors:
        for m in a.associations:
            if m.movie_id == movie.id:
                associations.append([a.id, a.name, m.character_name])      
    return {
        "id": movie.id,
        "title": movie.title,
        "genre": movie.genre,
        "release_date": movie.release_date,
        "assocations": associations
    }

def MovieListRepresentation(movies: List[Movie]):
    """ Returns the representation of a list of movies.
    """
    return {
        "movies": [MovieRepresentation(m) for m in movies]
    }