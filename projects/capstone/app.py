import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Movie, Actor
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app TODO
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # TODO
    # CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Access-Control-Allow-Headers',
    #                         'Content-Type,Authorization,true')
    #     response.headers.add('Access-Control-Allow-Methods',
    #                         'GET,POST,DELETE,PATCH,OPTIONS')
    #     return response

    '''
    GET /movies
    returns status code 200 and list of movies,
        otherwise appropriate json indicating reason for failure
    allowed roles: Casting Assistant, Casting Director, Executive Producer
    permission: get:movies
    '''
    @app.route('/movies')
    def get_movies():
        try:
            movies = [movie.format() for movie in Movie.query.all()]
        except Exception:
            abort(422)
        return jsonify({
            'success': True,
            'status': 200,
            'movies': movies
        })

    '''
    GET /actors
    returns status code 200 and list of actors,
        otherwise appropriate json indicating reason for failure
    allowed roles: Casting Assistant, Casting Director, Executive Producer
    permission: get:actors
    '''
    @app.route('/actors')
    def get_actors():
        try:
            actors = [actor.format() for actor in Actor.query.all()]
        except Exception:
            abort(422)
        return jsonify({
            'success': True,
            'status': 200,
            'actors': actors
        })

    '''
    POST /movies
    returns status code 200 and newly added movie,
        otherwise appropriate json indicating reason for failure
    allowed roles: Executive Producer
    permission: post:movies
    '''
    @app.route('/movies', methods=['POST'])
    def add_movies():
        error = 400
        try:
            body = request.get_json()
            title = body['title']
            release_date = body['release_date']
            error = 422
            movie = Movie(title, release_date)
            movie.insert()
        except Exception:
            abort(error)
        return jsonify({
            'success': True,
            'status': 200,
            'movie': movie.format()
        })

    '''
    POST /actors
    returns status code 200 and newly added actor,
        otherwise appropriate json indicating reason for failure
    allowed roles: Casting Director, Executive Producer
    permission: post:actors
    '''
    @app.route('/actors', methods=['POST'])
    def add_actors():
        error = 400
        try:
            body = request.get_json()
            name = body['name']
            age = body['age']
            gender = body['gender']
            error = 422
            actor = Actor(name, gender, age)
            actor.insert()
        except Exception:
            abort(error)
        return jsonify({
            'success': True,
            'status': 200,
            'actor': actor.format()
        })

    '''
    PATCH /movies/<int:movie_id>
    returns status code 200 and the modified movie,
        otherwise appropriate json indicating reason for failure
    allowed roles: Casting Director, Executive Producer
    permission: patch:movies
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def edit_movies(movie_id):
        error = 422
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                error = 404
                raise Exception

            body = request.get_json()

            edit_flag = False
            if 'title' in body:
                movie.title = body['title']
                edit_flag = True
            if 'release_date' in body:
                movie.release_date = body['release_date']
                edit_flag = True
            if not edit_flag:
                error = 400
                raise Exception
            movie.update()
        except Exception:
            abort(error)
        return jsonify({
            'success': True,
            'status': 200,
            'movie': movie.format()
        })

    '''
    PATCH /actors/<int:actor_id>
    returns status code 200 and the modified actor,
        otherwise appropriate json indicating reason for failure
    allowed roles: Casting Director, Executive Producer
    permission: patch:actors
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def edit_actors(actor_id):
        error = 422
        try:
            actor = Actor.query.get(actor_id)
            if not actor:
                error = 404
                raise Exception

            body = request.get_json()

            edit_flag = False
            if 'name' in body:
                actor.name = body['name']
                edit_flag = True
            if 'age' in body:
                actor.age = body['age']
                edit_flag = True
            if 'gender' in body:
                actor.gender = body['gender']
                edit_flag = True

            if not edit_flag:
                error = 400
                raise Exception

            actor.update()
        except Exception:
            abort(error)
        return jsonify({
            'success': True,
            'status': 200,
            'actor': actor.format()
        })

    '''
    DELETE /movies/<int:movie_id>
    returns status code 200 and the deleted movie id,
        otherwise appropriate json indicating reason for failure
    allowed roles: Executive Producer
    permission: delete:movies
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def remove_movies(movie_id):
        error = 422
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                error = 404
                raise Exception
            movie.delete()
        except Exception:
            abort(error)

        return jsonify({
            'success': True,
            'status': 200,
            'id': movie.id
        })

    '''
    DELETE /actors/<int:actor_id>'
    returns status code 200 and the deleted actor id,
        otherwise appropriate json indicating reason for failure
    allowed roles: Casting Director, Executive Producer
    permission: delete:actors
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def remove_actors(actor_id):
        error = 422
        try:
            actors = Actor.query.get(actor_id)
            if not actors:
                error = 404
                raise Exception
            actors.delete()
        except Exception:
            abort(error)

        return jsonify({
            'success': True,
            'status': 200,
            'id': actors.id
        })

    '''
    error handlers: if any error occures it will responde with the
    corresponding error messages in json format
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422
    '''
    Note: this 500 error handler, will only work if server is not working on
    Debug mode
    '''
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app


app = create_app()


if __name__ == '__main__':
    app.run()
    # APP.run(host='0.0.0.0', port=8080, debug=True)
