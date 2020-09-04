import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import sys

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,POST,DELETE,PATCH,OPTIONS')
    return response


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN (DONE)
'''


# db_drop_and_create_all()

# ROUTES


'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where
    drinks is the list of drinks
        or appropriate status code indicating reason for failure (DONE)
'''


@app.route('/drinks')
def get_drinks():
    try:
        drinks = [drink.short() for drink in Drink.query.all()]
        return jsonify({
            "success": True,
            "status": 200,
            "drinks": drinks
        })
    except Exception:
        abort(422)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where
    drinks is the list of drinks
        or appropriate status code indicating reason for failure (DONE)
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = [drink.long() for drink in Drink.query.all()]
        return jsonify({
            "success": True,
            "status": 200,
            "drinks": drinks
        })
    except Exception:
        abort(422)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where
    drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure (DONE)
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(payload):
    error400 = True  # to catch errors from parsing request body
    try:
        body = request.get_json()
        drink = Drink(title=body['title'], recipe=json.dumps(body['recipe']))
        error400 = False
        drink.insert()
        drink = [drink.long()]
        return jsonify({
            "success": True,
            "status": 200,
            "drinks": drink
        })
    except Exception:
        if error400:
            abort(400)
        else:
            abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where
    drink an array containing only the updated drink
        or appropriate status code indicating reason for failure (DONE)
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drinks(payload, drink_id):
    error400 = False
    try:
        body = request.get_json()
        drink = Drink.query.get(drink_id)
        if not drink:
            abort(404)
        drink.title = body.get('title', None)
        recipe = body.get('recipe', None)
        if drink.title is None and recipe is None:
            error400 = True
            raise Exception
        if recipe:
            drink.recipe = json.dumps(recipe)
        drink.update()
        drink = [drink.long()]
        return jsonify({
            "success": True,
            "status": 200,
            "drinks": drink
        })
    except Exception as e:
        if error400:
            abort(400)
        else:
            abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id
    is the id of the deleted record
        or appropriate status code indicating reason for failure (DONE)
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def remove_drinks(payload, drink_id):
    try:
        drink = Drink.query.get(drink_id)
        if not drink:
            abort(404)
        drink.delete()
        return jsonify({
            "success": True,
            "status": 200,
            "delete": drink_id
        })
    except Exception:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404
(DONE)
'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above (DONE)
'''


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above (DONE)
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code
