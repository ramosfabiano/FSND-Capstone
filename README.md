# # FSND-Capstone - Casting Agency
Capstone Project in the Udacity Full Stack NanoDegree program.

## Project Motivation

The objetive of this capstone project is to showcase the skills learned during the course.

In particular, we are implementing a *backend* , thus involving  data modelling, API design, authentication/authorization and finally deployment on a cloud platform.

The context of this application is "Casting Agency", an imaginary company that is responsible for creating movies and managing and assigning actors to those movies.

The idea is to create an API that allows manipulating the actors and movies database.

## Technology Stack

The application is developed in Python 3.10.12, using the  [Flask](http://flask.pocoo.org/) framework. 

The database system used is [PostgreSQL](https://www.postgresql.org/), along with [SQLAlchemy](https://www.sqlalchemy.org/) Object Relational Mapper (ORM).

[Flask-CORS](https://flask-cors.readthedocs.io/) is used to  handle cross origin requests.

For authentication, we use  [Auth0](https://auth0.com/).

The API is documented using [Swagger](https://swagger.io/).

Finally, we deploy our app on [Heroku](https://www.heroku.com/) Cloud platform.


## API Documentation

The API is documented using OpenAPI/Swagger.

The documentation can be browsed only at `http://localhost:5000/doc` once the server is running.


## Setup

### Installing Dependencies

Using a python virtual environment is recommended for running the project locally:

```bash
python3 -m venv venv
source venv/bin/activate
```

Once the virtual environment is activated, the dependencies can be installed:

```bash
(venv) pip install -r requirements.txt
```

### Database Setup

We assume a local postgres database is configured and running within the local machine. Installing and configuring the database is outside the scope of this README.

### Auth0 Setup

An Auth0 account is required. Setting up such account is outside the scope of this README.

The following environment variables need to be set accordingly:

```bash
export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com" # tenant domain
export ALGORITHMS="RS256"
export API_AUDIENCE="castingagency"        # api audience
```

#### Permissions

The following invividual permissions are required:

* Actors
  * `view:actors`
  * `update:actors`
  * `delete:actors`
  * `post:actors`

* Movies
  * `view:movies`
  * `update:movies`
  * `post:movies`
  * `delete:movies`
  
#### Roles

The following roles are required:

* Assistant: 
  *  `view:actors`
  *  `view:movies`

* Director: 
  * `view:actors`
  * `update:actors`
  * `delete:actors`
  * `post:actors`
  * `view:movies`
  * `update:movies`
    
* Producer
  * `view:actors`
  * `update:actors`
  * `delete:actors`
  * `post:actors`
  * `view:movies`
  * `update:movies`
  * `post:movies`
  * `delete:movies`
  
### JWT Tokens

JWT Tokens needs to be stored in `auth.json`

In order to generate the tokens... **TODO:** complete

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

## Running Locally

First, initialize and activate the virtual environment previously setup. 

```bash
source venv/bin/activate
```

Make sure the `DATABASE_URL` is properly set `setup.sh`

```bash
(venv) source ./setup.sh 
```

**Please make sure the database is up and running.**

Finally launch the server locally:

```bash
(venv) flask run --reload --port 5000
```

## Handling database changes

In order to handle changes in the ORM, the Flask migration mechanism is supported.

First, initialize the migrations directory (needs to be done once):

```bash
(venv) flask db init
```

Next, create and apply a migration:

```bash
(venv) flask db migrate -m "optional message"
(venv) flask db update
```

The create/appy procedure should then be repeated everytime the ORM changes in the app.

### Running Tests

To run the tests, first load the testing database:

```bash
dropdb testdb
createdb testdb
psql testdb < testdb.psql
```

Then follow the same preliminary steps used to run the app locally, except that instead of running the flask app we run the test itself:

```bash
(venv) python test_app.py
```

## Hosting Instructions

Hosting at [Heroku](https://www.heroku.com/). Setting up and account and installing the heroku SDK is outside the scope of this README.

This is an overview of the process...

**TODO:** complete


