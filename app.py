import os
from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, abort, request
from flask_cors import CORS
from flask import redirect
import logging

from model import Session, Actor, Movie, ActorMovieAssociation, database_path
from schemas import *
from auth.auth import AuthError, requires_auth

#
# Enables or disables authentication
# 
enable_auth_var = os.getenv('ENABLE_AUTH')
auth_enabled = enable_auth_var is None or enable_auth_var != '0'

#
# Creates, initializes and runs the Flask application
#
def create_app():
    
    # openapi setup
    info = Info(title="FSND-Capstone", version="1.0.0")
    app = OpenAPI(__name__, info=info, security_schemes={"jwt": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}} if auth_enabled else None)
        
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
   
    logger.info(f'Starting the application... (auth_enabled={auth_enabled})')

    # cross-origin resource sharing
    CORS(app, resources={r"/api/*": {"origins": "*"}})
            
    #
    # Documentation
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
    @app.get('/api/v1/actors', tags=[actors_tag], responses={"200": ActorListSchema}, security=[{"jwt": []}] if auth_enabled else None)
    @requires_auth('view:actors', auth_enabled)
    def get_actors():
        """Retrieves all actors.
        
        Returns a representation of the list of actors.
        """
        session = Session()
        actors = session.query(Actor).all()
        return ActorListRepresentation(actors), 200

    @app.post('/api/v1/actors', tags=[actors_tag], responses={"200": ActorViewSchema, "422": ErrorSchema}, security=[{"jwt": []}] if auth_enabled else None)
    @requires_auth('post:actors', auth_enabled)
    def create_actor(form: ActorAddSchema):
        """Creates a new actor.
        
        Arguments:
            form: actor's data.
        
        Returns a representation of the created actor.
        """
        try:
            session = Session()
            actor = Actor(name=form.name, gender=form.gender, birth_date=form.birth_date, nationality=form.nationality)
            session.add(actor)
            session.commit()
            return ActorRepresentation(actor), 200
        except Exception as e:
            #logger.error(e)
            abort(422)
        
    @app.delete('/api/v1/actors/<int:id>', tags=[actors_tag], responses={"200": ActorViewSchema, "404": ErrorSchema, "422": ErrorSchema}, security=[{"jwt": []}] if auth_enabled else None)
    @requires_auth('delete:actors', auth_enabled)
    def delete_actor(path: ActorPathSchema):
        """Deletes an actor.
        
        Arguments:
            id: the actor's id.
        
        Returns a status message.
        """
        session = Session()
        actor = session.query(Actor).filter(Actor.id == path.id).first()
        if actor is None:
            abort(404)
        try:
            session.delete(actor)
            session.commit()
            return ActorRepresentation(actor), 200
        except Exception as e:
            #logger.error(e)
            abort(422)

    @app.patch('/api/v1/actors/<int:id>', tags=[actors_tag], responses={"200": ActorViewSchema, "404": ErrorSchema, "422": ErrorSchema}, security=[{"jwt": []}] if auth_enabled else None)
    @requires_auth('update:actors', auth_enabled)
    def update_actor(path: ActorPathSchema, form: ActorPatchSchema):
        """Updates an actor.
        
        Arguments:
            id: the actor's id.
            form: actor's data.
        
        Returns a representation of the updated actor.
        """        
        session = Session()
        actor = session.query(Actor).filter(Actor.id == path.id).first()
        if actor is None:
            abort(404)
        try:
            actor.name = form.name
            actor.gender = form.gender
            actor.birth_date = form.birth_date
            actor.nationality = form.nationality
            session.commit()
            return ActorRepresentation(actor), 200
        except Exception as e:
            #logger.error(e)
            abort(422)

    #
    # Movies
    #
    @app.get('/api/v1/movies', tags=[movies_tag], responses={"200": MovieListSchema}, security=[{"jwt": []}] if auth_enabled else None)
    @requires_auth('view:movies', auth_enabled)
    def get_movies():
        """Retrieves all movies.
        
        Returns a representation of the list of movies.
        """
        session = Session()
        movies = session.query(Movie).all()
        return MovieListRepresentation(movies), 200

    @app.post('/api/v1/movies', tags=[movies_tag], responses={"200": MovieViewSchema, "422": ErrorSchema}, security=[{"jwt": []}] if auth_enabled else None)
    @requires_auth('post:movies', auth_enabled)
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
            #logger.error(e)
            abort(422)

    @app.delete('/api/v1/movies/<int:id>', tags=[movies_tag], responses={"200": MovieViewSchema, "404": ErrorSchema, "422": ErrorSchema}, security=[{"jwt": []}] if auth_enabled else None)
    @requires_auth('delete:movies', auth_enabled)
    def delete_movie(path: MoviePathSchema):
        """Deletes an movie.
        
        Arguments:
            id: the movie's id.
        
        Returns a status message.
        """
        session = Session()
        movie = session.query(Movie).filter(Movie.id == path.id).first()
        if movie is None:
            abort(404)
        try:
            session.delete(movie)
            session.commit()
            return MovieRepresentation(movie), 200
        except Exception as e:
            #logger.error(e)
            abort(422)

    @app.patch('/api/v1/movies/<int:id>', tags=[movies_tag], responses={"200": MovieViewSchema, "404": ErrorSchema, "422": ErrorSchema}, security=[{"jwt": []}] if auth_enabled else None)
    @requires_auth('update:movies', auth_enabled)
    def update_movie(path: MoviePathSchema, form: MoviePatchSchema):
        """Updates an movie.
        
        Arguments:
            id: the movie's id.
            form: movie's data.
        
        Returns a representation of the updated movie.
        """
        session = Session()
        movie = session.query(Movie).filter(Movie.id == path.id).first()
        if movie is None:
            abort(404)
        try:
            movie.title = form.title
            movie.genre = form.genre
            movie.release_date = form.release_date
            session.commit()
            return MovieRepresentation(movie), 200
        except Exception as e:
            #logger.error(e)
            abort(422) 

    #
    # Actor-Movie Association
    # 
    @app.post('/api/v1/actor-movie', tags=[actor_movies_tag], responses={"200": ActorMovieSchema, "422": ErrorSchema}, security=[{"jwt": []}] if auth_enabled else None)
    @requires_auth('update:movies', auth_enabled)
    def create_association(form: ActorMovieSchema):
        """Creates a new actor-movie association.
        
        Arguments:
            form: actor's and movie's id.
        
        Returns a status message.
        """
        try:
            session = Session()
            actor_movie = ActorMovieAssociation(actor_id=form.actor_id,  movie_id=form.movie_id, character_name=form.character_name)
            session.add(actor_movie)
            session.commit()
            return ActorMovieRepresentation(actor_movie), 200
        except Exception as e:
            #logger.error(e)
            abort(422)

    @app.delete('/api/v1/actor-movie', tags=[actor_movies_tag], responses={"200": ActorMovieSchema, "404": ErrorSchema, "422": ErrorSchema}, security=[{"jwt": []}] if auth_enabled else None)
    @requires_auth('update:movies', auth_enabled)
    def delete_association(form: ActorMovieDeleteSchema):
        """Deletes an actor-movie association.
        
        Arguments:
            form: actor's and movie's id.
        
        Returns a status message.
        """
        session = Session()
        actor_movie = session.query(ActorMovieAssociation).filter(ActorMovieAssociation.actor_id==form.actor_id, ActorMovieAssociation.movie_id==form.movie_id).first()
        if (actor_movie is None):
            abort(404)   
        try:
            session.delete(actor_movie)
            session.commit()            
            return ActorMovieRepresentation(actor_movie), 200
        except Exception as e:
            #logger.error(e)
            abort(422)

    #
    # Error handlers
    #
    @app.errorhandler(400)
    def bad_request(error):
        return ErrorRepresentation('Bad request.'), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return ErrorRepresentation('Unauthorized.'), 401

    @app.errorhandler(404)
    def not_found(error):
        return ErrorRepresentation('Resource not found.'), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return ErrorRepresentation('Processing of request failed.'), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return ErrorRepresentation('Internal server error.'), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(error):    
        return ErrorRepresentation(f'Not authorized: {error.error_message}'), error.status_code
    
    
    return app
 
#
# Main program
# 
if __name__ == '__main__':
    app = create_app()
    app.run()
