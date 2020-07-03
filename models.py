import os
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "capstone"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = "postgres://ozpvkhqfsyxrld:cbc327f695b5788279d0b76f15d5b105704b36724541fd21611d7e2279f338e3@ec2-3-216-129-140.compute-1.amazonaws.com:5432/dd54kb4mbdfd03"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = db.Column(db.DateTime())
    actors = db.relationship(
        'Movie_Actor_relation',
        cascade="all, delete-orphan",
        backref='movie',
        lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

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
            'release_date': self.release_date,
            'actors': [actor.id for actor in self.actors]
        }


class Actor(db.Model):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    movies = db.relationship(
        'Movie_Actor_relation',
        cascade="all, delete-orphan",
        backref='actor',
        lazy=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

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
            'gender': self.gender,
            'movies': [movie.id for movie in self.movies]
        }


class Movie_Actor_relation(db.Model):
    __tablename__ = 'movie_actor_relation'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'movie.id',
            ondelete="CASCADE"),
        nullable=False)
    actor_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'actor.id',
            ondelete="CASCADE"),
        nullable=False)
