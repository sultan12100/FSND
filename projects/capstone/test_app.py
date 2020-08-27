import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, release_date_checker, db

from flask import jsonify


'''
CastingAgencyTest
        class of unittest, constains test cases of all api endpoints
        in both failure and seccuss
'''


class CastingAgencyTest(unittest.TestCase):
    '''
    setUp()
            sets up configurations before the corresponding test case
    '''

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']

        self.movie_to_add = {  # insertion will lead to success
            'title': 'back to the future 10',
            'release_date': '24-10-2020'
        }

        self.old_movie_to_add = {  # insertion will lead to failure
            'title': 'back to the future',
            'release_date': '3-7-1985',
        }

        self.actor_to_add = {
            'name': 'Rami Malek',
            'age': 39,
            'gender': 'm'
        }

        self.actor_to_add_wrong_json = {
            'full name': 'Leonardo DiCaprio',
            'age': 45,
            'gender': 'm'
        }

        self.movie_title_to_patch = {
            'title': 'back to the future 11',
        }

        self.actor_to_edit = {
            'age': 40
        }

        self.db = db
        self.db.init_app(self.app)
        # binds the app to the current context
        with self.app.app_context():
            # creates all tables
            self.db.create_all()

    '''
    tearDown()
            overridden method that might be used to
            reinitialize the internal state of the program
    '''

    def tearDown(self):
        pass

    '''
    test methods
    '''

    # testing of endpoint POST '/movies'

    def test01_add_movies(self):
        response = self.client().post('/movies', json=self.movie_to_add)
        data = json.loads(response.data)

        # making sure of crud operations by taking the movie object from
        # the database as dictionary based on the returned id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

        movie = Movie.query.get(data['movie']['id'])
        self.assertEqual(movie.title, self.movie_to_add['title'])
        self.assertEqual(movie.release_date, release_date_checker(
            self.movie_to_add['release_date']))

    def test02_error422_adding_old_movies(self):
        response = self.client().post('/movies', json=self.old_movie_to_add)
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    # testing of endpoint POST '/actors'

    def test03_add_actors(self):
        response = self.client().post('/actors', json=self.actor_to_add)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

        # making sure of crud operations by taking the movie object from
        # the database as dictionary based on the returned id
        actor = Actor.query.get(data['actor']['id'])
        self.assertEqual(actor.name, self.actor_to_add['name'])
        self.assertEqual(actor.age, self.actor_to_add['age'])
        self.assertEqual(actor.gender, self.actor_to_add['gender'])

    def test04_error422_adding_actor_wrong_json(self):
        response = self.client().post('/actors',
                                      json=self.actor_to_add_wrong_json)
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

    # testing of endpoint GET '/movies'

    def test05_get_movies(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test06_error405_deleting_movies_without_id(self):
        response = self.client().delete('/movies')
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method Not Allowed')

    # testing of endpoint GET '/actors'

    def test07_get_actors(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test08_error405_patching_actors_without_id(self):
        response = self.client().patch('/actors')
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method Not Allowed')

    # testing of endpoint PATCH '/movies/<int:movie_id>'

    def test09_edit_movies(self):
        movie_before = Movie.query.filter(
            Movie.title.ilike('back to the future 10')).first()
        response = self.client().patch('/movies/'+str(movie_before.id),
                                       json=self.movie_title_to_patch)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        movie_after = Movie.query.get(movie_before.id)
        self.assertEqual(movie_after.title,
                         self.movie_title_to_patch['title'])

    def test10_error400_editing_movies_with_empty_json(self):
        movie = Movie.query.first()
        response = self.client().patch('/movies/'+str(movie.id), json='')
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

    # testing of endpoint PATCH '/actors/<int:actor_id>'

    def test11_edit_actors(self):
        actor_before = Actor.query.filter(
            Actor.name.ilike('Rami Malek')).first()
        response = self.client().patch('/actors/'+str(actor_before.id),
                                       json={'age': 40})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        actor_after = Actor.query.get(actor_before.id)
        self.assertEqual(actor_after.age, 40)

    def test12_error405_editing_actors(self):
        response = self.client().get('/actors/1', json='')
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method Not Allowed')

    # testing of endpoint DELETE '/movies/<int:movie_id>'

    def test13_remove_movies(self):
        movie_to_delete = Movie.query.first()
        response = self.client().delete('/movies/'+str(movie_to_delete.id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        movie = Movie.query.get(movie_to_delete.id)
        self.assertFalse(movie)

    def test14_error405_putting_movies(self):
        response = self.client().put('/movies/1', json='')
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method Not Allowed')

        # testing of endpoint DELETE '/actors/<int:actor_id>'

    def test15_remove_actors(self):
        actor_to_delete = Actor.query.first()
        response = self.client().delete('/actors/'+str(actor_to_delete.id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        actor = Actor.query.get(actor_to_delete.id)
        self.assertFalse(actor)

    def test16_error405_deleting_actors_without_id(self):
        response = self.client().delete('/actors', json='')
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method Not Allowed')


if __name__ == "__main__":
    unittest.main()
