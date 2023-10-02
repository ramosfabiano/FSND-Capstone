import os
from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, abort
from flask_cors import CORS
from flask import redirect
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
import logging

from model import Session, Actor, Movie, database_path
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
   
    logger.info('Starting the application...')

    # cross-origin resource sharing
    CORS(app, resources={r"/api/*": {"origins": "*"}})
            
    #
    # Actors
    #
    @app.get('/', tags=[home_tag])
    def home():
        """Redirects to documentation page.
        """
        return redirect('/openapi/swagger')

    @app.get('/api/v1', tags=[home_tag])
    def v1_home():
        """Redirects to documentation page.
        """
        return redirect('/openapi/swagger')

    #
    # Endpoints (actors)
    #
    @app.get('/api/v1/actors', tags=[actors_tag], responses={"200": ActorListSchema})
    def get_actors():
        """Retrieves all actors.
        
        Returns a representation of the list of actors.
        """
        session = Session()
        actors = session.query(Actor).all()
        return ActorListRepresentation(actors), 200

    @app.post('/api/v1/actor', tags=[actors_tag], responses={"200": ActorViewSchema, "422": ErrorSchema})
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
        except Exception as e:
            logger.error(e)
            abort(422)

    @app.delete('/api/v1/actor', tags=[actors_tag], responses={"200": SuccessSchema, "404": ErrorSchema, "422": ErrorSchema})
    def delete_actor(form: ActorSearchSchema):
        """Deletes an actor.
        
        Arguments:
            form: actor's data.
        
        Returns a status message.
        """
        session = Session()
        actor = session.query(Actor).filter(Actor.id == form.id).first()
        if actor is None:
            abort(404)
        else:
            try:
                session.delete(actor)
                session.commit()
                return SuccessRepresentation(), 200
            except Exception as e:
                logger.error(e)
                abort(422)

    @app.patch('/api/v1/actor', tags=[actors_tag], responses={"200": ActorViewSchema, "404": ErrorSchema, "422": ErrorSchema})
    def update_actor(form: ActorPatchSchema):
        """Updates an actor.
        
        Arguments:
            form: actor's data.
        
        Returns a representation of the updated actor.
        """
        session = Session()
        actor = session.query(Actor).filter(Actor.id == form.id).first()
        if actor is None:
            abort(404)
        else:
            try:
                actor.name = form.name
                actor.gender = form.gender
                actor.birth_date = form.birth_date
                actor.email = form.email
                session.commit()
                return ActorRepresentation(actor), 200
            except Exception as e:
                logger.error(e)
                abort(422)

    #
    # Movies
    #
    @app.get('/api/v1/movies', tags=[movies_tag], responses={"200": MovieListSchema})
    def get_movies():
        """Retrieves all movies.
        
        Returns a representation of the list of movies.
        """
        session = Session()
        movies = session.query(Movie).all()
        return MovieListRepresentation(movies), 200

    @app.post('/api/v1/movie', tags=[movies_tag], responses={"200": MovieViewSchema, "422": ErrorSchema})
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
        except Exception as e:
            logger.error(e)
            abort(422)

    @app.delete('/api/v1/movie', tags=[movies_tag], responses={"200": SuccessSchema, "404": ErrorSchema, "422": ErrorSchema})
    def delete_movie(form: MovieSearchSchema):
        """Deletes an movie.
        
        Arguments:
            form: movie's data.
        
        Returns a status message.
        """
        session = Session()
        movie = session.query(Movie).filter(Movie.id == form.id).first()
        if movie is None:
            abort(404)
        else:
            try:
                session.delete(movie)
                session.commit()
                return SuccessRepresentation(), 200
            except Exception as e:
                logger.error(e)
                abort(422)

    @app.patch('/api/v1/movie', tags=[movies_tag], responses={"200": MovieViewSchema, "404": ErrorSchema, "422": ErrorSchema})
    def update_movie(form: MoviePatchSchema):
        """Updates an movie.
        
        Arguments:
            form: movie's data.
        
        Returns a representation of the updated movie.
        """
        session = Session()
        movie = session.query(Movie).filter(Movie.id == form.id).first()
        if movie is None:
            abort(404)
        else:
            try:
                movie.title = form.title
                movie.genre = form.genre
                movie.release_date = form.release_date
                session.commit()
                return MovieRepresentation(movie), 200
            except Exception as e:
                logger.error(e)
                abort(422) 

    #
    # Actor-Movie Association
    # 
    @app.post('/api/v1/actor-movie', tags=[actor_movies_tag], responses={"200": SuccessSchema, "422": ErrorSchema})
    def create_association(form: ActorMovieSchema):
        """Creates a new actor-movie association.
        
        Arguments:
            form: actor's and movie's id.
        
        Returns a status message.
        """
        try:
            session = Session()
            actor = session.query(Actor).filter(Actor.id == form.actor_id).first()
            movie = session.query(Movie).filter(Movie.id == form.movie_id).first()
            actor.movies.append(movie)
            #movie.actors.append(actor)
            session.commit()
            return SuccessRepresentation(), 200
        except Exception as e:
            logger.error(e)
            abort(422)

    @app.delete('/api/v1/actor-movie', tags=[actor_movies_tag], responses={"200": SuccessSchema, "422": ErrorSchema})
    def delete_association(form: ActorMovieSchema):
        """Deletes an actor-movie association.
        
        Arguments:
            form: actor's and movie's id.
        
        Returns a status message.
        """
        try:
            session = Session()
            actor = session.query(Actor).filter(Actor.id == form.actor_id).first()
            movie = session.query(Movie).filter(Movie.id == form.movie_id).first()      
            actor.movies.remove(movie)
            #movie.actors.remove(actor) 
            session.commit()
            return SuccessRepresentation(), 200
        except Exception as e:
            logger.error(e)
            abort(422)

    return app
 

#
# App instance
# 
app = create_app()

#
# Error handlers
#
@app.errorhandler(400)
def bad_request(error):
    return ErrorRepresentation('Bad request.'), 400

@app.errorhandler(404)
def not_found(error):
    return ErrorRepresentation('Resource not found.'), 404

@app.errorhandler(422)
def unprocessable(error):
    return ErrorRepresentation('Processing of request failed.'), 422

@app.errorhandler(500)
def internal_server_error(error):
    return ErrorRepresentation('Internal server error.'), 500
 
#
# Main program
# 
if __name__ == '__main__':
    app.run()
