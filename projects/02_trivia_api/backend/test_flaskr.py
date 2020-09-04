import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question_to_post = {
            'question': 'Who created Linux?',
            'answer': 'Linus Torvalds',
            'category': '4',
            'difficulty': '4',
        }
        self.search_term = {
            'searchTerm': '19'
        }
        self.empty_question_to_post = {
            'question': '',
            'answer': '',
            'category': '',
            'difficulty': '',
        }
        self.existed_question_to_post = {
            'question': "Whose autobiography is entitled 'I Know Why the Caged\
                 Bird Sings'?",
            'answer': 'Maya Angelou',
            'category': '2',
            'difficulty': '4',
        }
        self.to_play_quiz_game = {
            'previous_questions': [],
            'quiz_category': {
                'type': {
                    'id': 1,
                    'type': 'Science'
                },
                'id': '0'}
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for\
         expected errors.
    """

    # testing of endpoint GET '/categories'
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

    def test_405_creating_categories(self):
        response = self.client().post('/categories')
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method Not Allowed')
    ###########

    # GET '/questions'
    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'], None)

    def test_405_delete_questions_collection(self):
        response = self.client().delete('/questions')
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method Not Allowed')
    ###########

    # # DELETE '/questions/<int:question_id>'
    def test_delete_question(self):
        '''
         deleting question  In which royal palace would you find the Hall of\
              Mirrors?
        '''
        question_id = 14
        question_before = Question.query.filter(
            Question.id == question_id).one_or_none()
        response = self.client().delete('/questions/'+str(question_id))
        data = json.loads(response.data)
        question_after = Question.query.filter(
            Question.id == question_id).one_or_none()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_question_id'], question_id)
        self.assertTrue(question_before)
        self.assertFalse(question_after)

    def test_404_delete_not_found_question(self):
        response = self.client().delete('/questions/1000')
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')
    ##########

    # POST '/questions'
    # creating question
    def test_create_question(self):
        response = self.client().post('/questions',
                                      json=self.new_question_to_post)
        data = json.loads(response.data)
        question = Question.query.filter(
            Question.id == data['question']['id']).one_or_none()
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(question)

    # searching questions
    def test_search_questions(self):
        response = self.client().post('/questions',
                                      json=self.search_term)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertFalse(data['current_category'])

    def test_400_create_empty_question(self):
        response = self.client().post('/questions',
                                      json=self.empty_question_to_post)
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

    def test_422_create_existed_question(self):
        response = self.client().post('/questions',
                                      json=self.existed_question_to_post)
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
    ###########

    # GET '/categories/<int:category_id>/questions'
    def test_get_category_questions(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 1)
        self.assertEqual(data['questions'][0]['category'], 1)

    def test_404_get_invalid_category_questions(self):
        response = self.client().get('/categories/1234/questions',
                                     json=self.existed_question_to_post)
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    # POST '/quizzes'
    def test_play_quiz_game(self):
        response = self.client().post('/quizzes',
                                      json=self.to_play_quiz_game)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_422_empty_json_to_play(self):
        response = self.client().post('/quizzes',
                                      json={})
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
