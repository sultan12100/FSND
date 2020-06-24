# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


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
- GET '/categories'
- GET '/questions'
- DELETE '/questions/<int:question_id>'
- POST '/questions'
- GET '/categories/<int:category_id>/questions'
- POST '/quizzes'

#### GET '/categories'
- All categories:

Request specefications:
- String query: None
- Arguments: None
- Body: None

curl localhost:5000/categories

Response example:
```
{
   "categories" : [
      {
         "type" : "Science",
         "id" : 1
      },
      {
         "type" : "Art",
         "id" : 2
      },
      {
         "id" : 3,
         "type" : "Geography"
      },
      {
         "type" : "History",
         "id" : 4
      },
      {
         "id" : 5,
         "type" : "Entertainment"
      },
      {
         "id" : 6,
         "type" : "Sports"
      }
   ],
   "success" : true,
   "total_categories" : 6
}
```
#### GET '/questions'
- All questions:

Request specefications:
- String query: None
- Arguments: None
- Body: None

curl localhost:5000/questions

Response example:
```
{
   "questions" : [
      {
         "answer" : "Apollo 13",
         "category" : 5,
         "question" : "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
         "id" : 2,
         "difficulty" : 4
      },
      {
         "answer" : "Tom Cruise",
         "category" : 5,
         "question" : "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
         "id" : 4,
         "difficulty" : 4
      },
      {
         "answer" : "Maya Angelou",
         "category" : 4,
         "question" : "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
         "id" : 5,
         "difficulty" : 2
      },
      {
         "id" : 6,
         "question" : "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
         "difficulty" : 3,
         "category" : 5,
         "answer" : "Edward Scissorhands"
      }
   ],
   "total_questions" : 4,
   "success" : true,
   "categories" : [
      {
         "type" : "Science",
         "id" : 1
      },
      {
         "type" : "Art",
         "id" : 2
      },
      {
         "type" : "Geography",
         "id" : 3
      },
      {
         "id" : 4,
         "type" : "History"
      },
      {
         "type" : "Entertainment",
         "id" : 5
      },
      {
         "type" : "Sports",
         "id" : 6
      }
   ],
   "current_category" : null
}                             
                                  
```
#### DELETE '/questions/&lt;int:question_id&gt;'
- Deletes specific question:

Request specefications:
- String query: None
- Arguments: id to specify the question from the collection
- Body: None

curl localhost:5000/questions/6 -X DELETE

Response example:
```
{
   "success" : true,
   "deleted_question_id" : 6
}
                                  
```
#### POST '/questions'
- Creates or searches questions:
Request specefications:
- String query: None
- Arguments: None
- Body:
```
{
  "question": "who created Linux'?",
  "answer": "Linus Torvalds",
  "category": "4",
  "difficulty": "4"
  "searchTerm": "some pattern"
}
```
##### to create a question

Response example:
```
{
    "question": {
        "answer": "Linus Torvalds",
        "category": 4,
        "difficulty": 4,
        "id": 25,
        "question": "who created Linux'?"
    },
    "success": true
}
```
##### to search for questions

curl localhost:5000/questions -X POST -H 'Content-Type: application/json' -d '{"searchTerm": "wHaT"}'

Response example:
```
{
   "current_category" : null,
   "success" : true,
   "questions" : [
      {
         "answer" : "Apollo 13",
         "difficulty" : 4,
         "question" : "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
         "category" : 5,
         "id" : 2
      },
      {
         "question" : "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
         "category" : 5,
         "difficulty" : 4,
         "answer" : "Tom Cruise",
         "id" : 4
      }
   ],
   "total_questions" : 3
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



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
