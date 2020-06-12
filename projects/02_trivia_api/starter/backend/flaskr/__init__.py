import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formated_questions = [question.format() for question in questions]
    current_formated_questions = formated_questions[start:end]

    return current_formated_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after
  completing the TODOs
  (DONE)
  '''
    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  (DONE)
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origins',
                             '*')
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  (DONE)
  '''

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)
        formated_categories = [category.format() for category in categories]
        return jsonify({
            'success': True,
            'categories': formated_categories,
            'total_categories': len(categories)
        })

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories. (DONE)

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three
  pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_formated_questions = paginate_questions(request, questions)
        if len(current_formated_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()

        formated_categories = [category.format() for category in categories]
        return jsonify({
            'success': True,
            'questions': current_formated_questions,
            'total_questions': len(questions),
            'categories': formated_categories,
            'current_category': None
        })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID. (DONE)

  TEST: When you click the trash icon next to a question, the question will be
  removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        error404 = False
        try:
            question = Question.query.order_by(Question.id).filter(
                Question.id == question_id).one_or_none()
            if not question:
                error404 = True
            question.delete()
            return jsonify({
                'success': True,
                'deleted_question_id': question_id
            })
        except:
            if error404:
                abort(404)
            else:
                abort(422)

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score. (DONE)

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.(DONE)

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        # FormView
        error422 = False
        try:
            question = body.get('question')
            if question is not None:
                if not Question.query.filter(Question.question.ilike(
                        question)).one_or_none():
                    answer = body['answer']
                    if not answer:
                        raise Exception
                    category_id = int(body['category'])+1
                    difficulty = int(body['difficulty'])
                    question_orm = Question(
                        question, answer, category_id, difficulty)
                    question_orm.insert()
                    return jsonify({
                        'success': True,
                        'question': question_orm.format()
                    })
                else:
                    error422 = True
                    raise Exception  # if questions was there raise error

            else:
                # QuestionView
                search_term = body['searchTerm']
                results = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%'+search_term+'%')).all()
                current_results = paginate_questions(request, results)
                return jsonify({
                    'success': True,
                    'questions': current_results,
                    'total_questions': Question.query.count(),
                    'current_category': None
                })
        except:
            if error422:
                abort(422)
            else:
                abort(400)

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.(DONE)

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        if Category.query.filter(Category.id == category_id).count() == 0:
            abort(404)
        try:
            category_questions = Question.query.order_by(Question.id).filter(
                Question.category == category_id).order_by(Question.id).all()
            current_formated_category_questions = paginate_questions(
                request, category_questions)
            return jsonify({
                'success': True,
                'questions': current_formated_category_questions,
                'total_questions': len(category_questions),
                'current_category': category_id
            })
        except:
            abort(422)

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.(DONE)

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    @app.route('/quizzes', methods=['POST'])
    def play_quize_game():
        body = request.get_json()

        previous_questions_IDs = body.get('previous_questions')
        quiz_category = body.get('quiz_category')
        if quiz_category.get('type') != 'click':
            quiz_category_id = int(quiz_category.get('type').get('id'))
            questions = Question.query.filter(
                Question.category == quiz_category_id).all()
        else:
            questions = Question.query.all()

        questions_IDs = {
            question.id for question in questions}  # returns set
        list_of_possible_IDs = list(
            set(questions_IDs) - set(previous_questions_IDs))
        if len(list_of_possible_IDs) == 0:
            return jsonify({
                'succes': True,
                'question': None
            })

        random_question_id = random.choice(list_of_possible_IDs)
        random_question = Question.query.filter(
            Question.id == random_question_id).one_or_none()
        return jsonify({
            'succes': True,
            'question': random_question.format()
        })

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422. (DONE)
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
    Note: this 500 error handle, will only work if server is not working on
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
