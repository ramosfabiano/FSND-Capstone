# FSND-Capstone - Casting Agency
Capstone Project in the Udacity Full Stack NanoDegree program.

## Project Motivation

The objetive of this capstone project is to showcase the skills learned during the course.

In particular, we are implementing a *backend* , thus involving  data modelling, API design, role-based authentication/authorization, containerization and finally its deployment on a cloud platform.

The context of this application is a "Casting Agency", an imaginary company that is responsible for creating movies and managing and assigning actors to those movies. We are then creating an API that allows manipulating the actors and movies database.

## Technology Stack

The application is developed in Python 3.10.12, using the  [Flask](http://flask.pocoo.org/) framework. 

The database system used is [PostgreSQL](https://www.postgresql.org/), along with [SQLAlchemy](https://www.sqlalchemy.org/) Object Relational Mapper (ORM).

[Flask-CORS](https://flask-cors.readthedocs.io/) is used to  handle cross origin requests.

For authentication/authorization, we use [Json Web Tokens - JWTs](https://datatracker.ietf.org/doc/html/rfc7519) as handled by the [Auth0](https://auth0.com/) authentication and identity management platform.

The API is documented using [OpenAPI/Swagger](https://swagger.io/).

Optionally, [Docker](https://www.docker.com/) or [Podman](https://podman.io/) are required for running inside containers. They can be used interchangeably for this project.

Finally, we deploy our app on [Heroku](https://www.heroku.com/) Cloud platform.


## API Documentation

The API is documented using [Flask_OpenAPI3](https://luolingchun.github.io/flask-openapi3).

The documentation can be browsed online at `http://localhost:5000/` once the server is running.

![Screenshot](images/openapi.png)

The swagger page also provides an interface to test-drive the APIs.  Please refer to the [JWT](#JWT) section for information on where the obtain valid acccess tokens or disable authentication.

## External Services

### Database

We assume a postgres database server is configured and available for use. 

The `DATABASE_URL` environment variable should be used to point to the database, for instance:

```bash
export DATABASE_URL="postgresql://postgres:1234@localhost:5432/fsnd_capstone"
```

indicating a server at host `localhost`, port `5432`, user `postgres` , password `1234` and database `fsnd_capstone`.

The [containerized execution](#Containerized execution) option does not require an external postgres server.

### Authentication

For authentication, we assume an Auth0 account has been setup.

The following environment variables need to be set accordingly:

```bash
export AUTH0_DOMAIN="dev-rvbtc7dkfddvaibw.auth0.com" # tenant domain
export API_AUDIENCE="fsnd-capstone"                  # api audience
export ALGORITHMS="RS256"
```

Aditionally, for development purposes, authentication can be completely disabled/bypassed by setting the `ENABLE_AUTH=0` environment variable.

#### Authentication Details

##### Permissions

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
  
##### Roles

The following roles are required:

* Assistant: view permissions for actors and movies.
  *  `view:actors`
  *  `view:movies`

* Director: all permissions for actors plus view/update permissions for movies.
  * `view:actors`
  * `update:actors`
  * `delete:actors`
  * `post:actors`
  * `view:movies`
  * `update:movies`
    
* Producer: all permissions for actors and movies.
  * `view:actors`
  * `update:actors`
  * `delete:actors`
  * `post:actors`
  * `view:movies`
  * `update:movies`
  * `post:movies`
  * `delete:movies`

##### Users

* *assistant*, with the `Assistant` profile.
* *director*, with the `Director` profile.
* *producer*, with the `Producer` profile.

  
##### JWT

For project submission purposes, valid JWT access tokens are provided in `tests/auth.json`

These tokens are used by the unit tests, and can also be used for authentication in the Swagger documentation interface.

## Running Locally

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

### Running the application

*Optionally*, initialize the database with the testing content:

```bash
dropdb -U postgres fsnd_capstone
createdb -U postgres fsnd_capstone
psql -U postgres fsnd_capstone < fsnd_capstone.psql
```

Next, initialize the python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then, sure the environment variables related to the database and authentication are set. For convience, we provide the `setup.sh` script:

```bash
(venv) source ./setup.sh 
```

Finally launch the app:

```bash
(venv) flask run --reload --port 5000
```

### Running the tests

First, initialize the testing database:

```bash
dropdb -U postgres fsnd_capstone_test
createdb -U postgres fsnd_capstone_test
psql -U postgres fsnd_capstone_test < tests/fsnd_capstone_test.psql
```

Next, initialize the python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Also, make sure the environment variables related to the database and authentication are set. For convience, we provide the `tests/setup.sh` script:

```bash
(venv) source ./tests/setup.sh 
```

Finally launch the tests:

```bash
(venv) python -m unittest tests.test_app
```

### Containerized execution

We offer an alternative way of running the application based on docker/podman containers.

For this we encapsulate both the database and app installation together.

In order to launch the containerized version, first build the container images (done once):

```bash
 podman-compose build
```

Then launch the database/application bundle:

```bash
 podman-compose up
```

When finished, bring the containers down:

```bash
 podman-compose down
```

A couple of observations for the containerized execution:
* the environment variables are not read from `setup.sh`, but from `docker/*.env`. They are ingested automatically and do not require manual sourcing. If editing the `docker/*.env`, watch out for extra spaces ;) 
* the postgres container will keep its data files under `docker/postgres_data/`. This folder is automatically created and mounted inside the container.


## Cloud Deployment

For submission purposes, we have deployed the application to the [Heroku](https://www.heroku.com/) cloud provider.

URL and info of how to run the application...

This is an overview of the process...

**TODO:** complete


