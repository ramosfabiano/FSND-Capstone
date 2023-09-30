from pydantic import BaseModel
from typing import List
from model.movie import Movie

class MovieViewSchema(BaseModel):
    """ Movie schema.
    """
    id: int 
    title: str 
    genre: str
    release_date: str

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
    id: int 
    title: str 
    genre: str
    release_date: str
    
def MovieRepresentation(movie: Movie):
    """ Returns the representation of an Movie.
    """
    return {
        "id": movie.id,
        "title": movie.title,
        "genre": movie.genre,
        "release_date": movie.release_date
    }

def MovieListRepresentation(movies: List[Movie]):
    """ Returns the representation of a list of Movies.
    """
    return {
        "movies": [MovieRepresentation(m) for m in movies]
    }