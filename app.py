import os
from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask
from flask_cors import CORS
from flask import redirect
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
import logging

from model import Session, Actor, Movie, ActorMovieAssociation, database_path
from schemas import *

    
#
# Creates, initializes and runs the Flask application
#
def create_app(test_config=None):
    
    # openapi setup
    info = Info(title="FSND-Capstone", version="1.0.0")
    app = OpenAPI(__name__, info=info)

    # openapi tags
    home_tag = Tag(name="Documentation", description="OpenAPI documentation")
    actors_tag = Tag(name="Actors", description="Actors API documentation")
    movies_tag = Tag(name="Movies", description="Movies API documentation")
    actor_movies_tag = Tag(name="Actor-Movies", description="Actor-Movies Association API documentation")
        
    # avoid alphabetic ordering of the schema attributes in the documentation.
    app.json.sort_keys = False

    # configures logging
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
   
    #logger.info('Starting the application...')

    # cross-origin resource sharing
    CORS(app, resources={r"/api/*": {"origins": "*"}})
            
    #
    # Actors
    #
    @app.get('/', tags=[home_tag])
    def home():
        """Redirects to documentation page.
        """
        return redirect('/openapi')

    @app.get('/api/v1', tags=[home_tag])
    def v1_home():
        """Redirects to documentation page.
        """
        return redirect('/openapi')

    #
    # Endpoints (actors)
    #
    @app.get('/api/v1/actors', tags=[actors_tag], responses={"200": ActorListSchema, "404": ErrorSchema})
    def get_actors():
        """Retrieves all actors.
        
        Returns a representation of the list of actors.
        """
        session = Session()
        actors = session.query(Actor).all()
        return ActorListRepresentation(actors), 200

    @app.post('/api/v1/actor', tags=[actors_tag], responses={"200": ActorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
    def create_actor(form: ActorAddSchema):
        """Creates a new actor.
        
        Arguments:
            form: actor's data.
        
        Returns a representation of the created actor.
        """
        try:
            session = Session()
            actor = Actor(name=form.name, gender=form.gender, birth_date=form.birth_date, email=form.email)
            session.add(actor)
            session.commit()
            return ActorRepresentation(actor), 200
        except IntegrityError as e:
            error_msg = 'Actor already exists.'
            return ErrorRepresentation(error_msg), 409
        except Exception as e:
            error_msg = 'Error creating actor.'
            return ErrorRepresentation(error_msg), 400

    @app.delete('/api/v1/actor', tags=[actors_tag], responses={"200": ErrorSchema, "404": ErrorSchema})
    def delete_actor(form: ActorSearchSchema):
        """Deletes an actor.
        
        Arguments:
            form: actor's data.
        
        Returns a status message.
        """
        session = Session()
        actor = session.query(Actor).filter(Actor.id == form.id).first()
        if actor is None:
            error_msg = 'Actor not found.'
            return ErrorRepresentation(error_msg), 404
        else:
            session.delete(actor)
            session.commit()
            error_msg = f'Actor successfuly deleted.'
            return ErrorRepresentation(error_msg), 200
        
    @app.patch('/api/v1/actor', tags=[actors_tag], responses={"200": ActorViewSchema, "404": ErrorSchema, "400": ErrorSchema})
    def update_actor(form: ActorPatchSchema):
        """Updates an actor.
        
        Arguments:
            form: actor's data.
        
        Returns a representation of the updated actor.
        """
        session = Session()
        actor = session.query(Actor).filter(Actor.id == form.id).first()
        if actor is None:
            error_msg = 'Actor not found.'
            return ErrorRepresentation(error_msg), 404
        else:
            actor.name = form.name
            actor.gender = form.gender
            actor.birth_date = form.birth_date
            actor.email = form.email
            try:
                session.commit()
                return ActorRepresentation(actor), 200
            except Exception as e:
                error_msg = 'Error patching actor.'
                return ErrorRepresentation(error_msg), 400

    #
    # Movies
    #
    @app.get('/api/v1/movies', tags=[movies_tag], responses={"200": MovieListSchema, "404": ErrorSchema})
    def get_movies():
        """Retrieves all movies.
        
        Returns a representation of the list of movies.
        """
        session = Session()
        movies = session.query(Movie).all()
        return MovieListRepresentation(movies), 200

    @app.post('/api/v1/movie', tags=[movies_tag], responses={"200": MovieViewSchema, "409": ErrorSchema, "400": ErrorSchema})
    def create_movie(form: MovieAddSchema):
        """Creates a new movie.
        
        Arguments:
            form: movie's data.
        
        Returns a representation of the created movie.
        """
        try:
            session = Session()
            movie = Movie(title=form.title, genre=form.genre, release_date=form.release_date)
            session.add(movie)
            session.commit()
            return MovieRepresentation(movie), 200
        except IntegrityError as e:
            error_msg = 'Movie already exists.'
            return ErrorRepresentation(error_msg), 409
        except Exception as e:
            logger.error(e)
            error_msg = 'Error creating movie.'
            return ErrorRepresentation(error_msg), 400

    @app.delete('/api/v1/movie', tags=[movies_tag], responses={"200": ErrorSchema, "404": ErrorSchema})
    def delete_movie(form: MovieSearchSchema):
        """Deletes an movie.
        
        Arguments:
            form: movie's data.
        
        Returns a status message.
        """
        session = Session()
        movie = session.query(Movie).filter(Movie.id == form.id).first()
        if movie is None:
            error_msg = 'Movie not found.'
            return ErrorRepresentation(error_msg), 404
        else:
            session.delete(movie)
            session.commit()
            error_msg = f'Movie successfuly deleted.'
            return ErrorRepresentation(error_msg), 200
        
    @app.patch('/api/v1/movie', tags=[movies_tag], responses={"200": MovieViewSchema, "404": ErrorSchema, "400": ErrorSchema})
    def update_movie(form: MoviePatchSchema):
        """Updates an movie.
        
        Arguments:
            form: movie's data.
        
        Returns a representation of the updated movie.
        """
        session = Session()
        movie = session.query(Movie).filter(Movie.id == form.id).first()
        if movie is None:
            error_msg = 'Movie not found.'
            return ErrorRepresentation(error_msg), 404
        else:
            movie.title = form.title
            movie.genre = form.genre
            movie.release_date = form.release_date
            try:
                session.commit()
                return MovieRepresentation(movie), 200
            except Exception as e:
                error_msg = 'Error patching movie.'
                return ErrorRepresentation(error_msg), 400


    #
    # Actor-Movie Association
    #
    @app.get('/api/v1/actor-movie', tags=[actor_movies_tag], responses={"200": ActorMovieListSchema, "404": ErrorSchema})
    def get_associations():
        """Retrieves all actor-movie associations.
        
        Returns a representation of the list of associations.
        """
        session = Session()
        associations = session.query(ActorMovieAssociation).all()
        return ActorMovieListRepresentation(associations), 200
        
    @app.post('/api/v1/actor-movie', tags=[actor_movies_tag], responses={"200": ActorMovieViewSchema, "409": ErrorSchema, "400": ErrorSchema})
    def create_association(form: ActorMovieAddSchema):
        """Creates a new actor-movie association.
        
        Arguments:
            form: actor's and movie's id.
        
        Returns a representation of the created association.
        """
        try:
            session = Session()
            association = session.query(ActorMovieAssociation).filter(ActorMovieAssociation.actor_id == form.actor_id, ActorMovieAssociation.movie_id == form.movie_id).first()
            if association is not None:
                error_msg = 'Association already exists.'
                return ErrorRepresentation(error_msg), 409                    
            association = ActorMovieAssociation(actor_id=form.actor_id, movie_id=form.movie_id)
            session.add(association)
            session.commit()
            return ActorMovieRepresentation(association), 200
        except IntegrityError as e:
            error_msg = 'Invalid actor / movies ids provided.'
            return ErrorRepresentation(error_msg), 409
        except Exception as e:
            logger.error(e)
            error_msg = 'Error creating association.'
            return ErrorRepresentation(error_msg), 400

    @app.delete('/api/v1/actor-movie', tags=[actor_movies_tag], responses={"200": ErrorSchema, "404": ErrorSchema})
    def delete_association(form: ActorMovieSearchSchema):
        """Deletes an actor-movie association.
        
        Arguments:
            form: actor's and movie's id.
        
        Returns a status message.
        """
        session = Session()
        association = session.query(ActorMovieAssociation).filter(ActorMovieAssociation.actor_id == form.actor_id, ActorMovieAssociation.movie_id == form.movie_id).first()
        if association is None:
            error_msg = 'Association not found.'
            return ErrorRepresentation(error_msg), 404
        else:
            session.delete(association)
            session.commit()
            error_msg = f'Association successfuly deleted.'
            return ErrorRepresentation(error_msg), 200


    return app
 

#
# App instance
# 
app = create_app()
 
#
# Main program
# 
if __name__ == '__main__':
    app.run()
