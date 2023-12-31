from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from model.base import Base
from model.actor_movie import actor_movie_association, ActorMovieAssociation
from model.actor import Actor
from model.movie import Movie

# reads the database path from the environment
database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)
  
# creates a PostgreSQL database engine
engine = create_engine(database_path, echo=False)

# initializes the database
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
