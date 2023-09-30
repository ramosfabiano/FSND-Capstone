import os
from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask
from flask_cors import CORS
from flask import redirect
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import logging

from model import Session, Actor, database_path
from schemas import *

#
# Allows the application to run database migrations
#
def setup_migrations(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path  
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)  
    
#
# Creates, initializes and runs the Flask application
#
def create_app(test_config=None):
    # openapi setup
    info = Info(title="FSND-Capstone", version="1.0.0")
    app = OpenAPI(__name__, info=info)
    
    # migrations
    setup_migrations(app)  

    # avoid alphabetic ordering of the schema attributes in the documentation.
    app.json.sort_keys = False

    # configures logging
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
   
    #logger.info('Starting the application...')

    # cross-origin resource sharing
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # openapi tags
    home_tag = Tag(name="Documentation", description="OpenAPI documentation")
    actors_tag = Tag(name="Actors", description="Actors API documentation")
    directors_tag = Tag(name="Directors", description="Directors API documentation")
    movies_tag = Tag(name="Movies", description="Movies API documentation")
            
    #
    # Endpoints (documentation)
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
            actor = Actor(id=form.id, name=form.name, gender=form.gender, birth_date=form.birth_date, email=form.email)
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
        
        Returns a representation of the deleted actor.
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
            actor.id = form.id
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
    # Endpoints (movies)
    #
    # TODO


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
