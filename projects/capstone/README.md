# Full Stack Nanodegree Capston Project: Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

```
├── CastingAgency.postman_collection.json
├── Procfile
├── app.py
├── auth.py
├── manage.py
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 606d1cf32457_.py
│       ├── 781514ca1ada_.py
│       ├── 9c9dabdae17e_.py
│       └── daaf819e8285_.py
├── models.py
├── requirements.txt
├── setup.sh
└── test_app.py
```
## Getting Started
# Initial Setup
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
pip install -r requirements.txt
```

This will install all of the required dependencies to run the application.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [psycopg2](https://pypi.org/project/psycopg2/) Psycopg is the most popular PostgreSQL database adapter for the Python programming language.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) is an extension for Flask that adds support for SQLAlchemy to your application.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [python-jose](https://pypi.org/project/python-jose/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

##### Postman
for API endpoints testing purposes.

## Database Setup
With Postgres running, create database named `casting_agency` using createdb tool:
```bash
createdb casting_agency
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
flask run --reload
```

Setting the `FLASK_APP` variable to `app.py` directs flask to run `app.py` whenever `flask run` is issued.

The `--reload` flag will detect file changes and restart the server automatically.


## API DOCUMENTATION
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

Response example:
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
- Deletes specific question:

Request specefications:
- String query: None
- Arguments: id to specify a movie from the collection
- Body: None


Response example:
```
{
    "id": 21,
    "status": 200,
    "success": true
}
```
#### DELETE '/actors/&lt;int:actor_id&gt;'
- Deletes specific question:

Request specefications:
- String query: None
- Arguments: id to specify an actor from the collection
- Body: None


Response example:
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
       "title":"Star Wars 20",
       "release_date":"1-26-2025"
    }
    ```
##### adding the movie
```
curl --location --request POST 'http://127.0.0.1:5000//movies' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
   "title":"Star Wars 20",
   "release_date":"1-26-2025"
}'
```
example Response:
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
##### adding the actor
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
Response example:
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
#### PATCH '/movies'
- Adds movies:

Request specefications:
- String query: None
- Arguments: None
- Body:
    ```
    {
            "title": "<NEW TITLE NAME>",
            "release_date": "<NEW RELEASE DATE>"
    }
    ```

##### modifying the movie
```
curl --location --request PATCH 'http://127.0.0.1:5000/movies/14' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
   "title":"back to the future 11"
}'
```
example Response:
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

#### GET '/categories/&lt;int:category_id&gt;/questions'
- All questions that belong to specific category:

Request specefications:
- String query: None
- Arguments: id to specify the category from the categories collection
- Body: None

curl localhost:5000/categories/4/questions

Response example:
```
{
   "current_category" : 4,
   "questions" : [
      {
         "id" : 5,
         "answer" : "Maya Angelou",
         "difficulty" : 2,
         "category" : 4,
         "question" : "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      {
         "answer" : "Linus Torvalds",
         "difficulty" : 4,
         "id" : 25,
         "category" : 4,
         "question" : "who created Linux'?"
      }
   ],
   "success" : true,
   "total_questions" : 2
}
```
#### POST '/quizzes'
- Gets random question to play a game, out of the provided list of question IDs and in a specific category if provided:

Request specefications:
- String query: None
- Arguments: None
- Body: 
```
{
  "previous_questions": "",
  "quiz_category": {
    "type": {
      "id": "4",
      "type": "History"
    }
  }
}
```

```
curl localhost:5000/quizzes -H 'Content-Type: application/json' -d '{"previous_questions":"","quiz_category":{"type":{"id":"4","type":"History"}}}'
```

Response example:
```
{
   "question" : {
      "category" : 4,
      "difficulty" : 4,
      "id" : 25,
      "question" : "who created Linux'?",
      "answer" : "Linus Torvalds"
   },
   "success" : true
}
```

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Dillinger is a cloud-enabled, mobile-ready, offline-storage, AngularJS powered HTML5 Markdown editor.

  - Type some Markdown on the left
  - See HTML in the right
  - Magic

# New Features!

  - Import a HTML file and watch it magically convert to Markdown
  - Drag and drop images (requires your Dropbox account be linked)


You can also:
  - Import and save files from GitHub, Dropbox, Google Drive and One Drive
  - Drag and drop markdown and HTML files into Dillinger
  - Export documents as Markdown, HTML and PDF

Markdown is a lightweight markup language based on the formatting conventions that people naturally use in email.  As [John Gruber] writes on the [Markdown site][df1]

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.

### Tech

Dillinger uses a number of open source projects to work properly:

* [AngularJS] - HTML enhanced for web apps!
* [Ace Editor] - awesome web-based text editor
* [markdown-it] - Markdown parser done right. Fast and easy to extend.
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [node.js] - evented I/O for the backend
* [Express] - fast node.js network app framework [@tjholowaychuk]
* [Gulp] - the streaming build system
* [Breakdance](https://breakdance.github.io/breakdance/) - HTML to Markdown converter
* [jQuery] - duh

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

### Installation

Dillinger requires [Node.js](https://nodejs.org/) v4+ to run.

Install the dependencies and devDependencies and start the server.

```sh
$ cd dillinger
$ npm install -d
$ node app
```

For production environments...

```sh
$ npm install --production
$ NODE_ENV=production node app
```

### Plugins

Dillinger is currently extended with the following plugins. Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md][PlDb] |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |
| OneDrive | [plugins/onedrive/README.md][PlOd] |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |


### Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantaneously see your updates!

Open your favorite Terminal and run these commands.

First Tab:
```sh
$ node app
```

Second Tab:
```sh
$ gulp watch
```

(optional) Third:
```sh
$ karma test
```
#### Building for source
For production release:
```sh
$ gulp build --prod
```
Generating pre-built zip archives for distribution:
```sh
$ gulp build dist --prod
```
### Docker
Dillinger is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the Dockerfile if necessary. When ready, simply use the Dockerfile to build the image.

```sh
cd dillinger
docker build -t joemccann/dillinger:${package.json.version} .
```
This will create the dillinger image and pull in the necessary dependencies. Be sure to swap out `${package.json.version}` with the actual version of Dillinger.

Once done, run the Docker image and map the port to whatever you wish on your host. In this example, we simply map port 8000 of the host to port 8080 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 8000:8080 --restart="always" <youruser>/dillinger:${package.json.version}
```

Verify the deployment by navigating to your server address in your preferred browser.

```sh
127.0.0.1:8000
```

#### Kubernetes + Google Cloud

See [KUBERNETES.md](https://github.com/joemccann/dillinger/blob/master/KUBERNETES.md)


### Todos

 - Write MORE Tests
 - Add Night Mode

License
----

MIT


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
