# FSND-Capstone - Casting Agency
Capstone Project in the Udacity Full Stack NanoDegree program.

## Project Motivation

The objective of this capstone project is to showcase the skills learned during the course.

In particular, we are implementing (from scratch) a *backend* , thus involving  data modelling, API design, role-based authentication/authorization, containerization and finally its deployment on a cloud platform.

The context of this application is a "Casting Agency", an imaginary company that is responsible for creating and managing movies, actors, and their associations.

## Technology Stack

The application was developed in Python 3.10.12, using the [Flask](http://flask.pocoo.org/) framework. 

The database system used was [PostgreSQL](https://www.postgresql.org/), along with [SQLAlchemy](https://www.sqlalchemy.org/) Object Relational Mapper (ORM).

[Flask-CORS](https://flask-cors.readthedocs.io/) was used to  handle cross origin requests.

For authentication/authorization, we used [Json Web Tokens - JWTs](https://datatracker.ietf.org/doc/html/rfc7519), managed by the [Auth0](https://auth0.com/) authentication and identity management platform.

The API was documented using [OpenAPI/Swagger](https://swagger.io/).

Optionally, [Podman](https://podman.io/) is required for containerized execution.

Finally, we deployed our app on the [Heroku](https://www.heroku.com/) Cloud platform.


## API Documentation

The API is documented using [Flask_OpenAPI3](https://luolingchun.github.io/flask-openapi3).

The documentation can be browsed online at `http://localhost:5000/` once the server is running.

![Screenshot](images/openapi.png)

The documentation page also provides an interface to test-drive the APIs.  Please refer to the [JWT](#JWT) section for information regarding acccess tokens.

## External Services

### Database

We assume a postgres database server is configured and available for use. 

The `DATABASE_URL` environment variable should be used to point to the database, for instance:

```bash
export DATABASE_URL="postgresql://postgres:1234@localhost:5432/fsnd_capstone"
```

indicating a server at host `localhost`, port `5432`, user `postgres` , password `1234` and database `fsnd_capstone`.

The containerized execution option, described later in this document, does not require an external postgres server.

### Authentication

For authentication, we assume an Auth0 account has been setup.

The following environment variables need to be set accordingly:

```bash
export AUTH0_DOMAIN="dev-rvbtc7dkfddvaibw.auth0.com" # tenant domain
export API_AUDIENCE="fsnd-capstone"                  # api audience
export ALGORITHMS="RS256"
```

Aditionally, for development purposes, authentication can be completely disabled/bypassed by setting the `ENABLE_AUTH=0` environment variable.

For submission purposes only, in order to match the rubric, we have also provided the a client's ID and SECRET in the  `setup.sh` initialization script.

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

For project submission purposes, valid JWT access tokens for 3 users (`assistant`, `director` and `producer`) are provided in `tests/auth.json`.

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

Then, make sure the environment variables related to the database and authentication are set. For convience, we provide the `setup.sh` script:

```bash
(venv) source ./setup.sh 
```

Finally launch the app:

```bash
(venv) flask run --reload --port 5000
```

### Running the tests

First, initialize the testing database (mandatory):

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

If a code coverage report is desired, run the tests using the `coverage` module instead:

```bash
(venv) coverage run --source=.  -m unittest tests.test_app
(venv) coverage report -m
(venv) coverage html
```

### Containerized execution

We offer an alternative way of running the application using docker/podman containers.

For this we bundle both the database and app installation together using `podman-compose`.

In order to launch the containerized version, first build the container images:

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

A couple of observations for the containerized execution option:
* The environment variables are not read from `setup.sh`, but from `docker/*.env`. They are ingested automatically and do not require manual sourcing. Tip: if editing the `docker/*.env`, watch out for extra white spaces ;) 
* The postgres container will keep its data files under `docker/postgres_data/`. This folder is automatically created and mounted inside the postgres container.

The postgres container is set so that it will automatically load data if the database is uninitialized.

Manually resetting the database is also possible. First, make sure the app container is stopped:

```bash
podman-compose down app
```

Then open a terminal inside the container and load the database:

```bash
podman-compose exec postgres /bin/bash
root@a3d4770da7d3:/scripts# dropdb -U postgres fsnd_capstone
root@a3d4770da7d3:/scripts# createdb -U postgres fsnd_capstone
root@a3d4770da7d3:/scripts# psql -U postgres fsnd_capstone < fsnd_capstone.psql
```

Opening a `psql` session is also possible:

```bash
podman-compose exec postgres psql -U postgres fsnd_capstone
fsnd_capstone=# select count(*) from actor;
```

## Cloud Deployment

For submission purposes, we have deployed the application to the [Heroku](https://www.heroku.com/) cloud provider.

For access tokens to be used for testing, please refer to the [JWT](#JWT) section.

The app is deployed and live [here](https://fsnd-capstone-74a9cd403748.herokuapp.com/).



