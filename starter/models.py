import os
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "capstone"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

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

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    

    def format(self):
        return {
            'id': self.id,
            'title': self.type,
            'release_date' : self.release_date
        }


class Actor(db.Model):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age 
        self.gender = gender

    

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age' : self.age, 
            'gender' : self.gender
        }

