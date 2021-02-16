# Full Stack Nanodegree Capston Project: Casting Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

- live url: https://casting-agency-fsnd-prjct.herokuapp.com

```
├── CastingAgency.postman_collection.json # collection of requests to test RBAC controls, and can be imported by postman
├── Procfile # a recognized file by heroku, and it will be used it to tell heroku which WSGI Server to use with our app
├── app.py  # main file to run the application
├── auth.py # contains teh authentication logic
├── manage.py # implemnted using flask_script to run flask-migrate command through and to use it in heroku's production environment
├── migrations # folder managed by flask-migrate
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 606d1cf32457_.py
│       ├── 781514ca1ada_.py
│       ├── 9c9dabdae17e_.py
│       └── daaf819e8285_.py
├── models.py  # business logic of data modeling using ORM library
├── requirements.txt # contains all packages to run the application along with their versions. used by pip to install
├── setup.sh   # contains enviornment variables used by the application and it conntains tokens for inspection purposes
└── test_app.py   # used to test api endpoints
```

## Getting Started

## Initial Setup

1. Fork this project to your Github account.
2. Locally clone your forked version to begin working on the project.

### Installing Dependencies

#### Python 3.7

the version used to develop the application.

#### PostgresSQL

[download](https://www.postgresql.org/download/) PostgresSQL if you haven't yet

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
$ pip install -r requirements.txt
```

This will install all of the required dependencies to run the application.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [psycopg2](https://pypi.org/project/psycopg2/) Psycopg is the most popular PostgreSQL database adapter for the Python programming language.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the database. You'll primarily work in app.py and can reference models.py.

- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) is an extension for Flask that adds support for SQLAlchemy to your application.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [python-jose](https://pypi.org/project/python-jose/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [gunicorn](https://gunicorn.org/) is a Python WSGI HTTP server, that will be used instead of [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/) when the application is deployed

#### Postman

for API endpoints testing purposes.

## Database Setup

With Postgres running, create database named `casting_agency` using createdb tool:

```bash
$ createdb casting_agency
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
$ source setup.sh
$ export FLASK_APP=app.py
$ python manage.py db upgrade
$ flask run --reload
```

Setting the `FLASK_APP` variable to `app.py` directs flask to run `app.py` whenever `flask run` is issued.

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation

### Base URL

you can use `http://127.0.0.1:5000` if you want to test the application locally or use `https://casting-agency-fsnd-prjct.herokuapp.com`

### Errors

#### 400 Bad Request

```
{
   "success" : false,
   "message" : "Bad Request",
   "error" : 400
}
```

#### 404 Not Found

```
{
   "message" : "Not Found",
   "success" : false,
   "error" : 404
}
```

#### 405 Method Not Allowed

```
{
   "success" : false,
   "message" : "Method Not Allowed",
   "error" : 405
}
```

#### 422 Unprocessable Entity

```
{
   "success" : false,
   "message" : "Unprocessable Entity",
   "error" : 422
}
```

#### 500 Internal Server Error

```
{
   "success" : false,
   "message" : "Internal Server Error",
   "error" : 500
}
```

#### 401 Unauthorized

The client must pass authentication before access to this resource is granted. The server cannot validate the identity of the requested party.

#### 403 Forbidden

The client does not have permission to access the resource. Unlike 401, the server knows who is making the request, but that requesting party has no authorization to access the resource.

### Resource endpoint library

Endpoints

- GET '/movies'
- GET '/actors'
- POST '/movies'
- POST '/actors'
- PATCH '/movies/<int:movie_id>'
- PATCH '/actors/<int:actor_id>'
- DELETE '/movies/<int:movie_id>'
- DELETE '/actors/<int:actor_id>'

#### GET '/movies'

- All movies:

Request specefications:

- String query: None
- Arguments: None
- Body: None

##### getting movies

```
curl --location --request GET 'http://127.0.0.1:5000/movies' \
--header 'Authorization: Bearer <TOKEN>'
```

Response example:

```
{
    "movies": [
        {
            "id": 10,
            "release_date": "02/01/2025",
            "title": "Star Wars 20"
        },
        {
            "id": 11,
            "release_date": "02/01/2060",
            "title": "The Lord of the Rings 13"
        },
        {
            "id": 12,
            "release_date": "01/06/2030",
            "title": "Inception 3"
        },
        {
            "id": 13,
            "release_date": "01/15/2035",
            "title": "The Matrix 5"
        },
        {
            "id": 14,
            "release_date": "01/20/2035",
            "title": "Interstellar 2"
        }
    ],
    "status": 200,
    "success": true
}
```

#### GET '/actors'

- All actors:

Request specefications:

- String query: None
- Arguments: None
- Body: None

##### getting actors

```
curl --location --request GET 'http://127.0.0.1:5000/actors' \
--header 'Authorization: Bearer <TOKEN>'
```

Example response:

```
{
    "actors": [
        {
            "age": 45,
            "gender": "m",
            "id": 10,
            "name": "Leonardo DiCaprio"
        },
        {
            "age": 39,
            "gender": "m",
            "id": 12,
            "name": "Rami Malek"
        }
    ],
    "status": 200,
    "success": true
}
```

#### DELETE '/mvoies/&lt;int:movie_id&gt;'

- Deletes specific movie:

Request specefications:

- String query: None
- Arguments: id to specify a movie from the collection
- Body: None

##### deleting movie

```
curl --location --request DELETE 'http://127.0.0.1:5000/movies/21' \
--header 'Authorization: Bearer <TOKEN>'
```

Example response:

```
{
    "id": 21,
    "status": 200,
    "success": true
}
```

#### DELETE '/actors/&lt;int:actor_id&gt;'

- Deletes specific actor:

Request specefications:

- String query: None
- Arguments: id to specify an actor from the collection
- Body: None

##### deleting actor

```
curl --location --request DELETE 'http://127.0.0.1:5000/actors/12' \
--header 'Authorization: Bearer <TOKEN>'
```

Example response:

```
{
    "id": 12,
    "status": 200,
    "success": true
}
```

#### POST '/movies'

- Adds movies:

Request specefications:

- String query: None
- Arguments: None
- Body:
  ```
  {
     "title":"<MOVIE TITLE>",
     "release_date":"<MOVIE RELEASE DATE>"
  }
  ```

##### adding movie

```
curl --location --request POST 'http://127.0.0.1:5000/movies' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
   "title":"Star Wars 20",
   "release_date":"1-26-2025"
}'
```

Example response:

```
{
    "movie": {
        "id": 21,
        "release_date": "01/26/2025",
        "title": "Star Wars 20"
    },
    "status": 200,
    "success": true
}
```

#### POST '/actors'

- Adds actors:

Request specefications:

- String query: None
- Arguments: None
- Body:
  ```
  {
     "name":"<ACTOR NAME>",
     "age":<ACTOR AGE>,
     "gender":"<ACTOR GENDER>"
  }
  ```

##### adding actor

```
curl --location --request POST 'http://127.0.0.1:5000/actors' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
   "name":"Leonardo DiCaprio",
   "age":45,
   "gender":"m"
}'
```

Example response:

```
{
    "actor": {
        "age": 45,
        "gender": "m",
        "id": 14,
        "name": "Leonardo DiCaprio"
    },
    "status": 200,
    "success": true
}
```

#### PATCH '/movies/<int:movie_id>'

- Modifies movies:

Request specefications:

- String query: None
- Arguments: id to specify a movie from the collection
- Body:
  ```
  {
          "title": "<NEW TITLE NAME>",
          "release_date": "<NEW RELEASE DATE>"
  }
  ```

##### modifying movie

```
curl --location --request PATCH 'http://127.0.0.1:5000/movies/14' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
   "title":"back to the future 11"
}'
```

Example response:

```
{
    "movie": {
        "id": 14,
        "release_date": "01/20/2035",
        "title": "back to the future 11"
    },
    "status": 200,
    "success": true
}
```

#### PATCH '/actors/<int:actor_id>'

- modifies actors:

Request specefications:

- String query: None
- Arguments: id to specify an actor from the collection
- Body:
  ```
  {
          "name": "<NEW NAME>",
          "age":<NEW AGE>,
          "gender": "<NEW GENDER>"
  }
  ```

##### modifying actor

```
curl --location --request PATCH 'http://127.0.0.1:5000/actors/15' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "age": 40
}'
```

Example response:

```
{
    "actor": {
        "age": 40,
        "gender": "m",
        "id": 15,
        "name": "Rami Malek"
    },
    "status": 200,
    "success": true
}
```

## Authentication Setup

the steps i followed to setup 3rd party authentication system auth0 :-

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, regular web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:movies`
   - `get:actors`
   - `post:movies`
   - `post:actors`
   - `patch:movies`
   - `patch:actors`
   - `delete:movies`
   - `delete:actors`
6. Create new roles for:
   - Casting Assistant
     - Can `get:movies` and `get:actors`
   - Casting Director
     - can perform all Casting Assistant actions has and…
     - can `post:actors` and `delete:actors`
     - can `patch:actors` and `patch:actors`
   - Executive Producer
     - All permissions a Casting Director has and…
     - can `post:movies` and `delete:movies`
7. Obtain you JWT tokens
   according to the [api docs](https://auth0.com/docs/api/authentication#authentication-methods) of auth0 there are two ways to login
   - Implicit Flow recommended for front end use
     ```
     GET https://YOUR_DOMAIN/authorize?
       audience=API_IDENTIFIER&
       response_type=token
       client_id=YOUR_CLIENT_ID&
       redirect_uri=https://YOUR_APP/callback&
     ```
     redirects and returns jwt token
   - Authorization Code Flow recommended for regular web apps or testing use, where you can as a developer issue token that can expire in 7 days for example
     ```
     GET https://YOUR_DOMAIN/authorize?
       audience=API_IDENTIFIER&
       response_type=code&
       client_id=YOUR_CLIENT_ID&
       redirect_uri=https://YOUR_APP/callback&
     ```
     redirects and returns AUTHORIZATION_CODE that can be used against POST /oauth/token endpoint to exchange Authorization Code for a token
     ```
     POST https://YOUR_DOMAIN/oauth/token
     Content-Type: application/x-www-form-urlencoded

     grant_type=authorization_code&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&code=AUTHORIZATION_CODE&redirect_uri=https://YOUR_APP/callback
     ```
     and if you want to logout then use this url `https://YOUR_DOMAIN/v2/logout` regardless of which flow

## Endpoints Testing

```
$ dropdb casting_agency
$ createdb casting_agency
$ source setup.sh
$ python test_app.py
```

## RBAC Controls Testing

Test endpoints with [Postman](https://getpostman.com).

- Import the postman collection `./CastingAgency.postman_collection.json.json`
- If you want to test the application at live, then change the `app_url` variable from the collection by right-clicking the collection folder >> edit >> navigate to variables tab >> change variable value to `https://casting-agency-fsnd-prjct.herokuapp.com`. Or keep it `http://127.0.0.1:5000` if you want to test the local app after running the server using `flask run --reload`

## Deployment

[heroku](https://heroku.com/) is the cloud enviornment of choice, create an acount if you don't have and install the cli tool from [here](https://devcenter.heroku.com/categories/command-line) and use `heroku login` command to set your credentials.

- deploying to heroku instructions

```
$ git init
$ heroku create app-name
$ git remote -v # check if it is connected to heroku
$ git remote add heroku git_repo_url # if not, connecte it to your app heroku repo
$ heroku addons:create heroku-postgresql:hobby-dev --app app-name # add free tier postgres service
$ heroku config --app casting-agency-fsnd-prjct # check database url
# add environment variables to app using heroku web interface like AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE
$ pip freeze > requirements.txt # update requirements.txt
$ git add .
$ git commit -m 'add all'
$ git push heroku master
$ heroku run python manage.py db upgrade --app casting-agency-fsnd-prjct # instructing flask-migrate through manage.py to upgrade database schema to our database service or creates tables if it was not there for the first time
```

## Acknowledgment

i would like to express my gratitude to Udacity, Misk, and our session lead Abdullah Alhamzani
