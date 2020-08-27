import os
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json
import dateutil.parser
import babel.dates
from datetime import datetime

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


'''
Movie
    Have title and release date
    rules:
      passed release date must not be prior to current date
      release date can be of any order if it is as follows mm-dd-y
      title and release_date are unique combinaiton
'''


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(String, nullable=False)

    # set up unique combinaiton
    __table_args__ = (db.UniqueConstraint(
        'title', 'release_date', name='title_release_date_constraint'),)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date_checker(release_date)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}


'''
release_date_checker(release_date)
    based on the algorithm in the project i worked on
    https://github.com/sultan12100/FSND/blob/master/projects/01_fyyur/app.py
    module format_datetime line: 136
'''


def release_date_checker(release_date):

    # parse dates to compare between them
    parsed_release_date = dateutil.parser.parse(release_date)
    parsed_current_date = dateutil.parser.parse(str(datetime.now()))
    if parsed_release_date < parsed_current_date:
        raise Exception
    formated_release_date = babel.dates.format_datetime(
        dateutil.parser.parse(str(parsed_release_date)), 'MM/dd/y')
    # take the first term (date) and leave the second term (time)
    return formated_release_date


'''
Actor
    Have name, age, and gender
    rules:
      string that represent the gender must be of one length
      the one character must be eaither m or f

'''


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    age = Column(Integer)
    gender = Column(String(1), nullable=False)

    def __init__(self, name, gender, age=None):
        self.name = name
        self.gender = gender_checker(gender.lower())
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}


'''
gender_checker(gender_char)
    takes the gender (single) character and
    checks if it's m or f and of length 1
'''


def gender_checker(gender_char):
    if len(gender_char) != 1:
        raise Exception
    if gender_char != 'm' and gender_char != 'f':
        raise Exception
    return gender_char
